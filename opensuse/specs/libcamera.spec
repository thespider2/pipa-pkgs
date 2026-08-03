Epoch:          1
Name:           libcamera
Version:        0.7.1
Release:        3%{?dist}
Summary:        Camera support library for Linux with pipa sensor support
License:        LGPL-2.1-or-later AND GPL-2.0-or-later
URL:            https://libcamera.org/
Source0:        https://github.com/libcamera-org/libcamera/archive/refs/tags/v%{version}.tar.gz#/libcamera-%{version}.tar.gz
Source10:       hi846.yaml
Source11:       ov13b10.yaml

Patch0001:      0001-ipa-libipa-Add-sensor-helper-for-OV13B10.patch
Patch0002:      0002-libcamera-add-pipa-sensor-properties.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  meson >= 0.60
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-jinja2
BuildRequires:  python3-ply
BuildRequires:  python3-pyyaml
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pybind11-devel

%description
libcamera is a complex camera support library for Linux. This build
includes sensor helpers and IPA tuning files for the Xiaomi Pad 6
cameras (OV13B10 rear, HI846 front).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Development files for %{name}.

%package ipa
Summary:        IPA modules and proxy for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description ipa
Image Processing Algorithm modules and proxy executables for %{name}.

%package tools
Summary:        Camera tools (cam, libcamerify)
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
Command-line camera tools built with libcamera.

%package -n gstreamer1-plugin-libcamera
Summary:        GStreamer plugin for libcamera
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n gstreamer1-plugin-libcamera
GStreamer element for capturing from libcamera-supported cameras.

%package -n python3-libcamera
Summary:        Python bindings for libcamera
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python3-libcamera
Python 3 bindings for %{name}.

%prep
%autosetup -p1 -N -n %{name}-%{version}
%patch -P 0001 -p1 -F 2
%patch -P 0002 -p1 -F 2

%build
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC -Wno-array-bounds"
%meson \
    -Ddocumentation=disabled \
    -Dpipelines=simple,uvcvideo,vimc \
    -Dipas=simple,vimc \
    -Dv4l2=enabled \
    -Dgstreamer=enabled \
    -Dcam=enabled \
    -Dlc-compliance=disabled \
    -Dqcam=disabled \
    -Dpycamera=enabled \
    -Dtest=false
%meson_build

%install
%meson_install

install -Dm644 %{SOURCE10} %{buildroot}%{_datadir}/libcamera/ipa/simple/hi846.yaml
install -Dm644 %{SOURCE11} %{buildroot}%{_datadir}/libcamera/ipa/simple/ov13b10.yaml

%files
%license LICENSES/
%{_libdir}/libcamera.so.*
%{_libdir}/libcamera-base.so.*
%{_datadir}/libcamera/

%files devel
%{_includedir}/libcamera/
%{_libdir}/libcamera.so
%{_libdir}/libcamera-base.so
%{_libdir}/pkgconfig/libcamera.pc
%{_libdir}/pkgconfig/libcamera-base.pc

%files ipa
%{_libdir}/libcamera/
%{_libexecdir}/libcamera/

%files tools
%{_bindir}/cam
%{_bindir}/libcamerify
%{_bindir}/libcamera-bug-report

%files -n gstreamer1-plugin-libcamera
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files -n python3-libcamera
%{python3_sitearch}/libcamera/

%changelog
* Sat Jul 04 2026 Ayman <ayman@pipa> - 1:0.7.1-3
- Add libexecdir to ipa package (proxy executables, v4l2-compat)
- Disable qcam (not needed, removes Qt6 build dependency)
- Remove doxygen/graphviz/sphinx (docs disabled)

* Sat Jul 04 2026 Ayman <ayman@pipa> - 1:0.7.1-2
- Add epoch to override Fedora package
- Fix patch application with fuzz factor
- Use environment CFLAGS/CXXFLAGS for -fPIC instead of meson args

* Fri Jul 03 2026 Ayman <ayman@pipa> - 0.7.1-1
- Package for Ultramarine OS pipa port with OV13B10/HI846 sensor support
