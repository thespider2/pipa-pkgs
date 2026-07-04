Name:           alsa-ucm-conf-sm8250
Version:        1.0
Release:        2%{?dist}
Summary:        ALSA Use Case Manager configuration for sm8250/Xiaomi Pad 6
License:        MIT
BuildArch:      noarch

Source1:        Xiaomi Pad 6.conf
Source2:        HiFi_pipa.conf

Requires:       alsa-ucm-conf

%description
ALSA UCM profiles for the Qualcomm sm8250 platform used on the Xiaomi Pad 6 (pipa).

%install
install -d %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8250
install -d %{buildroot}/usr/share/alsa/ucm2/Qualcomm/sm8250
install -Dm644 %{SOURCE1} %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8250/Xiaomi\ Pad\ 6.conf
install -Dm644 %{SOURCE2} %{buildroot}/usr/share/alsa/ucm2/Qualcomm/sm8250/HiFi_pipa.conf
ln -sf "Xiaomi Pad 6.conf" %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8250/sm8250.conf
ln -sf "Xiaomi Pad 6.conf" %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8250/Xiaomi-Pad6-pipa-M82.conf

%files
/usr/share/alsa/ucm2/conf.d/sm8250/Xiaomi Pad 6.conf
/usr/share/alsa/ucm2/conf.d/sm8250/sm8250.conf
/usr/share/alsa/ucm2/conf.d/sm8250/Xiaomi-Pad6-pipa-M82.conf
/usr/share/alsa/ucm2/Qualcomm/sm8250/HiFi_pipa.conf

%changelog
* Sat Jul 04 2026 Ayman <ayman@pipa> - 1.0-2
- Initial Ultramarine OS package
