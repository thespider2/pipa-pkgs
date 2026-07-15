FROM ghcr.io/menci/archlinuxarm:base-devel

# Pacman 7's Landlock download sandbox fails in Docker/CI (no landlock LSM).
RUN set -eux; \
    sed -i \
      -e 's/^CheckSpace/#CheckSpace/' \
      -e 's/^DownloadUser[[:space:]]*=/#DownloadUser =/' \
      /etc/pacman.conf; \
    grep -q '^DisableSandbox' /etc/pacman.conf || \
      printf '\n# Required for Docker/CI builds without landlock\nDisableSandbox\n' \
        >> /etc/pacman.conf; \
    pacman -Syu --needed --noconfirm --disable-sandbox \
      git sudo gcc make pacman-contrib \
      arch-install-scripts e2fsprogs dosfstools zip unzip \
      bc bison flex cpio kmod python tar xz meson ninja cmake rsync wget curl \
      clang lld llvm \
      glib2 libgudev polkit libqmi protobuf-c qrtr dracut android-tools \
      pahole gtk-doc umockdev alsa-lib dbus ell json-c libical readline \
      python-docutils python-pygments autoconf automake libtool; \
    pacman -Scc --noconfirm --disable-sandbox

RUN useradd -m builder

COPY scripts/build-local-packages.sh /usr/local/bin/build-local-packages.sh
RUN chmod +x /usr/local/bin/build-local-packages.sh

WORKDIR /work
