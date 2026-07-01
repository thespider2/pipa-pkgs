Name: pipa-grub-config
Version: 1.0
Release: 3
Summary: GRUB config refresh helper for the Xiaomi Pad 6
License: MIT
Source1: pipa-refresh-grub-config
Source2: 95-pipa-refresh-grub-config.hook
Requires: bash
Requires: coreutils
Requires: util-linux
%description
Refreshes the Xiaomi Pad 6 GRUB menu and keeps the separate DTB entry as default.

%install
install -Dm755 %{SOURCE1} %{buildroot}/usr/local/bin/pipa-refresh-grub-config
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/libalpm/hooks/95-pipa-refresh-grub-config.hook

%files
/usr/local/bin/pipa-refresh-grub-config
/usr/share/libalpm/hooks/95-pipa-refresh-grub-config.hook
