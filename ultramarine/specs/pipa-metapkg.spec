Name:           pipa-metapkg
Version:        1.1
Release:        4%{?dist}
Summary:        Xiaomi Pad 6 support meta package for Ultramarine OS
License:        MIT
BuildArch:      noarch

Source1:        90-pipa-gsk-renderer.sh
Source2:        pipa-pkgs.repo

Requires:       kernel-pipa
Requires:       kernel-pipa-modules
Requires:       xiaomi-pipa-firmware
Requires:       linux-firmware
Requires:       qcom-firmware
Requires:       atheros-firmware
Requires:       pipa-dracut
Requires:       pipa-grub-config
Requires:       pipa-sound-conf
Requires:       pipa-sensors
Requires:       swclock-offset
Requires:       bootmac
Requires:       hexagonrpc
Requires:       libssc
Requires:       libcamera
Requires:       libcamera-ipa
Requires:       libcamera-tools
Recommends:     gstreamer1-plugin-libcamera
Requires:       iio-sensor-proxy
Requires:       qrtr
Requires:       tqftpserv
Requires:       pd-mapper
Requires:       mesa-dri-drivers
Requires:       wireless-regdb
Requires:       tuned
Requires:       tuned-ppd

%description
Meta package that pulls in all components needed for running
Ultramarine OS on the Xiaomi Pad 6 (pipa): custom kernel, firmware,
sensors, audio, camera, and boot configuration.

%install
install -Dm755 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/90-pipa-gsk-renderer.sh
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/yum.repos.d/pipa-pkgs.repo

%files
%config(noreplace) %{_sysconfdir}/profile.d/90-pipa-gsk-renderer.sh
%config(noreplace) %{_sysconfdir}/yum.repos.d/pipa-pkgs.repo

%changelog
* Sun Jul 05 2026 Ayman <ayman@pipa> - 1.1-4
- Ship pipa-pkgs DNF repo file for OTA updates

* Sun Jul 05 2026 Ayman <ayman@pipa> - 1.1-3
- Pull in Fedora linux-firmware GPU and ath11k subpackages

* Sat Jul 04 2026 Ayman <ayman@pipa> - 1.1-2
- Change gstreamer1-plugin-libcamera from Requires to Recommends

* Fri Jul 03 2026 Ayman <ayman@pipa> - 1.1-1
- Initial Ultramarine OS meta package
