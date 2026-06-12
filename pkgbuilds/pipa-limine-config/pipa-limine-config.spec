Name: pipa-limine-config
Version: 1.0
Release: 2
Summary: Limine config refresh helper for the Xiaomi Pad 6
License: MIT
Requires: limine
Source1: pipa-refresh-limine-config
Source2: 95-pipa-refresh-limine-config.hook

%description
Refreshes the Xiaomi Pad 6 Limine menu and keeps separate DTB entries available.

%install
install -Dm755 %{SOURCE1} %{buildroot}/usr/local/bin/pipa-refresh-limine-config
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/libalpm/hooks/95-pipa-refresh-limine-config.hook

%files
/usr/local/bin/pipa-refresh-limine-config
/usr/share/libalpm/hooks/95-pipa-refresh-limine-config.hook
