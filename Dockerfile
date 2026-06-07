FROM ghcr.io/menci/archlinuxarm:base-devel

RUN pacman -Syu --needed --noconfirm     git sudo gcc make pacman-contrib     arch-install-scripts e2fsprogs dosfstools zip unzip     bc bison flex cpio kmod python tar xz meson ninja cmake rsync wget curl     glib2 libgudev polkit libqmi protobuf-c qrtr dracut android-tools     pahole gtk-doc umockdev alsa-lib dbus ell json-c libical readline     python-docutils python-pygments autoconf automake libtool

RUN useradd -m builder

COPY scripts/build-local-packages.sh /usr/local/bin/build-local-packages.sh
RUN chmod +x /usr/local/bin/build-local-packages.sh

WORKDIR /work
