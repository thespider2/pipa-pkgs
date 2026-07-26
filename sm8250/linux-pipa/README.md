# linux-pipa

Arch package for the Xiaomi Pad 6 kernel.

## Source

Builds [kernel.org](https://kernel.org) **7.1.4** with the device patches next to
this PKGBUILD, plus local `0017` which unifies CSOT/Tianma into a single
`sm8250-xiaomi-pipa.dtb` (CSOT panel/firmware) for packaging and the flasher.

Config: `config-xiaomi-pipa.aarch64`.

## USB-C DisplayPort

External displays over USB-C need all three of these together:

- `0018` retries the FSA4480 chip id read; the first I2C read fails on pipa, and
  the resulting `FSA4480 not found` left `pm8150b_typec` stuck in deferred probe.
- `0019` sets `&mdss_dp { status = "okay"; }`; the endpoints were already wired to
  the USB3/DP combo PHY but the controller stayed disabled, so no `DP-1` existed.
- `CONFIG_TYPEC_DP_ALTMODE=y` in the config, so the connector can negotiate the
  DisplayPort altmode.

After booting the new kernel, a plugged-in adapter should give a `DP-1` connector
in `/sys/class/drm/` and a port under `/sys/class/typec/`.

## Bump version

Refresh patches/config as needed, then bump `pkgver` here and in Ultramarine/Ubuntu.

## Build

```bash
makepkg -s
```
