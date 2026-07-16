%global debug_package %{nil}

%global kversion 7.1.3
%global krelease 2
%global kbuildver %(echo $((%{krelease} + 1))-pipa)
%global kmajor %(echo %{kversion} | cut -d. -f1)

Name:           kernel-pipa
Version:        %{kversion}
Release:        %{krelease}%{?dist}
Summary:        Stable kernel for Xiaomi Pad 6
License:        GPL-2.0-only
URL:            https://kernel.org
ExclusiveArch:  aarch64

Source0:        https://cdn.kernel.org/pub/linux/kernel/v%{kmajor}.x/linux-%{kversion}.tar.xz
Source1:        config-xiaomi-pipa.aarch64

Patch0001:      0001-arm64-dts-qcom-sm8250-xiaomi-pipa-Add-device-tree-fo.patch
Patch0002:      0002-power-supply-Add-driver-for-Qualcomm-PMIC-fuel-gauge.patch
Patch0003:      0003-Input-Add-nt36523-touchscreen-driver.patch
Patch0004:      0004-drm-msm-dsi-change-sync-mode-to-sync-on-DSI0-rather-.patch
Patch0005:      0005-drm-msm-dsi-support-DSC-configurations-with-slice_pe.patch
Patch0006:      0006-drm-panel-Add-support-for-Novatek-NT36532-panel.patch
Patch0007:      0007-drivers-media-i2c-ov13b10-add-device-tree-support-an.patch
Patch0008:      0008-ASoC-qcom-sm8250-add-tertiary-tdm-support.patch
Patch0010:      0010-HACK-ASoC-codecs-aw88261-add-xiaomi-pipa-hacks.patch
Patch0011:      0011-FROMLIST-ASoC-qcom-qdsp6-q6afe-fix-clk-vote-response.patch
Patch0012:      0012-HACK-ASoC-qcom-qdsp6-q6afe-pretend-the-AFE-vote-didn.patch
Patch0013:      0013-Input-keyboard-add-Xiaomi-Nanosic-803-keyboard.patch
Patch0014:      0014-UPSTREAM-libbpf-Fix-UAF-in-strset__add_str.patch
Patch0015:      0015-arm64-dts-qcom-sm8250-xiaomi-pipa-Unify-single-dtb.patch
Patch0016:      0016-drm-panel-novatek-nt36532-add-unified-pipa-compatible.patch
Patch0017:      0017-Input-nt36523-try-both-pipa-touch-firmwares.patch
Patch0018:      0018-HACK-ASoC-qcom-qdsp6-q6afe-ignore-clock-set-param-er.patch

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
Stable Linux kernel %{kversion} for the Xiaomi Pad 6 (SM8250 / pipa).
Matches postmarketOS linux-xiaomi-pipa patches and config.

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
%setup -q -n linux-%{kversion}
cp %{SOURCE1} .config

%patch -P 0001 -p1 -F 2
%patch -P 0002 -p1 -F 2
%patch -P 0003 -p1 -F 2
%patch -P 0004 -p1 -F 2
%patch -P 0005 -p1 -F 2
%patch -P 0006 -p1 -F 2
%patch -P 0007 -p1 -F 2
%patch -P 0008 -p1 -F 2
%patch -P 0010 -p1 -F 2
%patch -P 0011 -p1 -F 2
%patch -P 0012 -p1 -F 2
%patch -P 0013 -p1 -F 2
%patch -P 0014 -p1 -F 2
%patch -P 0015 -p1 -F 2
%patch -P 0016 -p1 -F 2
%patch -P 0017 -p1 -F 2
%patch -P 0018 -p1 -F 2

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
* Thu Jul 16 2026 Ayman <ayman@pipa> - 7.1.3-2
- HACK: ignore spurious AFE clock set_param errors so va_macro can probe
- Drop Conflicts: kernel so dnf can upgrade between kernel-pipa releases
- Obsolete older kernel-pipa releases so dnf can upgrade cleanly

* Wed Jul 15 2026 Ayman <ayman@pipa> - 7.1.3-1
- upstream 7.1.3
