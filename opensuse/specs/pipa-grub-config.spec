Name:           pipa-grub-config
Version:        1.0
Release:        6%{?dist}
Summary:        GRUB config refresh helper for the Xiaomi Pad 6
License:        MIT
BuildArch:      noarch

Source1:        pipa-refresh-grub-config

BuildRequires:  systemd-rpm-macros

Requires:       bash
Requires:       coreutils
Requires:       util-linux
Requires:       grub2-arm64-efi

%description
Refreshes the Xiaomi Pad 6 GRUB menu and keeps the DTB entry as default.
On Fedora/Ultramarine, a kernel-install plugin triggers the refresh
automatically on kernel upgrades.

%install
install -Dm755 %{SOURCE1} %{buildroot}/usr/local/bin/pipa-refresh-grub-config
install -d %{buildroot}/usr/lib/kernel/install.d
cat > %{buildroot}/usr/lib/kernel/install.d/95-pipa-grub.install <<'SCRIPT'
#!/bin/bash
COMMAND="$1"
case "$COMMAND" in
    add|remove)
        /usr/local/bin/pipa-refresh-grub-config >/dev/null 2>&1 || :
        ;;
esac
SCRIPT
chmod 755 %{buildroot}/usr/lib/kernel/install.d/95-pipa-grub.install

%post
/usr/local/bin/pipa-refresh-grub-config >/dev/null 2>&1 || :

%files
/usr/local/bin/pipa-refresh-grub-config
/usr/lib/kernel/install.d/95-pipa-grub.install

%changelog
* Fri Aug 21 2026 Ayman <ayman@pipa> - 1.0-6
- Prefer linux-pipa Image over stock openSUSE Image-*-default symlink

* Sat Jul 04 2026 Ayman <ayman@pipa> - 1.0-5
- Use --- before kernel cmdline so GRUB does not parse root= as netboot

* Sat Jul 04 2026 Ayman <ayman@pipa> - 1.0-4
- GRUB menu: linux, initrd, then devicetree (required on aarch64 EFI)

* Fri Jul 03 2026 Ayman <ayman@pipa> - 1.0-3
- Replace libalpm hook with kernel-install plugin for Fedora
