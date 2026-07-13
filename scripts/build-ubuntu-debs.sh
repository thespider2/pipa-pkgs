#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UB_DIR="$ROOT_DIR/ubuntu"
PKGS_DIR="$UB_DIR/packages"
DEB_REPO_DIR="$ROOT_DIR/repo/ubuntu"
BUILD_DIR="$UB_DIR/.build"
CACHE_DIR="$UB_DIR/.build-cache"
SOURCES_DIR="$UB_DIR/.sources"
DL_DIR="$UB_DIR/.downloads"

mkdir -p "$DEB_REPO_DIR" "$BUILD_DIR" "$CACHE_DIR" "$SOURCES_DIR" "$DL_DIR"

link_files() {
    local dest="$1"; shift
    mkdir -p "$dest"
    for src in "$@"; do
        if [ -e "$src" ]; then
            cp -a "$src" "$dest/"
        else
            echo "WARNING: $src not found"
        fi
    done
}

compute_source_hash() {
    local name="$1"
    local pkg_debian="$PKGS_DIR/$name/debian"
    local src_dir="$SOURCES_DIR/$name"
    python3 - "$pkg_debian" "$src_dir" <<'PY'
import hashlib, pathlib, sys
digest = hashlib.sha256()
for arg in sys.argv[1:]:
    path = pathlib.Path(arg)
    if path.is_file():
        digest.update(b"file\0")
        digest.update(path.read_bytes())
    elif path.is_dir():
        for p in sorted(path.rglob("*")):
            if p.is_dir():
                continue
            digest.update(str(p.relative_to(path)).encode())
            digest.update(b"\0")
            digest.update(p.read_bytes())
            digest.update(b"\0")
print(digest.hexdigest())
PY
}

download() {
    local url="$1"
    local out="$2"
    if [ -f "$out" ]; then
        return 0
    fi
    echo "  Downloading $(basename "$out")"
    wget -q -O "$out" "$url"
}

stage_common_sources() {
    echo "=== Staging local extras into package trees ==="

    link_files "$SOURCES_DIR/hexagonrpc" \
        "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-adsp-rootpd.service" \
        "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-adsp-sensorspd.service" \
        "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-sdsp.service" \
        "$ROOT_DIR/common/hexagonrpc/sysusers.conf" \
        "$ROOT_DIR/common/hexagonrpc/10-fastrpc.rules"

    link_files "$SOURCES_DIR/xiaomi-pipa-firmware" \
        "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/"*.files

    link_files "$SOURCES_DIR/pipa-dracut" \
        "$ROOT_DIR/sm8250/pipa-dracut/module-setup.sh" \
        "$ROOT_DIR/sm8250/pipa-dracut/pipa.conf" \
        "$ROOT_DIR/sm8250/pipa-dracut/pipa-refresh-initramfs"

    link_files "$SOURCES_DIR/pipa-grub-config" \
        "$ROOT_DIR/sm8250/pipa-grub-config/pipa-refresh-grub-config"

    link_files "$SOURCES_DIR/libssc" \
        "$ROOT_DIR/common/libssc/"0*.patch

    link_files "$SOURCES_DIR/iio-sensor-proxy" \
        "$ROOT_DIR/common/iio-sensor-proxy/"0*.patch

    link_files "$SOURCES_DIR/pipa-sensors" \
        "$ROOT_DIR/sm8250/pipa-sensors/81-libssc-xiaomi-pipa.rules" \
        "$ROOT_DIR/sm8250/pipa-sensors/hexagonrpcd-sdsp.conf" \
        "$ROOT_DIR/sm8250/pipa-sensors/pipa-prepare-sensor-persist" \
        "$ROOT_DIR/sm8250/pipa-sensors/pipa-sensors-persist.service" \
        "$ROOT_DIR/sm8250/pipa-sensors/pipa-sensors-resume" \
        "$ROOT_DIR/sm8250/pipa-sensors/iio-sensor-proxy-pipa-audio.conf" \
        "$ROOT_DIR/sm8250/pipa-sensors/pipa-audio-init-sensors.conf" \
        "$ROOT_DIR/sm8250/pipa-sensors/pipa-sensors.tmpfiles" \
        "$ROOT_DIR/sm8250/pipa-sensors/hexagonrpcd-sdsp-pipa-sensors.conf"

    link_files "$SOURCES_DIR/pipa-sound-conf" \
        "$ROOT_DIR/sm8250/pipa-sound-conf/51-pipa.conf" \
        "$ROOT_DIR/sm8250/pipa-sound-conf/52-pipa-camera.conf" \
        "$ROOT_DIR/sm8250/pipa-sound-conf/pipewire-softisp-cpu.conf" \
        "$ROOT_DIR/sm8250/pipa-sound-conf/pipa-audio-init" \
        "$ROOT_DIR/sm8250/pipa-sound-conf/pipa-audio-init.service" \
        "$ROOT_DIR/sm8250/alsa-ucm-conf-sm8250/HiFi_pipa.conf"
    cp -f "$ROOT_DIR/sm8250/alsa-ucm-conf-sm8250/Xiaomi Pad 6.conf" \
        "$SOURCES_DIR/pipa-sound-conf/Xiaomi-Pad-6.conf"

    link_files "$SOURCES_DIR/libcamera" \
        "$ROOT_DIR/common/libcamera/"0*.patch \
        "$ROOT_DIR/common/libcamera/hi846.yaml" \
        "$ROOT_DIR/common/libcamera/ov13b10.yaml"

    link_files "$SOURCES_DIR/linux-pipa" \
        "$ROOT_DIR/sm8250/linux-pipa/pipa.config" \
        "$ROOT_DIR/sm8250/linux-pipa/"0*.patch

    link_files "$SOURCES_DIR/pipa-metapkg" \
        "$ROOT_DIR/sm8250/pipa-metapkg/90-pipa-gsk-renderer.sh" \
        "$UB_DIR/pipa-pkgs.list"
}

