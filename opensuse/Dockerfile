FROM opensuse/tumbleweed

RUN zypper --non-interactive refresh && \
    zypper --non-interactive install -y \
    rpm-build rpmdevtools createrepo_c \
    gcc gcc-c++ make cmake meson ninja \
    bc bison flex cpio kmod python3-base tar xz rsync wget curl git \
    clang llvm lld \
    openssl libopenssl-devel libelf-devel dwarves perl hostname \
    glib2-devel libgudev-1_0-devel libprotobuf-c-devel libqmi-devel \
    json-glib-devel gobject-introspection-devel \
    gtk-doc umockdev-devel systemd-rpm-macros systemd-devel \
    polkit-devel python3-dbus \
    python3-devel python3-Jinja2 python3-PyYAML python3-ply python3-pybind11 \
    libevent-devel libyaml-devel libgnutls-devel \
    libdrm-devel libjpeg8-devel SDL2-devel \
    gstreamer-devel gstreamer-plugins-base-devel \
    lttng-ust-devel libtiff-devel \
    qrtr-devel \
    && zypper clean -a

RUN rpmdev-setuptree
WORKDIR /work
