# pipa-pkgs

`pipa-pkgs` is a multi-distro package repository for Xiaomi Pad 6 / Pipa, published with GitHub Pages.
It hosts Arch Linux (pacman), Ultramarine/Fedora (dnf), and Ubuntu (apt) packages, enabling OTA updates from a single repo.

## Goals

- Build all packages whose sources are stored in this repo (PKGBUILDs, RPM specs, and Debian packaging)
- Use the local `linux-pipa` 7.1.4 package as the kernel source of truth
- Mirror only the remaining upstream Pipa packages that do not yet have local `PKGBUILD`s
- Publish a pacman repository at `https://<user>.github.io/pipa-pkgs/repo/`
- Publish a DNF repository at `https://<user>.github.io/pipa-pkgs/repo/ultramarine/`
- Publish an apt repository at `https://<user>.github.io/pipa-pkgs/repo/ubuntu/`
- Publish a zypper repository at `https://<user>.github.io/pipa-pkgs/repo/opensuse/`
- Enable OTA updates for EndeavourOS, Ultramarine OS, Ubuntu, and openSUSE installs

## Repository Layout

- `common/`, `sm8250/`: package source trees (PKGBUILDs + patches + configs)
- `ultramarine/specs/`: RPM `.spec` files for Ultramarine/Fedora packages
- `ultramarine/Dockerfile`: Fedora 44 build container for RPMs
- `ultramarine/pipa-pkgs.repo`: DNF repo config file for the tablet
- `opensuse/specs/`: RPM `.spec` files for openSUSE Tumbleweed packages
- `opensuse/Dockerfile`: Tumbleweed build container for RPMs
- `opensuse/pipa-pkgs.repo`: zypper repo config file for the tablet
- `ubuntu/packages/*/debian/`: Debian packaging for Ubuntu 26.04 (Resolute)
- `ubuntu/Dockerfile`: Ubuntu 26.04 build container for debs
- `ubuntu/pipa-pkgs.list`: apt sources snippet shipped by `pipa-metapkg`
- `config/packages.local.txt`: local package directories that should be built (pacman)
- `config/packages.upstream.txt`: packages still mirrored from the upstream Pipa repo
- `config/repo.env`: repo configuration, Pages URL, sync source, and kernel version note
- `scripts/build-local-packages.sh`: builds local `PKGBUILD`s into the pacman repo
- `scripts/build-ultramarine-rpms.sh`: builds RPM specs into the Ultramarine repo
- `scripts/build-opensuse-rpms.sh`: builds RPM specs into the openSUSE repo
- `scripts/build-ubuntu-debs.sh`: builds Ubuntu debs into the apt repo
- `scripts/sync-pkgbuilds.sh`: refreshes `pkgbuilds/` from the source `endeavouros-pipa` repo
- `scripts/fetch-upstream.py`: downloads selected upstream packages into the pacman repo
- `scripts/compose-repo.sh`: regenerates the pacman database from all package files
- `scripts/stage-pages.sh`: prepares the GitHub Pages site output
- `.github/workflows/publish.yml`: builds and publishes all repos to GitHub Pages

## Expected Published URL

Once Pages is enabled, the pacman repo URL should be:

```text
https://<your-github-username>.github.io/pipa-pkgs/repo/
```

Update `config/repo.env` before the first publish.

## Local Build

This repo is self-contained for the local packages that already live under `pkgbuilds/`.
The local kernel source is:

```text
sm8250/linux-pipa/PKGBUILD -> pkgver=7.1.4
```

To build locally on an ARM64 host:

```bash
git clone https://github.com/thespider2/pipa-pkgs.git
cd pipa-pkgs
docker build -t pipa-pkgs-builder .
mkdir -p repo

docker run --rm \
  -v "$PWD/repo:/repo" \
  -v "$PWD/config:/config" \
  -v "$PWD/common:/work/common" \
  -v "$PWD/sm8250:/work/sm8250" \
  pipa-pkgs-builder /usr/local/bin/build-local-packages.sh

python scripts/fetch-upstream.py
docker run --rm -v "$PWD:/work" -w /work pipa-pkgs-builder scripts/compose-repo.sh
sudo chown -R "$USER:$USER" repo
scripts/stage-pages.sh
```

The builder container uses an Arch Linux ARM `base-devel` image so it can run on `aarch64` runners and hosts.