prepare_build_tree() {
    local name="$1"
    local work="$BUILD_DIR/$name"
    rm -rf "$work"
    mkdir -p "$work"
    cp -a "$PKGS_DIR/$name/debian" "$work/debian"
    mkdir -p "$work/debian/extras"
    if [ -d "$SOURCES_DIR/$name" ]; then
        cp -a "$SOURCES_DIR/$name"/. "$work/debian/extras/" 2>/dev/null || true
    fi
    chmod +x "$work/debian/rules"
    [ -f "$work/debian/install-firmware.sh" ] && chmod +x "$work/debian/install-firmware.sh"
    # Minimal copyright if missing
    if [ ! -f "$work/debian/copyright" ]; then
        cat > "$work/debian/copyright" <<EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: $name
Files: *
Copyright: Xiaomi Pad 6 / pipa contributors
License: GPL-2.0-or-later OR MIT OR proprietary
EOF
    fi
    echo "$work"
}

fetch_and_extract() {
    local name="$1"
    local work="$2"
    case "$name" in
        bootmac)
            local ver=0.6.0
            local tar="$DL_DIR/bootmac-v${ver}.tar.gz"
            download "https://gitlab.postmarketos.org/postmarketOS/bootmac/-/archive/v${ver}/bootmac-v${ver}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            ;;
        swclock-offset)
            local ver=0.3.0
            local tar="$DL_DIR/swclock-offset-${ver}.tar.gz"
            download "https://gitlab.postmarketos.org/postmarketOS/swclock-offset/-/archive/${ver}/swclock-offset-${ver}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            ;;
        hexagonrpc)
            local ver=0.4.0
            local tar="$DL_DIR/hexagonrpc-${ver}.tar.gz"
            download "https://github.com/linux-msm/hexagonrpc/archive/refs/tags/v${ver}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            ;;
        xiaomi-pipa-firmware)
            local commit=842d35beffeda8c6d1b0e611b335543bf0e6b41e
            local tar="$DL_DIR/xiaomi-pipa-firmware-${commit}.tar.gz"
            download "https://github.com/pipa-mainline/xiaomi-pipa-firmware/archive/${commit}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work"
            ;;
        libssc)
            local ver=0.4.4
            local tar="$DL_DIR/libssc-${ver}.tar.gz"
            download "https://codeberg.org/DylanVanAssche/libssc/archive/v${ver}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            for p in "$work"/debian/extras/0*.patch; do
                [ -f "$p" ] || continue
                (cd "$work" && patch -p1 -F2 < "$p")
            done
            ;;
        iio-sensor-proxy)
            local commit=0085ddf8ecb173a1c5fcf2344aa40e561125354f
            local tar="$DL_DIR/iio-sensor-proxy-${commit}.tar.gz"
            download "https://gitlab.freedesktop.org/hadess/iio-sensor-proxy/-/archive/${commit}/iio-sensor-proxy-${commit}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            for p in "$work"/debian/extras/0*.patch; do
                [ -f "$p" ] || continue
                (cd "$work" && patch -p1 -F2 < "$p")
            done
            ;;
        libcamera)
            local ver=0.7.1
            local tar="$DL_DIR/libcamera-${ver}.tar.gz"
            download "https://github.com/libcamera-org/libcamera/archive/refs/tags/v${ver}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            for p in "$work"/debian/extras/0*.patch; do
                [ -f "$p" ] || continue
                (cd "$work" && patch -p1 -F2 < "$p" || patch -p1 -F2 --forward < "$p" || true)
            done
            ;;
        linux-pipa)
            local commit=afac0607a1046fe1dcdd341297a2144d5013272a
            local tar="$DL_DIR/linux-${commit}.tar.gz"
            download "https://github.com/aymanrgab/linux/archive/${commit}.tar.gz" "$tar"
            tar -xzf "$tar" -C "$work" --strip-components=1
            ;;
        pipa-dracut|pipa-grub-config|pipa-sensors|pipa-sound-conf|pipa-metapkg)
            # Local-only payload packages; extras already staged.
            touch "$work/README"
            ;;
        *)
            echo "Unknown package fetch: $name"
            exit 1
            ;;
    esac
}

