%global debug_package %{nil}

# PAD6-DEV pipa/7.1.7-Stable + config only. AFE audio hacks archived.
%global kversion 7.1.7
%global krelease 2
%global kbuildver %(echo %{krelease}-pipa)
%global kcommit f6344729eb71c1cb0c4189827c679502f4cd85a8
%global ksrcdir linux-7.xx-%{kcommit}

Name:           kernel-pipa
Version:        %{kversion}
Release:        %{krelease}%{?dist}
Summary:        Stable kernel for Xiaomi Pad 6
License:        GPL-2.0-only
URL:            https://github.com/PAD6-DEV/linux-7.xx/tree/pipa/7.1.7-Stable
ExclusiveArch:  aarch64

Source0:        https://github.com/PAD6-DEV/linux-7.xx/archive/%{kcommit}/linux-7.xx-%{kcommit}.tar.gz
Source1:        config-xiaomi-pipa.aarch64

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
Recommends:     pipa-dracut
Recommends:     pipa-grub-config
# Rich deps like "(kmod(i2c_dev.ko) if kernel)" need this for built-in i2c-dev.
Provides:       kernel = %{kversion}
Provides:       kernel-uname-r = %{kversion}-pipa
Provides:       kmod(i2c_dev.ko)
Obsoletes:      kernel-pipa < %{version}-%{release}

%description
Linux %{kversion} for the Xiaomi Pad 6 (SM8250 / pipa): PAD6-DEV pipa/7.1.7-Stable
with pipa config only (no local kernel patches).

%package headers
Summary:        Header files for kernel-pipa
Provides:       kernel-headers = %{kversion}
Obsoletes:      kernel-pipa-headers < %{version}-%{release}

%description headers
Kernel header files for building out-of-tree modules against kernel-pipa.

%package modules
Summary:        Kernel modules for kernel-pipa
Requires:       kernel-pipa = %{version}-%{release}
Recommends:     pipa-dracut
Recommends:     pipa-grub-config
Provides:       kernel-modules = %{kversion}
Obsoletes:      kernel-pipa-modules < %{version}-%{release}

%description modules
Loadable kernel modules for kernel-pipa.

%prep
%setup -q -n %{ksrcdir}
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

%post modules
%{_sbindir}/depmod -a %{kversion}-pipa >/dev/null 2>&1 || :
if [ -d /usr/lib/modules ]; then
  for d in /usr/lib/modules/*-pipa /usr/lib/modules/%{kversion}*; do
    [ -d "$d" ] || continue
    %{_sbindir}/depmod -a "$(basename "$d")" >/dev/null 2>&1 || :
  done
fi
if [ -x /usr/local/bin/pipa-refresh-initramfs ]; then
  /usr/local/bin/pipa-refresh-initramfs >/dev/null 2>&1 || :
elif [ -x /usr/local/bin/pipa-refresh-grub-config ]; then
  /usr/local/bin/pipa-refresh-grub-config >/dev/null 2>&1 || :
fi

%postun modules
if [ "$1" = "0" ] && [ -d /usr/lib/modules ]; then
  for d in /usr/lib/modules/*-pipa /usr/lib/modules/%{kversion}*; do
    [ -d "$d" ] || continue
    %{_sbindir}/depmod -a "$(basename "$d")" >/dev/null 2>&1 || :
  done
fi

%changelog
* Sun Sep 20 2026 Ayman <ayman@pipa> - 7.1.7-2
- Archive AFE audio hacks; build stock PAD6 tree + config only

* Sun Sep 20 2026 Ayman <ayman@pipa> - 7.1.7-1
- Switch to PAD6-DEV/linux-7.xx pipa/7.1.7-Stable (f6344729eb71)
- Drop integrated 7.1.4 kernel.org device patches; keep AFE audio hacks only

* Tue Aug 11 2026 Ayman <ayman@pipa> - 7.1.4-5
- Provide kmod(i2c_dev.ko) / kernel-uname-r so fwupd deps work without kernel-default
- Rebuild pipa initramfs and GRUB from kernel-pipa-modules %%post

* Tue Aug 11 2026 Ayman <ayman@pipa> - 7.1.4-4
- Ignore AFE clock set_param errors so va_macro probes (fixes silent audio)

* Thu Jul 30 2026 Ayman <ayman@pipa> - 7.1.4-3
- Report tablet mode without keyboard (pmaports 4a6b2648)

* Sun Jul 26 2026 Ayman <ayman@pipa> - 7.1.4-2
- Retry the FSA4480 chip id read so the USB-C SBU mux probes on pipa
- Enable mdss_dp and CONFIG_TYPEC_DP_ALTMODE for USB-C DisplayPort output

* Sat Jul 25 2026 Ayman <ayman@pipa> - 7.1.4-1
- Switch to kernel.org 7.1.4 with Xiaomi Pad 6 device patches
- Keep only local single-DTB unify overlay

* Sun Jul 19 2026 Ayman <ayman@pipa> - 7.1.0-4
- Rebuild as linux-pipa pkgrel 4 (SoftISP patches beside PKGBUILD for makepkg)

* Fri Jul 17 2026 Ayman <ayman@pipa> - 7.1.0-1
- Switch source to PipaDB/linux pipa/7.1

* Wed Jul 15 2026 Ayman <ayman@pipa> - 7.1.3-1
- upstream 7.1.3
