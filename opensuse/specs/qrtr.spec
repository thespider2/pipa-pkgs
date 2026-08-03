Name:           qrtr
Version:        1.1
Release:        1%{?dist}
Summary:        Qualcomm IPC Router userspace
License:        BSD-3-Clause
URL:            https://github.com/linux-msm/qrtr
Source0:        %{url}/archive/refs/heads/master.tar.gz#/%{name}-master.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja

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

%files
%license LICENSE
%{_bindir}/qrtr-cfg
%{_bindir}/qrtr-lookup
%{_libdir}/libqrtr.so.*

%files devel
%{_includedir}/libqrtr.h
%{_libdir}/libqrtr.so
%{_libdir}/pkgconfig/qrtr.pc

%changelog
* Mon Aug 03 2026 Ayman <ayman@pipa> - 1.1-1
- Package current linux-msm qrtr (cfg/lookup + libqrtr, no ns service)
