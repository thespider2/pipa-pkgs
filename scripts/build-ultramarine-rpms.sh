#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UM_DIR="$ROOT_DIR/ultramarine"
SPECS_DIR="$UM_DIR/specs"
RPM_REPO_DIR="$ROOT_DIR/repo/ultramarine"
SOURCES_DIR="$UM_DIR/.sources"
CACHE_DIR="$UM_DIR/.build-cache"
CACHE_RPM_DIR="$CACHE_DIR/rpms"

mkdir -p "$RPM_REPO_DIR" "$SOURCES_DIR" "$CACHE_DIR" "$CACHE_RPM_DIR"
rpmdev-setuptree 2>/dev/null || true

link_files() {
    local dest="$1"; shift
    mkdir -p "$dest"
    for src in "$@"; do
        [ -e "$src" ] && cp "$src" "$dest/" || echo "WARNING: $src not found"
    done
}

compute_source_hash() {
    local name="$1"
    local spec="$SPECS_DIR/$name.spec"
    local src_dir="$SOURCES_DIR/$name"

    python3 - "$spec" "$src_dir" <<'PY'
import hashlib, pathlib, sys

digest = hashlib.sha256()

spec = pathlib.Path(sys.argv[1])
if spec.is_file():
    digest.update(b"spec\0")
    digest.update(spec.read_bytes())
    digest.update(b"\0")

src_dir = pathlib.Path(sys.argv[2])
if src_dir.is_dir():
    for path in sorted(src_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = str(path.relative_to(src_dir))
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")

print(digest.hexdigest())
PY
}

stage_cached_rpm() {
    local rpm_name="$1"
    if [ -f "$RPM_REPO_DIR/$rpm_name" ]; then
        return 0
    fi
    if [ -f "$CACHE_RPM_DIR/$rpm_name" ]; then
        cp -f "$CACHE_RPM_DIR/$rpm_name" "$RPM_REPO_DIR/$rpm_name"
        return 0
    fi
    return 1
}

publish_rpms() {
    local rpm_name
    for rpm_name in "$@"; do
        [ -f "$RPM_REPO_DIR/$rpm_name" ] || continue
        cp -f "$RPM_REPO_DIR/$rpm_name" "$CACHE_RPM_DIR/$rpm_name"
    done
}

remove_cached_rpms() {
    local rpm_name
    for rpm_name in "$@"; do
        rm -f "$RPM_REPO_DIR/$rpm_name" "$CACHE_RPM_DIR/$rpm_name"
    done
}

is_installable_rpm() {
    case "$1" in
        *-debuginfo-*|*-debugsource-*|*.src.rpm) return 1 ;;
        *) return 0 ;;
    esac
}

