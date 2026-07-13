FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential debhelper devscripts dpkg-dev fakeroot \
    equivs lintian reprepro apt-utils \
    meson ninja-build cmake pkg-config \
    gcc g++ make bc bison flex cpio kmod rsync wget curl git \
    python3 python3-dev python3-jinja2 python3-yaml python3-ply python3-pybind11 \
    libssl-dev libelf-dev dwarves libdw-dev \
    libglib2.0-dev libgudev-1.0-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler \
    libqmi-glib-dev \
    libjson-glib-dev gobject-introspection libgirepository1.0-dev \
    libpolkit-gobject-1-dev umockdev libumockdev-dev python3-dbusmock \
    libdrm-dev libjpeg-dev libsdl2-dev libtiff-dev libyaml-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    liblttng-ust-dev libqrtr1 libqrtr-dev \
    systemd libsystemd-dev udev \
    ca-certificates xz-utils tar gzip unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
