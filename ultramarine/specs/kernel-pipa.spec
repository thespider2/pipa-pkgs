%global debug_package %{nil}

# kernel.org + device patches (+ local single DTB).
%global kversion 7.1.4
%global krelease 1
%global kbuildver %(echo $((%{krelease} + 1))-pipa)

Name:           kernel-pipa
Version:        %{kversion}
Release:        %{krelease}%{?dist}
Summary:        Stable kernel for Xiaomi Pad 6
License:        GPL-2.0-only
URL:            https://kernel.org
ExclusiveArch:  aarch64

Source0:        https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-%{kversion}.tar.xz
Source1:        config-xiaomi-pipa.aarch64

Patch0:         0001-arm64-dts-qcom-sm8250-xiaomi-pipa-Add-device-tree-fo.patch
Patch1:         0002-power-supply-Add-driver-for-Qualcomm-PMIC-fuel-gauge.patch
Patch2:         0003-Input-Add-nt36523-touchscreen-driver.patch
Patch3:         0004-drm-msm-dsi-change-sync-mode-to-sync-on-DSI0-rather-.patch
Patch4:         0005-drm-msm-dsi-support-DSC-configurations-with-slice_pe.patch
Patch5:         0006-drm-panel-Add-support-for-Novatek-NT36532-panel.patch
Patch6:         0007-drivers-media-i2c-ov13b10-add-device-tree-support-an.patch
Patch7:         0008-ASoC-qcom-sm8250-add-tertiary-tdm-support.patch
Patch8:         0010-HACK-ASoC-codecs-aw88261-add-xiaomi-pipa-hacks.patch
Patch9:         0011-FROMLIST-ASoC-qcom-qdsp6-q6afe-fix-clk-vote-response.patch
Patch10:        0012-HACK-ASoC-qcom-qdsp6-q6afe-pretend-the-AFE-vote-didn.patch
Patch11:        0013-Input-keyboard-add-Xiaomi-Nanosic-803-keyboard.patch
Patch12:        0014-UPSTREAM-libbpf-Fix-UAF-in-strset__add_str.patch
Patch13:        0016-power-supply-add-nuvolta-rx1665-wireless-charger.patch
Patch14:        0017-arm64-dts-qcom-sm8250-xiaomi-pipa-Unify-single-dtb.patch

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
Linux %{kversion} for the Xiaomi Pad 6 (SM8250 / pipa): kernel.org plus
device patches, with a local single-DTB overlay for packaging.

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
* Sat Jul 25 2026 Ayman <ayman@pipa> - 7.1.4-1
- Switch to kernel.org 7.1.4 with Xiaomi Pad 6 device patches
- Keep only local single-DTB unify overlay

* Sun Jul 19 2026 Ayman <ayman@pipa> - 7.1.0-4
- Rebuild as linux-pipa pkgrel 4 (SoftISP patches beside PKGBUILD for makepkg)

* Fri Jul 17 2026 Ayman <ayman@pipa> - 7.1.0-1
- Switch source to PipaDB/linux pipa/7.1

* Wed Jul 15 2026 Ayman <ayman@pipa> - 7.1.3-1
- upstream 7.1.3
