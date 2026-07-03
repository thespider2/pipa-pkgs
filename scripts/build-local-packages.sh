#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_LOCAL_BUILDER_ROOT="$ROOT_DIR"
if [ -d /work/common ] || [ -d /work/sm8250 ]; then
    DEFAULT_LOCAL_BUILDER_ROOT="/work"
fi
LOCAL_BUILDER_ROOT="${LOCAL_BUILDER_ROOT:-$DEFAULT_LOCAL_BUILDER_ROOT}"
SOURCE_ROOT="${SOURCE_ROOT:-/src/endeavouros-pipa}"
FALLBACK_BUILDER_ROOT="$SOURCE_ROOT/pipa-endeavouros-builder"
CONFIG_DIR="${CONFIG_DIR:-/config}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/repo}"
REPO_SUBDIR="${REPO_SUBDIR:-repo}"
REPO_DIR="$OUTPUT_ROOT/$REPO_SUBDIR"
CACHE_DIR="$REPO_DIR/.build-cache"
MAKEPKG_USER="${MAKEPKG_USER:-builder}"

if [ -d "$LOCAL_BUILDER_ROOT/common" ] || [ -d "$LOCAL_BUILDER_ROOT/sm8250" ]; then
    BUILDER_ROOT="$LOCAL_BUILDER_ROOT"
elif [ -d "$FALLBACK_BUILDER_ROOT/common" ] || [ -d "$FALLBACK_BUILDER_ROOT/sm8250" ]; then
    BUILDER_ROOT="$FALLBACK_BUILDER_ROOT"
else
    echo "Missing package sources under $LOCAL_BUILDER_ROOT/{common,sm8250} and $FALLBACK_BUILDER_ROOT/{common,sm8250}" >&2
    exit 1
fi

if [ ! -f "$CONFIG_DIR/packages.local.txt" ]; then
    echo "Missing local package list: $CONFIG_DIR/packages.local.txt" >&2
    exit 1
fi

mkdir -p "$REPO_DIR"
mkdir -p "$CACHE_DIR"
chown -R "$MAKEPKG_USER:$MAKEPKG_USER" "$REPO_DIR"

compute_pkg_source_hash() {
    local pkg_dir="$1"

    python - "$pkg_dir" <<'PY'
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ignore_dirs = {"src", "pkg", ".git"}
ignore_suffixes = (
    ".pkg.tar",
    ".pkg.tar.gz",
    ".pkg.tar.xz",
    ".pkg.tar.zst",
    ".src.tar",
    ".src.tar.gz",
    ".src.tar.xz",
    ".src.tar.zst",
)

digest = hashlib.sha256()

for path in sorted(root.rglob("*")):
    rel = path.relative_to(root)

    if any(part in ignore_dirs for part in rel.parts):
        continue
    if path.is_dir():
        continue
    if any(path.name.endswith(suffix) for suffix in ignore_suffixes):
        continue

    digest.update(str(rel).encode("utf-8"))
    digest.update(b"\0")
    digest.update(path.read_bytes())
    digest.update(b"\0")

print(digest.hexdigest())
PY
}

collect_pkg_dependencies() {
    local pkg_dir="$1"

    env -i HOME="$HOME" bash --noprofile --norc -c '
        set -e
        source "$1"
        printf "%s\n" "${depends[@]-}" "${makedepends[@]-}"
    ' _ "$pkg_dir/PKGBUILD" | awk 'NF' | sort -u
}

