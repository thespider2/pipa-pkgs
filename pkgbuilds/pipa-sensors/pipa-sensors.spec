Name: pipa-sensors
Version: 1.2
Release: 10
Summary: Sensors configs for the Xiaomi Pad 6
Source1: 81-libssc-xiaomi-pipa.rules
Source2: hexagonrpcd-sdsp.conf
Source4: pipa-sensors-resume
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
install -Dm755 %{SOURCE4} %{buildroot}/usr/lib/systemd/system-sleep/pipa-sensors-resume

%files
/usr/lib/udev/rules.d/81-libssc-xiaomi-pipa.rules
/usr/share/hexagonrpcd/hexagonrpcd-sdsp.conf
/usr/share/hexagonrpcd/hexagonrpcd-adsp-rootpd.conf
/usr/share/hexagonrpcd/hexagonrpcd-adsp-sensorspd.conf
/usr/lib/systemd/system-sleep/pipa-sensors-resume
