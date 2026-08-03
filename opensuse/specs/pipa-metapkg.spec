Name:           pipa-metapkg
Version:        1.1
Release:        1%{?dist}
Summary:        Xiaomi Pad 6 support meta package for openSUSE
License:        MIT
BuildArch:      noarch

Source1:        90-pipa-gsk-renderer.sh
Source2:        pipa-pkgs.repo
Source3:        local-overrides.quirks

Requires:       kernel-pipa
Requires:       kernel-pipa-modules
Requires:       xiaomi-pipa-firmware
Requires:       kernel-firmware-qcom
Requires:       kernel-firmware-ath11k
Requires:       kernel-firmware-bluetooth
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
Recommends:     libinput10
Requires:       iio-sensor-proxy
Requires:       qrtr
Requires:       pd-mapper
Requires:       Mesa-dri
Requires:       wireless-regdb
Requires:       tuned
Recommends:     tqftpserv
Recommends:     rmtfs

%description
Meta package that pulls in all components needed for running
openSUSE Tumbleweed on the Xiaomi Pad 6 (pipa): custom kernel, firmware,
sensors, audio, camera, and boot configuration.

%install
install -Dm755 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/90-pipa-gsk-renderer.sh
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/zypp/repos.d/pipa-pkgs.repo
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/libinput/local-overrides.quirks

%files
%config(noreplace) %{_sysconfdir}/profile.d/90-pipa-gsk-renderer.sh
%config(noreplace) %{_sysconfdir}/zypp/repos.d/pipa-pkgs.repo
%{_datadir}/libinput/local-overrides.quirks

%changelog
* Mon Aug 03 2026 Ayman <ayman@pipa> - 1.1-1
- Initial openSUSE Tumbleweed meta package