### Reuse Existing Package Builds

Keep the local `repo/` directory between runs.
`scripts/build-local-packages.sh` now stores a source hash per package under `repo/repo/.build-cache/` and reuses the already built package archives when the corresponding `pkgbuilds/<name>/` tree has not changed.
If you change a PKGBUILD or any file under that package directory, only that package is rebuilt.
The GitHub Actions publish workflow also restores the previous `repo/` cache first, so unchanged local packages are not rebuilt there either.

### Update A Running Tablet

Runtime fixes that belong in packages should be delivered through this repo so the tablet can pull them without a full image rebuild.
For the current sensor suspend/resume recovery and the GRUB menu refresh, publish the updated packages and then run on the tablet:

```bash
sudo pacman -Syu pipa-pkgs/pipa-sensors pipa-pkgs/pipa-grub-config
```

Those packages now carry:

- the sensor persist directory preparation helper
- the safe sensor resume hook
- the tmpfiles rule for `/mnt/vendor/persist/sensors/registry`
- the tablet-side `/boot/grub2/grub.cfg` refresh helper
- the separate DTB GRUB entry as the default boot option
- the GRUB menu resolution set to `1800x2880`

To refresh the local `common/` and `sm8250/` trees from your main source repo:

```bash
scripts/sync-pkgbuilds.sh
```

## Ultramarine / Fedora (DNF) Repository

The RPM packages are built from `.spec` files in `ultramarine/specs/` using the same
source files in `common/` and `sm8250/` that the Arch packages use.

### Published URL

```text
https://thespider2.github.io/pipa-pkgs/repo/ultramarine/
```

### Add to a running tablet

```bash
sudo cp pipa-pkgs.repo /etc/yum.repos.d/
sudo dnf install pipa-metapkg
```

Or install manually from the repo URL:

```bash
sudo dnf config-manager --add-repo https://thespider2.github.io/pipa-pkgs/repo/ultramarine/
sudo dnf install pipa-metapkg
```

### OTA Updates

```bash
sudo dnf upgrade --refresh
```

### Build RPMs locally

```bash
docker build -t pipa-rpms-builder -f ultramarine/Dockerfile .
docker run --rm -v "$PWD:/work" -w /work pipa-rpms-builder scripts/build-ultramarine-rpms.sh
```

RPMs are output to `repo/ultramarine/`.

## openSUSE Tumbleweed (zypper) Repository

RPMs are built from `.spec` files in `opensuse/specs/` using the same sources as Ultramarine.

```text
https://thespider2.github.io/pipa-pkgs/repo/opensuse/
```

```bash
sudo zypper addrepo https://thespider2.github.io/pipa-pkgs/repo/opensuse/ pipa-pkgs
sudo zypper install pipa-metapkg
```

Build locally:

```bash
docker build -t pipa-opensuse-rpms-builder -f opensuse/Dockerfile .
docker run --rm -v "$PWD:/work" -w /work pipa-opensuse-rpms-builder scripts/build-opensuse-rpms.sh
```

## Use In Image Builds

Point the builder at your published repo:

```bash
PIPA_REPO_URL="https://thespider2.github.io/pipa-pkgs/repo/" \
  docker run --privileged \
  -v "$(pwd)/images:/build/images" \
  -v "/dev:/dev" \
  pipa-endeavouros-builder plasma
```

## GitHub Setup

1. Create a new GitHub repository named `pipa-pkgs`.
2. Push this local scaffold to `main`.
3. In GitHub repo settings, enable Pages with GitHub Actions.
4. Edit `config/repo.env` so `PAGES_BASE_URL` matches your GitHub Pages URL.
5. Run the `Publish pacman repo` workflow.

## Notes

- The workflow assumes an ARM64 runner because these packages target `aarch64`.
- The builder image uses Arch Linux ARM so `docker build` works on ARM64 runners.
- If `ubuntu-24.04-arm` is unavailable for your repository, use a self-hosted ARM64 runner.
- The local kernel source in this repo is the Xiaomi Pad 6 `linux-pipa` package pinned to 7.1.4.
- `packages.upstream.txt` now represents only the packages that still have no local `PKGBUILD` sources in this workspace.
- Local packages win over mirrored upstream packages because overlapping package names are intentionally excluded from `packages.upstream.txt`.