restore_all_cached_to_repo() {
    shopt -s nullglob
    for rpm_file in "$CACHE_RPM_DIR"/*.rpm; do
        cp -fn "$rpm_file" "$RPM_REPO_DIR/$(basename "$rpm_file")"
    done
    shopt -u nullglob
}

package_present_in_repo() {
    local pkg="$1"
    local candidate
    shopt -s nullglob
    for candidate in "$RPM_REPO_DIR/$pkg"-*.aarch64.rpm "$RPM_REPO_DIR/$pkg"-*.noarch.rpm; do
        if is_installable_rpm "$(basename "$candidate")"; then
            shopt -u nullglob
            return 0
        fi
    done
    shopt -u nullglob
    return 1
}

echo "=== Gathering sources from pipa-pkgs ==="

link_files "$SOURCES_DIR/kernel-pipa" \
    "$ROOT_DIR/sm8250/linux-pipa/pipa.config" \
    "$ROOT_DIR/sm8250/linux-pipa/"0*.patch

link_files "$SOURCES_DIR/xiaomi-pipa-firmware" \
    "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/awinic_firmware.files" \
    "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/dsp_firmware.files" \
    "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/qcom_firmware.files" \
    "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/novatek_firmware.files" \
    "$ROOT_DIR/sm8250/xiaomi-pipa-firmware/nuvolta_firmware.files"

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

link_files "$SOURCES_DIR/pipa-dracut" \
    "$ROOT_DIR/sm8250/pipa-dracut/module-setup.sh" \
    "$ROOT_DIR/sm8250/pipa-dracut/pipa.conf" \
    "$ROOT_DIR/sm8250/pipa-dracut/pipa-refresh-initramfs"

link_files "$SOURCES_DIR/pipa-grub-config" \
    "$ROOT_DIR/sm8250/pipa-grub-config/pipa-refresh-grub-config"

link_files "$SOURCES_DIR/pipa-metapkg" \
    "$ROOT_DIR/sm8250/pipa-metapkg/90-pipa-gsk-renderer.sh"

link_files "$SOURCES_DIR/hexagonrpc" \
    "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-adsp-rootpd.service" \
    "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-adsp-sensorspd.service" \
    "$ROOT_DIR/common/hexagonrpc/hexagonrpcd-sdsp.service" \
    "$ROOT_DIR/common/hexagonrpc/sysusers.conf" \
    "$ROOT_DIR/common/hexagonrpc/10-fastrpc.rules"

link_files "$SOURCES_DIR/libssc" \
    "$ROOT_DIR/common/libssc/"0*.patch

link_files "$SOURCES_DIR/iio-sensor-proxy" \
    "$ROOT_DIR/common/iio-sensor-proxy/"0*.patch

link_files "$SOURCES_DIR/libcamera" \
    "$ROOT_DIR/common/libcamera/"0*.patch \
    "$ROOT_DIR/common/libcamera/hi846.yaml" \
    "$ROOT_DIR/common/libcamera/ov13b10.yaml"

echo "=== Building RPMs ==="
restore_all_cached_to_repo
BUILT=0
SKIPPED=0
FAILED=0

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
    kernel-pipa
    pipa-metapkg
)

for name in "${BUILD_ORDER[@]}"; do
    spec="$SPECS_DIR/$name.spec"
    [ -f "$spec" ] || { echo "SKIP: $spec not found"; continue; }

    echo ""
    echo "--- $name ---"

    source_hash="$(compute_source_hash "$name")"
    cache_file="$CACHE_DIR/$name"

    if [ -f "$cache_file" ]; then
        mapfile -t cache_lines < "$cache_file"
        if [ "${#cache_lines[@]}" -gt 1 ] && [ "${cache_lines[0]}" = "$source_hash" ]; then
            cache_hit=1
            has_installable=0
            for rpm_name in "${cache_lines[@]:1}"; do
                if ! stage_cached_rpm "$rpm_name"; then
                    cache_hit=0
                    break
                fi
                if is_installable_rpm "$rpm_name"; then
                    has_installable=1
                fi
            done
            if [ "$cache_hit" -eq 1 ] && [ "$has_installable" -eq 0 ]; then
                cache_hit=0
            fi
            if [ "$cache_hit" -eq 1 ]; then
                echo "  Unchanged, reusing cached RPMs"
                # Install cached RPMs so later packages can depend on them
                cached_rpms=()
                for rpm_name in "${cache_lines[@]:1}"; do
                    case "$rpm_name" in
                        *-debuginfo-*|*-debugsource-*|*.src.rpm) ;;
                        *) cached_rpms+=("$RPM_REPO_DIR/$rpm_name") ;;
                    esac
                done
                if [ ${#cached_rpms[@]} -gt 0 ]; then
                    dnf install -y --nogpgcheck "${cached_rpms[@]}" 2>/dev/null || true
                fi
                publish_rpms "${cache_lines[@]:1}"
                SKIPPED=$((SKIPPED + 1))
                continue
            fi
        fi
    fi

    echo "  Building..."

    rm -rf ~/rpmbuild/SOURCES/*
    cp "$SOURCES_DIR/$name"/* ~/rpmbuild/SOURCES/ 2>/dev/null || true

    echo "  Downloading sources..."
    spectool -g -R --define "_topdir $HOME/rpmbuild" "$spec" || \
        echo "  WARNING: spectool failed for $name, sources may be missing"

    echo "  Running rpmbuild..."
    BUILD_LOG="/tmp/rpmbuild-$name.log"
    set +e
    rpmbuild -ba "$spec" \
        --define "_topdir $HOME/rpmbuild" \
        --define "dist .um44" \
        --target "$(uname -m)" 2>&1 | tee "$BUILD_LOG"
    BUILD_RC=${PIPESTATUS[0]}
    set -e
    if [ "$BUILD_RC" -eq 0 ]; then
        # Remove old cached RPMs for this package
        if [ -f "$cache_file" ]; then
            mapfile -t old_cache_lines < "$cache_file"
            remove_cached_rpms "${old_cache_lines[@]:1}"
        fi

        # Collect newly built RPMs from rpmbuild output
        built_rpms=()
        while IFS= read -r rpm_path; do
            [ -n "$rpm_path" ] || continue
            rpm_basename="$(basename "$rpm_path")"
            cp -f "$rpm_path" "$RPM_REPO_DIR/$rpm_basename"
            cp -f "$rpm_path" "$CACHE_RPM_DIR/$rpm_basename"
            built_rpms+=("$rpm_basename")
        done < <(grep '^Wrote:' "$BUILD_LOG" | sed 's|^Wrote: ||')

        if [ ${#built_rpms[@]} -eq 0 ]; then
            echo "ERROR: rpmbuild succeeded for $name but no RPM artifacts were collected" >&2
            FAILED=$((FAILED + 1))
            continue
        fi

        # Write cache
        {
            printf '%s\n' "$source_hash"
            printf '%s\n' "${built_rpms[@]}"
        } > "$cache_file"

        # Install built RPMs so later packages can depend on them
        install_rpms=()
        for rpm_name in "${built_rpms[@]}"; do
            case "$rpm_name" in
                *-debuginfo-*|*-debugsource-*|*.src.rpm) ;;
                *) install_rpms+=("$RPM_REPO_DIR/$rpm_name") ;;
            esac
        done
        if [ ${#install_rpms[@]} -gt 0 ]; then
            dnf install -y --nogpgcheck "${install_rpms[@]}" 2>/dev/null || true
        fi

        BUILT=$((BUILT + 1))
    else
        echo ""
        echo "========================================="
        echo "FAILED: $name"
        echo "========================================="
        tail -30 "$BUILD_LOG" 2>/dev/null
        echo "========================================="
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "=== Creating RPM repo metadata ==="
restore_all_cached_to_repo
createrepo_c --update "$RPM_REPO_DIR"

echo ""
echo "=== Done: $BUILT built, $SKIPPED cached, $FAILED failed ==="
ls -lh "$RPM_REPO_DIR/"*.rpm 2>/dev/null | wc -l
echo "RPM packages in repo"

if [ "$FAILED" -gt 0 ]; then
    echo "ERROR: $FAILED RPM build(s) failed; refusing to publish incomplete repo" >&2
    exit 1
fi

missing_pkgs=()
for pkg in bootmac swclock-offset hexagonrpc xiaomi-pipa-firmware pipa-dracut \
    pipa-grub-config libssc iio-sensor-proxy pipa-sensors pipa-sound-conf \
    libcamera kernel-pipa pipa-metapkg; do
    if ! package_present_in_repo "$pkg"; then
        missing_pkgs+=("$pkg")
    fi
done

if [ ${#missing_pkgs[@]} -gt 0 ]; then
    echo "ERROR: Missing required RPMs in $RPM_REPO_DIR: ${missing_pkgs[*]}" >&2
    exit 1
fi
