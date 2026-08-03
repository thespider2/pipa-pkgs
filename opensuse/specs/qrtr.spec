Name:           qrtr
Version:        1.1
Release:        1%{?dist}
Summary:        Qualcomm IPC Router userspace
License:        BSD-3-Clause
URL:            https://github.com/linux-msm/qrtr
# v1.0 is Makefile-only; master provides meson + qrtr.pc
Source0:        %{url}/archive/refs/heads/master.tar.gz#/%{name}-master.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  pkgconfig(libudev)
BuildRequires:  systemd-rpm-macros

Requires(post): systemd
Obsoletes:      qrtr < 1.1-1
Provides:       qrtr = %{version}-%{release}

%description
Userspace reference for the Qualcomm IPC router protocol (QRTR).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       pkgconfig(qrtr) = %{version}
Obsoletes:      qrtr-devel < 1.1-1
Provides:       qrtr-devel = %{version}-%{release}

%description devel
Headers and pkg-config file for %{name}.

%prep
%autosetup -n %{name}-master

%build
%meson
%meson_build

%install
%meson_install

%post
%systemd_post qrtr-ns.service

%preun
%systemd_preun qrtr-ns.service

%postun
%systemd_postun_with_restart qrtr-ns.service

%files
%license LICENSE
%{_bindir}/qrtr-*
%{_libdir}/libqrtr.so.*
%{_unitdir}/qrtr-ns.service

%files devel
%{_includedir}/libqrtr.h
%{_libdir}/libqrtr.so
%{_libdir}/pkgconfig/qrtr.pc

%changelog
* Mon Aug 03 2026 Ayman <ayman@pipa> - 1.1-1
- Build linux-msm qrtr master (meson) for openSUSE pkgconfig(qrtr)
