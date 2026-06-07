#!/bin/bash
set -euo pipefail

SOURCE_ROOT="${SOURCE_ROOT:-/src/endeavouros-pipa}"
BUILDER_ROOT="$SOURCE_ROOT/pipa-endeavouros-builder"
CONFIG_DIR="${CONFIG_DIR:-/config}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/repo}"
REPO_SUBDIR="${REPO_SUBDIR:-repo}"
REPO_DIR="$OUTPUT_ROOT/$REPO_SUBDIR"
MAKEPKG_USER="${MAKEPKG_USER:-builder}"

if [ ! -d "$BUILDER_ROOT/pkgbuilds" ]; then
    echo "Missing package sources under $BUILDER_ROOT/pkgbuilds" >&2
    exit 1
fi

if [ ! -f "$CONFIG_DIR/packages.local.txt" ]; then
    echo "Missing local package list: $CONFIG_DIR/packages.local.txt" >&2
    exit 1
fi

mkdir -p "$REPO_DIR"
chown -R "$MAKEPKG_USER:$MAKEPKG_USER" "$REPO_DIR"

mapfile -t PKGS < <(grep -vE '^[[:space:]]*(#|$)' "$CONFIG_DIR/packages.local.txt")

for pkg in "${PKGS[@]}"; do
    pkg_dir="$BUILDER_ROOT/pkgbuilds/$pkg"
    if [ ! -d "$pkg_dir" ]; then
        echo "Missing PKGBUILD directory for $pkg at $pkg_dir" >&2
        exit 1
    fi

    echo "### Building $pkg"
    chown -R "$MAKEPKG_USER:$MAKEPKG_USER" "$pkg_dir"
    su "$MAKEPKG_USER" -c "cd '$pkg_dir' && rm -f ./*.pkg.tar.* && makepkg --nodeps --noconfirm --nocheck"

    built_packages=()
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

    cp "${built_packages[@]}" "$REPO_DIR/"

    install_packages=()
    for package_path in "${built_packages[@]}"; do
        case "$(basename "$package_path")" in
            *-debug-*.pkg.tar.*|*-headers-*.pkg.tar.*) ;;
            *) install_packages+=("$package_path") ;;
        esac
    done

    if [ "$pkg" != "linux-pipa" ] && [ ${#install_packages[@]} -gt 0 ]; then
        pacman -U --noconfirm --ask=4 "${install_packages[@]}"
    fi
done
