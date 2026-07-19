%global debug_package %{nil}

# PipaDB/linux branch pipa/7.1 (Linux 7.1.0 + pipa DT/drivers).
%global gitcommit e64607dc60963a05133304a8b682818ee4412106
%global kversion 7.1.0
%global krelease 2
%global kbuildver %(echo $((%{krelease} + 1))-pipa)

Name:           kernel-pipa
Version:        %{kversion}
Release:        %{krelease}%{?dist}
Summary:        Xiaomi Pad 6 kernel (PipaDB pipa/7.1)
License:        GPL-2.0-only
URL:            https://github.com/PipaDB/linux/tree/pipa/7.1
ExclusiveArch:  aarch64

Source0:        https://github.com/PipaDB/linux/archive/%{gitcommit}/linux-%{gitcommit}.tar.gz
Source1:        config-xiaomi-pipa.aarch64

# Camera bring-up aligned with Xiaomi Android DT (19.2 MHz MCLK) + SoftISP.
Patch0:         0001-clk-qcom-clk-rcg2-keep-force-enable-in-shared_enable.patch
Patch1:         0002-media-i2c-hi846-fix-power-on-reset-sequencing.patch
Patch2:         0003-media-i2c-hi846-retry-MCLK-enable-and-accept-19.2MHz.patch
Patch3:         0004-media-i2c-ov13b10-retry-MCLK-enable-and-set-19.2MHz-.patch
Patch4:         0005-arm64-dts-qcom-pipa-fix-OV13B10-rear-camera-clocks-a.patch
Patch5:         0006-arm64-dts-qcom-pipa-fix-HI846-front-camera-clocks-an.patch
Patch6:         0007-media-qcom-camss-fix-video-pipeline-stop-streaming.patch
Patch7:         0008-media-i2c-ov13b10-add-get_selection-pad-operation.patch

BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  clang
BuildRequires:  cpio
BuildRequires:  dwarves
BuildRequires:  elfutils-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  hostname
BuildRequires:  kmod
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  perl-interpreter
BuildRequires:  python3
BuildRequires:  rsync
BuildRequires:  tar
BuildRequires:  xz

Requires:       dracut
Requires:       kmod
Requires:       xiaomi-pipa-firmware
Provides:       kernel = %{kversion}
Obsoletes:      kernel-pipa < %{version}-%{release}

%description
Linux %{kversion} from PipaDB/linux branch pipa/7.1 for the Xiaomi Pad 6
(SM8250 / pipa). Includes rear OV13B10 and front HI846 camera support (DT + SoftISP bring-up patches).

%package headers
Summary:        Header files for kernel-pipa
Provides:       kernel-headers = %{kversion}
Obsoletes:      kernel-pipa-headers < %{version}-%{release}

%description headers
Kernel header files for building out-of-tree modules against kernel-pipa.

%package modules
Summary:        Kernel modules for kernel-pipa
Requires:       kernel-pipa = %{version}-%{release}
Provides:       kernel-modules = %{kversion}
Obsoletes:      kernel-pipa-modules < %{version}-%{release}

%description modules
Loadable kernel modules for kernel-pipa.

%prep
%setup -q -n linux-%{gitcommit}
%autopatch -p1
cp %{SOURCE1} .config
./scripts/config --file .config -d LOCALVERSION_AUTO
./scripts/config --file .config --set-str LOCALVERSION "-pipa"
make ARCH=arm64 LLVM=1 olddefconfig

%build
unset LDFLAGS
make ARCH=arm64 LLVM=1 KBUILD_BUILD_VERSION=%{kbuildver} \
    %{?_smp_mflags} Image Image.gz modules dtbs

%install
KernelVer=$(make ARCH=arm64 LLVM=1 KBUILD_BUILD_VERSION=%{kbuildver} -s kernelrelease)

make ARCH=arm64 LLVM=1 KBUILD_BUILD_VERSION=%{kbuildver} \
    INSTALL_MOD_PATH=%{buildroot}/usr \
    INSTALL_MOD_STRIP=1 \
    modules_install

rm -f %{buildroot}/usr/lib/modules/*/build %{buildroot}/usr/lib/modules/*/source

install -Dm644 arch/arm64/boot/Image.gz %{buildroot}/boot/vmlinuz-${KernelVer}
install -Dm644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-${KernelVer}.uncompressed
install -Dm644 arch/arm64/boot/Image.gz %{buildroot}/boot/Image.gz
install -Dm644 arch/arm64/boot/Image %{buildroot}/boot/Image
install -Dm644 System.map %{buildroot}/boot/System.map-${KernelVer}
install -Dm644 .config %{buildroot}/boot/config-${KernelVer}
install -Dm644 arch/arm64/boot/dts/qcom/sm8250-xiaomi-pipa.dtb \
    %{buildroot}/boot/dtbs/qcom/sm8250-xiaomi-pipa.dtb

ModDir=%{buildroot}/usr/lib/modules/${KernelVer}
install -d ${ModDir}/devicetree
cp arch/arm64/boot/dts/qcom/sm8250-xiaomi-pipa.dtb ${ModDir}/devicetree/
ln -s devicetree ${ModDir}/dtb
cp arch/arm64/boot/Image.gz ${ModDir}/vmlinuz
cp arch/arm64/boot/Image    ${ModDir}/vmlinuz.uncompressed

install -Dm644 include/config/kernel.release \
    %{buildroot}/usr/share/kernel/xiaomi-pipa/kernel.release

make ARCH=arm64 LLVM=1 KBUILD_BUILD_VERSION=%{kbuildver} \
    INSTALL_HDR_PATH=%{buildroot}/usr headers_install
find %{buildroot}/usr/include -name '.*' -delete

%files
%license COPYING
/boot/vmlinuz-*
/boot/Image*
/boot/System.map-*
/boot/config-*
/boot/dtbs/
/usr/share/kernel/xiaomi-pipa/kernel.release

%files modules
/usr/lib/modules/

%files headers
/usr/include/

%changelog
* Sun Jul 19 2026 Ayman <ayman@pipa> - 7.1.0-2
- Camera bring-up patches: CAMCC MCLK force-enable, HI846/OV13B10 power
  and MCLK retries, DTS assigned-clocks @ 19.2MHz + pinctrl (Android DT),
  camss stop-streaming and ov13b10 get_selection for SoftISP

* Fri Jul 17 2026 Ayman <ayman@pipa> - 7.1.0-1
- Switch source to PipaDB/linux pipa/7.1 (commit e64607dc6096)
- Drop vanilla kernel.org patch series (integrated in that tree)

* Thu Jul 16 2026 Ayman <ayman@pipa> - 7.1.3-2
- HACK: ignore spurious AFE clock set_param errors so va_macro can probe
- Drop Conflicts: kernel so dnf can upgrade between kernel-pipa releases
- Obsolete older kernel-pipa releases so dnf can upgrade cleanly

* Wed Jul 15 2026 Ayman <ayman@pipa> - 7.1.3-1
- upstream 7.1.3
