Name: swclock-offset
Version: 0.3.0
Release: 1
Summary: Keep system time at an offset to a non-writable RTC
License: GPL-3.0-or-later
BuildArch: noarch
Source0: https://gitlab.postmarketos.org/postmarketOS/swclock-offset/-/archive/%{version}/swclock-offset-%{version}.tar.gz

Requires: systemd

%description
Keep system time at an offset to a non-writable RTC

%prep
%autosetup -n %{name}-%{version}

%build
sed -e 's+STORAGE_PATH+/var/cache+g' "src/%{name}-boot.sh.in" > "src/%{name}-boot.sh"
sed -e 's+STORAGE_PATH+/var/cache+g' "src/%{name}-shutdown.sh.in" > "src/%{name}-shutdown.sh"
sed -e 's+SWCLOCK_PATH+/usr/bin+g' "systemd/%{name}-boot.service.in" > "systemd/%{name}-boot.service"
sed -e 's+SWCLOCK_PATH+/usr/bin+g' "systemd/%{name}-shutdown.service.in" > "systemd/%{name}-shutdown.service"

%install
install -Dm755 "src/%{name}-boot.sh" "%{buildroot}/usr/bin/%{name}-boot"
install -Dm755 "src/%{name}-shutdown.sh" "%{buildroot}/usr/bin/%{name}-shutdown"
install -Dm644 "systemd/%{name}.target" "%{buildroot}/usr/lib/systemd/system/%{name}.target"
install -Dm644 "systemd/%{name}-boot.service" "%{buildroot}/usr/lib/systemd/system/%{name}-boot.service"
install -Dm644 "systemd/%{name}-shutdown.service" "%{buildroot}/usr/lib/systemd/system/%{name}-shutdown.service"

%post
systemctl daemon-reload >/dev/null 2>&1 || :
systemctl enable swclock-offset-boot.service >/dev/null 2>&1 || :
systemctl enable swclock-offset-shutdown.service >/dev/null 2>&1 || :

%preun
if [ "$1" -eq 0 ]; then
  systemctl disable --now swclock-offset-boot.service >/dev/null 2>&1 || :
  systemctl disable --now swclock-offset-shutdown.service >/dev/null 2>&1 || :
fi

%postun
if [ "$1" -eq 0 ]; then
  rm -f /var/cache/swclock-offset/offset-storage >/dev/null 2>&1 || :
  rmdir /var/cache/swclock-offset >/dev/null 2>&1 || :
fi
systemctl daemon-reload >/dev/null 2>&1 || :

%files
/usr/bin/swclock-offset-boot
/usr/bin/swclock-offset-shutdown
/usr/lib/systemd/system/swclock-offset.target
/usr/lib/systemd/system/swclock-offset-boot.service
/usr/lib/systemd/system/swclock-offset-shutdown.service
