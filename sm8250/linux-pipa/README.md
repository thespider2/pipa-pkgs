# linux-pipa

Arch package for the Xiaomi Pad 6 kernel.

## Source

Builds [PAD6-DEV/linux-7.xx](https://github.com/PAD6-DEV/linux-7.xx) branch
`pipa/7.1.7-Stable` (pinned commit `f6344729eb71`) with pipa config plus local
patches: duplicate `cpu7_opp21` DTB label fix and `linux/hex.h` include for
nanosic_803 (`hex_to_bin` on 7.1.x).

Former AFE audio hacks (`0011`–`0012`, `0020`) live under `archived-patches/`.
Speakers may need them restored if stock PAD6 audio is insufficient.

Device tree, DisplayPort, FSA4480 chip-id retries, touch, wireless charger, and
the rest of the former kernel.org 7.1.4 patch series are integrated upstream of
this branch.

Config: `config-xiaomi-pipa.aarch64`.

## Bump version

Refresh `_commit` with `git ls-remote`, update config if needed, then bump
`pkgver` here and in Ultramarine/Ubuntu/openSUSE specs.

## Build

```bash
makepkg -s
```
