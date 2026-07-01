Name: pipa-sensors
Version: 1.2
Release: 16
Summary: Sensors configs for the Xiaomi Pad 6
Source1: 81-libssc-xiaomi-pipa.rules
Source2: hexagonrpcd-sdsp.conf
Source3: pipa-prepare-sensor-persist
Source4: pipa-sensors-persist.service
Source5: pipa-sensors-resume
Source6: iio-sensor-proxy-pipa-audio.conf
Source7: pipa-audio-init-sensors.conf
Source8: pipa-sensors.tmpfiles
License: MIT

Requires: xiaomi-pipa-firmware
Requires: iio-sensor-proxy
Requires: hexagonrpc

%description
Sensors configs for the Xiaomi Pad 6

%install
install -Dm644 %{SOURCE1} %{buildroot}/usr/lib/udev/rules.d/81-libssc-xiaomi-pipa.rules
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/hexagonrpcd/hexagonrpcd-sdsp.conf
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/hexagonrpcd/hexagonrpcd-adsp-rootpd.conf
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/hexagonrpcd/hexagonrpcd-adsp-sensorspd.conf
install -Dm755 %{SOURCE3} %{buildroot}/usr/local/bin/pipa-prepare-sensor-persist
install -Dm644 %{SOURCE4} %{buildroot}/usr/lib/systemd/system/pipa-sensors-persist.service
install -Dm755 %{SOURCE5} %{buildroot}/usr/lib/systemd/system-sleep/pipa-sensors-resume
install -Dm644 %{SOURCE6} %{buildroot}/usr/lib/systemd/system/iio-sensor-proxy.service.d/10-pipa-audio.conf
install -Dm644 %{SOURCE7} %{buildroot}/usr/lib/systemd/system/pipa-audio-init.service.d/10-sensors.conf
install -Dm644 %{SOURCE8} %{buildroot}/usr/lib/tmpfiles.d/pipa-sensors.conf

%post
systemd-tmpfiles --create %{_tmpfilesdir}/pipa-sensors.conf >/dev/null 2>&1 || :
/usr/local/bin/pipa-prepare-sensor-persist >/dev/null 2>&1 || :

%files
/usr/lib/udev/rules.d/81-libssc-xiaomi-pipa.rules
/usr/share/hexagonrpcd/hexagonrpcd-sdsp.conf
/usr/share/hexagonrpcd/hexagonrpcd-adsp-rootpd.conf
/usr/share/hexagonrpcd/hexagonrpcd-adsp-sensorspd.conf
/usr/local/bin/pipa-prepare-sensor-persist
/usr/lib/systemd/system/pipa-sensors-persist.service
/usr/lib/systemd/system-sleep/pipa-sensors-resume
/usr/lib/systemd/system/iio-sensor-proxy.service.d/10-pipa-audio.conf
/usr/lib/systemd/system/pipa-audio-init.service.d/10-sensors.conf
/usr/lib/tmpfiles.d/pipa-sensors.conf
