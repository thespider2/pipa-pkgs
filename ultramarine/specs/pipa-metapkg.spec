Name:           pipa-metapkg
Version:        1.1
Release:        5%{?dist}
Summary:        Xiaomi Pad 6 support meta package for Ultramarine OS
License:        MIT
BuildArch:      noarch

Source1:        90-pipa-gsk-renderer.sh
Source2:        pipa-pkgs.repo
Source3:        local-overrides.quirks

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
Recommends:     libinput
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
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/libinput/local-overrides.quirks

%files
%config(noreplace) %{_sysconfdir}/profile.d/90-pipa-gsk-renderer.sh
%config(noreplace) %{_sysconfdir}/yum.repos.d/pipa-pkgs.repo
%{_datadir}/libinput/local-overrides.quirks

%changelog
* Thu Jul 30 2026 Ayman <ayman@pipa> - 1.1-5
- Ship libinput quirks for Nanosic keyboard cover (pmaports a3236185)

* Sun Jul 05 2026 Ayman <ayman@pipa> - 1.1-4
- Ship pipa-pkgs DNF repo file for OTA updates

* Sun Jul 05 2026 Ayman <ayman@pipa> - 1.1-3
- Pull in Fedora linux-firmware GPU and ath11k subpackages

* Sat Jul 04 2026 Ayman <ayman@pipa> - 1.1-2
- Change gstreamer1-plugin-libcamera from Requires to Recommends

* Fri Jul 03 2026 Ayman <ayman@pipa> - 1.1-1
- Initial Ultramarine OS meta package
