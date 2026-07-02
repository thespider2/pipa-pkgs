Name: pipa-sound-conf
Version: 1.4
Release: 7
Summary: Sound settings for Xiaomi Mi Pad 6 (pipa)
Source1: 51-pipa.conf
Source2: pipa-audio-init
Source3: pipa-audio-init.service
License: Unknown
BuildArch: noarch
Provides: alsa-ucm-conf-xiaomi-pipa = %{version}-%{release}
Obsoletes: alsa-ucm-conf-xiaomi-pipa < %{version}-%{release}

Requires: alsa-ucm-conf-sm8250
Requires: alsa-utils
Requires: wireplumber

%description
Wireplumber configuration for Xiaomi Mi Pad 6 (pipa)

%install
install -Dm644 "%{SOURCE1}" "%{buildroot}/usr/share/wireplumber/wireplumber.conf.d/51-pipa.conf"
install -Dm755 "%{SOURCE2}" "%{buildroot}/usr/local/bin/pipa-audio-init"
install -Dm644 "%{SOURCE3}" "%{buildroot}/usr/lib/systemd/system/pipa-audio-init.service"

%post
systemctl daemon-reload >/dev/null 2>&1 || :
systemctl enable pipa-audio-init.service >/dev/null 2>&1 || :
systemctl start pipa-audio-init.service >/dev/null 2>&1 || :

%files
/usr/share/wireplumber/wireplumber.conf.d/51-pipa.conf
/usr/local/bin/pipa-audio-init
/usr/lib/systemd/system/pipa-audio-init.service
