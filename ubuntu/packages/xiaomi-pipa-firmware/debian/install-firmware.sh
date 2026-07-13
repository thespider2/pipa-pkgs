#!/bin/bash
set -euo pipefail

DEST="${CURDIR:-.}/debian/xiaomi-pipa-firmware"
FW="$DEST/usr/lib/firmware"
EXTRAS="debian/extras"

SRC="$(find . -maxdepth 1 -type d -name 'xiaomi-pipa-firmware-*' | head -1)"
[ -n "$SRC" ] || { echo "firmware source tree not found"; exit 1; }

cd "$SRC"

for firmware in $(cat "../$EXTRAS/awinic_firmware.files"); do
    install -Dm644 "$firmware" "$FW/awinic/$(basename "$firmware")"
done

for firmware in $(cat "../$EXTRAS/dsp_firmware.files"); do
    install -Dm644 "$firmware" "$DEST/$firmware"
done

for firmware in $(cat "../$EXTRAS/qcom_firmware.files"); do
    install -Dm644 "$firmware" "$FW/qcom/sm8250/xiaomi/pipa/$(basename "$firmware")"
done

for firmware in $(cat "../$EXTRAS/novatek_firmware.files"); do
    install -Dm644 "$firmware" "$FW/novatek/$(basename "$firmware")"
done

for firmware in $(cat "../$EXTRAS/nuvolta_firmware.files"); do
    install -Dm644 "$firmware" "$FW/nuvolta/$(basename "$firmware")"
done