find_local_dependency_archives() {
    local package_name="$1"

    shopt -s nullglob
    local matches=("$REPO_DIR"/"${package_name}"-*.pkg.tar.zst "$REPO_DIR"/"${package_name}"-*.pkg.tar.xz)
    shopt -u nullglob

    if [ ${#matches[@]} -eq 0 ]; then
        return 1
    fi

    printf '%s\n' "${matches[@]}" | xargs -r ls -1t | head -n1
}

mapfile -t PKGS < <(grep -vE '^[[:space:]]*(#|$)' "$CONFIG_DIR/packages.local.txt")

for pkg in "${PKGS[@]}"; do
    if [ -d "$BUILDER_ROOT/common/$pkg" ]; then
        pkg_dir="$BUILDER_ROOT/common/$pkg"
    elif [ -d "$BUILDER_ROOT/sm8250/$pkg" ]; then
        pkg_dir="$BUILDER_ROOT/sm8250/$pkg"
    else
        echo "Missing PKGBUILD directory for $pkg in common/ or sm8250/" >&2
        exit 1
    fi
    cache_file="$CACHE_DIR/$pkg"

    pkg_source_hash="$(compute_pkg_source_hash "$pkg_dir")"
    built_packages=()

    if [ -f "$cache_file" ]; then
        mapfile -t cache_lines < "$cache_file"
        if [ "${#cache_lines[@]}" -gt 1 ] && [ "${cache_lines[0]}" = "$pkg_source_hash" ]; then
            cache_hit=1
            for package_name in "${cache_lines[@]:1}"; do
                if [ -f "$REPO_DIR/$package_name" ]; then
                    built_packages+=("$REPO_DIR/$package_name")
                else
                    cache_hit=0
                    built_packages=()
                    break
                fi
            done
            if [ "$cache_hit" -eq 1 ] && [ ${#built_packages[@]} -gt 0 ]; then
                echo "### Reusing cached build for $pkg"
            fi
        fi
    fi

    if [ ${#built_packages[@]} -eq 0 ]; then
        echo "### Building $pkg"
        chown -R "$MAKEPKG_USER:$MAKEPKG_USER" "$pkg_dir"
        mapfile -t pkg_dependencies < <(collect_pkg_dependencies "$pkg_dir")
        if [ ${#pkg_dependencies[@]} -gt 0 ]; then
            remote_dependencies=()
            local_dependency_archives=()

            for dependency in "${pkg_dependencies[@]}"; do
                if printf '%s\n' "${PKGS[@]}" | grep -Fxq "$dependency"; then
                    if local_archive="$(find_local_dependency_archives "$dependency")"; then
                        local_dependency_archives+=("$local_archive")
                    else
                        echo "Missing local dependency package for $dependency in $REPO_DIR" >&2
                        exit 1
                    fi
                else
                    remote_dependencies+=("$dependency")
                fi
            done

            if [ ${#remote_dependencies[@]} -gt 0 ]; then
                mapfile -t unsatisfied < <(pacman -T "${remote_dependencies[@]}" 2>/dev/null || true)
                if [ ${#unsatisfied[@]} -gt 0 ] && [ -n "${unsatisfied[0]}" ]; then
                    pacman -S --needed --noconfirm "${unsatisfied[@]}"
                fi
            fi

            if [ ${#local_dependency_archives[@]} -gt 0 ]; then
                pacman -U --noconfirm --ask=4 "${local_dependency_archives[@]}"
            fi
        fi
        su "$MAKEPKG_USER" -c "cd '$pkg_dir' && rm -f ./*.pkg.tar.* ./*.src.tar.* && makepkg --nodeps --noconfirm --nocheck"

        shopt -s nullglob
        for package_path in "$pkg_dir"/*.pkg.tar.zst "$pkg_dir"/*.pkg.tar.xz; do
            case "$(basename "$package_path")" in
                *-debug-*.pkg.tar.*|*-headers-*.pkg.tar.*) ;;
                *) built_packages+=("$package_path") ;;
            esac
        done
        shopt -u nullglob

        if [ ${#built_packages[@]} -eq 0 ]; then
            echo "No package archives were produced for $pkg" >&2
            exit 1
        fi

        if [ -f "$cache_file" ]; then
            mapfile -t old_cache_lines < "$cache_file"
            for old_package_name in "${old_cache_lines[@]:1}"; do
                rm -f "$REPO_DIR/$old_package_name"
            done
        fi

        cp -f "${built_packages[@]}" "$REPO_DIR/"

        repo_packages=()
        for package_path in "${built_packages[@]}"; do
            repo_packages+=("$REPO_DIR/$(basename "$package_path")")
        done
        built_packages=("${repo_packages[@]}")

        {
            printf '%s\n' "$pkg_source_hash"
            for package_path in "${built_packages[@]}"; do
                basename "$package_path"
            done
        } > "$cache_file"
    fi

    install_packages=()
    for package_path in "${built_packages[@]}"; do
        case "$(basename "$package_path")" in
            *-debug-*.pkg.tar.*|*-headers-*.pkg.tar.*) ;;
            *) install_packages+=("$package_path") ;;
        esac
    done

    # Keep the builder container lean: do not install the kernel package there,
    # and skip the meta package because it depends on linux-pipa being installed.
    case "$pkg" in
        linux-pipa|pipa-metapkg)
            ;;
        *)
            if [ ${#install_packages[@]} -gt 0 ]; then
                pacman -U --noconfirm --ask=4 "${install_packages[@]}"
            fi
            ;;
    esac
done