publish_debs() {
    local work="$1"
    shopt -s nullglob
    for deb in "$work"/../*.deb "$BUILD_DIR"/*.deb; do
        [ -f "$deb" ] || continue
        case "$(basename "$deb")" in
            *-dbgsym_*) continue ;;
        esac
        cp -f "$deb" "$DEB_REPO_DIR/"
    done
    # dpkg-buildpackage writes to parent of work
    for deb in "$BUILD_DIR"/*.deb; do
        [ -f "$deb" ] || continue
        case "$(basename "$deb")" in
            *-dbgsym_*) continue ;;
        esac
        cp -f "$deb" "$DEB_REPO_DIR/"
    done
    shopt -u nullglob
}

compose_apt_repo() {
    echo "=== Composing apt repo at $DEB_REPO_DIR ==="
    cd "$DEB_REPO_DIR"
    dpkg-scanpackages --multiversion . /dev/null > Packages
    gzip -9c Packages > Packages.gz
    cat > Release <<EOF
Origin: pipa-pkgs
Label: pipa-pkgs
Suite: resolute
Codename: resolute
Architectures: arm64 all
Components: main
Description: Xiaomi Pad 6 packages for Ubuntu
EOF
}

cache_hit() {
    local name="$1"
    local hash="$2"
    local cache_file="$CACHE_DIR/$name"
    [ -f "$cache_file" ] || return 1
    local cached_hash
    cached_hash="$(head -n1 "$cache_file")"
    [ "$cached_hash" = "$hash" ] || return 1
    local deb
    while IFS= read -r deb; do
        [ -n "$deb" ] || continue
        [ -f "$CACHE_DIR/debs/$deb" ] || return 1
        cp -f "$CACHE_DIR/debs/$deb" "$DEB_REPO_DIR/$deb"
    done < <(tail -n +2 "$cache_file")
    return 0
}

save_cache() {
    local name="$1"
    local hash="$2"
    shift 2
    mkdir -p "$CACHE_DIR/debs"
    local cache_file="$CACHE_DIR/$name"
    {
        echo "$hash"
        for deb in "$@"; do
            [ -f "$DEB_REPO_DIR/$deb" ] || continue
            cp -f "$DEB_REPO_DIR/$deb" "$CACHE_DIR/debs/$deb"
            echo "$deb"
        done
    } > "$cache_file"
}

list_new_debs() {
    local before_file="$1"
    local after_list=()
    local f
    shopt -s nullglob
    for f in "$DEB_REPO_DIR"/*.deb; do
        local base
        base="$(basename "$f")"
        if ! grep -qxF "$base" "$before_file" 2>/dev/null; then
            after_list+=("$base")
        fi
    done
    shopt -u nullglob
    printf '%s\n' "${after_list[@]}"
}

BUILD_ORDER=(
    bootmac
    swclock-offset
    hexagonrpc
    xiaomi-pipa-firmware
    pipa-dracut
    pipa-grub-config
    libssc
    iio-sensor-proxy
    pipa-sensors
    pipa-sound-conf
    libcamera
    linux-pipa
    pipa-metapkg
)

stage_common_sources

# Install previously built packages so later builds can depend on them
if ls "$DEB_REPO_DIR"/*.deb >/dev/null 2>&1; then
    echo "=== Installing existing debs for build-deps ==="
    dpkg -i "$DEB_REPO_DIR"/*.deb 2>/dev/null || apt-get -f install -y || true
fi

BUILT=0
SKIPPED=0
FAILED=0

for name in "${BUILD_ORDER[@]}"; do
    echo ""
    echo "--- $name ---"
    if [ ! -d "$PKGS_DIR/$name/debian" ]; then
        echo "SKIP: no debian/ for $name"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    hash="$(compute_source_hash "$name")"
    if cache_hit "$name" "$hash"; then
        echo "  Unchanged, reusing cached debs"
        SKIPPED=$((SKIPPED + 1))
        # Ensure deps available for subsequent packages
        dpkg -i "$DEB_REPO_DIR"/${name}*.deb "$DEB_REPO_DIR"/lib${name}*.deb 2>/dev/null || true
        continue
    fi

    before="$(mktemp)"
    ls "$DEB_REPO_DIR"/*.deb 2>/dev/null | xargs -r -n1 basename > "$before" || true

    work="$(prepare_build_tree "$name")"
    fetch_and_extract "$name" "$work"

    echo "  Building $name"
    (
        cd "$work"
        # Move built debs to BUILD_DIR parent for collection
        dpkg-buildpackage -us -uc -b -d || dpkg-buildpackage -us -uc -b
    ) && ok=1 || ok=0

    # Collect debs written next to workdir (dpkg-buildpackage default)
    shopt -s nullglob
    for deb in "$BUILD_DIR"/*.deb; do
        case "$(basename "$deb")" in
            *-dbgsym_*) rm -f "$deb"; continue ;;
        esac
        cp -f "$deb" "$DEB_REPO_DIR/"
        rm -f "$deb"
    done
    shopt -u nullglob

    if [ "$ok" -eq 1 ]; then
        mapfile -t new_debs < <(list_new_debs "$before")
        save_cache "$name" "$hash" "${new_debs[@]}"
        echo "  OK: ${new_debs[*]:-no new debs?}"
        BUILT=$((BUILT + 1))
        # Install for subsequent deps
        if [ "${#new_debs[@]}" -gt 0 ]; then
            (cd "$DEB_REPO_DIR" && dpkg -i "${new_debs[@]}" 2>/dev/null) || apt-get -f install -y || true
        fi
    else
        echo "  FAILED: $name"
        FAILED=$((FAILED + 1))
    fi
    rm -f "$before"
done

compose_apt_repo

echo ""
echo "=== Ubuntu deb build complete: built=$BUILT skipped=$SKIPPED failed=$FAILED ==="
[ "$FAILED" -eq 0 ]
