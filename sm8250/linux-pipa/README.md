# linux-pipa

Arch package for the Xiaomi Pad 6 kernel.

## Source

Builds [kernel.org](https://kernel.org) **7.1.4** with the device patches next to
this PKGBUILD, plus local `0017` which unifies CSOT/Tianma into a single
`sm8250-xiaomi-pipa.dtb` (CSOT panel/firmware) for packaging and the flasher.

Config: `config-xiaomi-pipa.aarch64`.

## Bump version

Refresh patches/config as needed, then bump `pkgver` here and in Ultramarine/Ubuntu.

## Build

```bash
makepkg -s
```
