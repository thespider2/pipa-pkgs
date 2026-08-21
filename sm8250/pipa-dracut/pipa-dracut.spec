Name: pipa-dracut
Version: 1.1
Release: 7
Summary: Dracut modules for the Xiaomi Pad 6
Source1: module-setup.sh
Source2: pipa.conf
Source3: pipa-refresh-initramfs
License: GPL2.0

Requires: xiaomi-pipa-firmware
Requires: dracut

%description
Dracut modules for the Xiaomi Pad 6

%install
install -Dm755 %{SOURCE1} %{buildroot}/usr/lib/dracut/modules.d/90pipafw/module-setup.sh
install -Dm644 %{SOURCE2} %{buildroot}/usr/lib/dracut/dracut.conf.d/10-pipa.conf
install -Dm755 %{SOURCE3} %{buildroot}/usr/local/bin/pipa-refresh-initramfs

%post
/usr/local/bin/pipa-refresh-initramfs >/dev/null 2>&1 || :

%files
/usr/lib/dracut/modules.d/90pipafw/*
/usr/lib/dracut/dracut.conf.d/10-pipa.conf
/usr/local/bin/pipa-refresh-initramfs
