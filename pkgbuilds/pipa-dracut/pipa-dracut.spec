Name: pipa-dracut
Version: 1.1
Release: 4
Summary: Dracut modules for the Xiaomi Pad 6
Source1: module-setup.sh
Source2: pipa.conf
License: GPL2.0

Requires: xiaomi-pipa-firmware
Requires: dracut

%description
Dracut modules for the Xiaomi Pad 6

%install
install -Dm755 %{SOURCE1} %{buildroot}/usr/lib/dracut/modules.d/90pipafw/module-setup.sh
install -Dm644 %{SOURCE2} %{buildroot}/usr/lib/dracut/dracut.conf.d/10-pipa.conf

%files
/usr/lib/dracut/modules.d/90pipafw/*
/usr/lib/dracut/dracut.conf.d/10-pipa.conf
