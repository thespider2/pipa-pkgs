FROM opensuse/tumbleweed

# Tumbleweed aarch64 ships versioned python3NN-* packages; prefer concrete
# names over unversioned provides so zypper does not fail the transaction.
RUN zypper --non-interactive refresh && \
    zypper --non-interactive install -y \
    rpm-build rpmdevtools createrepo_c \
    gcc gcc-c++ make cmake meson ninja \
    bc bison flex cpio kmod tar xz rsync wget curl git \
    clang llvm lld \
    openssl libopenssl-devel libelf-devel dwarves perl hostname \
    glib2-devel libgudev-1_0-devel protobuf-c-devel libqmi-devel \
    json-glib-devel gobject-introspection-devel \
    gtk-doc umockdev-devel systemd-rpm-macros systemd-devel \
    polkit-devel \
    python313-base python313-devel \
    python313-Jinja2 python313-PyYAML python313-ply \
    python313-pybind11 python313-pybind11-devel \
    python313-dbus-python python313-python-dbusmock \
    libevent-devel libyaml-devel libgnutls-devel \
    libdrm-devel libjpeg8-devel sdl2-compat-devel \
    gstreamer-devel gstreamer-plugins-base-devel \
    lttng-ust-devel libtiff-devel \
    && zypper clean -a

RUN rpmdev-setuptree
WORKDIR /work
