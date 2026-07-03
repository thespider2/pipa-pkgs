FROM fedora:44

RUN dnf install -y \
    rpm-build rpmdevtools createrepo_c dnf-plugins-core \
    gcc gcc-c++ make cmake meson ninja-build \
    bc bison flex cpio kmod python3 tar xz rsync wget curl git \
    openssl openssl-devel elfutils-devel dwarves perl hostname \
    glib2-devel libgudev-devel protobuf-c-devel libqmi-devel \
    json-glib-devel gobject-introspection-devel \
    gtk-doc umockdev-devel systemd-rpm-macros systemd-devel \
    polkit-devel python3-dbusmock \
    python3-devel python3-jinja2 python3-yaml python3-ply python3-pybind11 pybind11-devel \
    python3-sphinx doxygen graphviz \
    libevent-devel libyaml-devel gnutls-devel \
    libdrm-devel libjpeg-turbo-devel SDL2-devel \
    gstreamer1-devel gstreamer1-plugins-base-devel \
    lttng-ust-devel libtiff-devel \
    qt6-qtbase-devel qt6-qttools-devel \
    qrtr-devel \
    && dnf clean all

RUN rpmdev-setuptree
WORKDIR /work
