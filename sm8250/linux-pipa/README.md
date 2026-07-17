# linux-pipa

Arch package for the Xiaomi Pad 6 kernel.

## Source

Builds [PipaDB/linux](https://github.com/PipaDB/linux) branch [`pipa/7.1`](https://github.com/PipaDB/linux/tree/pipa/7.1)
(Linux 7.1.0 + pipa DT/drivers). That tree already includes rear **OV13B10** and front **HI846** cameras, display, touch, audio, etc.

Config: `config-xiaomi-pipa.aarch64` (packaging overlay; `olddefconfig` against the tree).

## Bump commit

```bash
git ls-remote https://github.com/PipaDB/linux.git refs/heads/pipa/7.1
# edit _commit= in PKGBUILD
```

## Build

```bash
makepkg -s
```

Old vanilla `kernel.org` + patch series live under `archived-patches/` (not applied).
