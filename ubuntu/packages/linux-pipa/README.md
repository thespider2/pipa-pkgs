# linux-pipa (Ubuntu/Debian)

Source tree: clone [PipaDB/linux](https://github.com/PipaDB/linux) branch `pipa/7.1`
(pinned commit in Arch `PKGBUILD` `_commit`), then build with this `debian/` overlay:

```bash
git clone https://github.com/PipaDB/linux.git -b pipa/7.1 linux-pipa
cd linux-pipa
git checkout e64607dc60963a05133304a8b682818ee4412106
cp -a /path/to/pipa-pkgs/ubuntu/packages/linux-pipa/debian .
dpkg-buildpackage -b -uc -us -aarm64
```

Config lives in `debian/extras/config-xiaomi-pipa.aarch64` (same as Arch package).
