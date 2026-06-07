# pipa-pkgs

`pipa-pkgs` is a pacman repository for Xiaomi Pad 6 / Pipa packages, published with GitHub Pages.
It is designed to replace or reduce dependency on the upstream `pipa-alarm` feed during image builds.
This repo now carries your local `pkgbuilds/` tree directly, including the `linux-pipa` 7.0.8 kernel package source.

## Goals

- Build all packages whose `PKGBUILD` sources are stored in this repo
- Use the local `linux-pipa` 7.0.8 package as the kernel source of truth
- Mirror only the remaining upstream Pipa packages that do not yet have local `PKGBUILD`s
- Publish a pacman repository at `https://<user>.github.io/pipa-pkgs/repo/`
- Make `pipa-endeavouros-builder/build-image.sh` faster by pointing `PIPA_REPO_URL` at a single cached feed

## Repository Layout

- `pkgbuilds/`: local package sources built into the pacman repo
- `config/packages.local.txt`: local package directories that should be built
- `config/packages.upstream.txt`: packages still mirrored from the upstream Pipa repo
- `config/repo.env`: repo configuration, Pages URL, sync source, and kernel version note
- `scripts/build-local-packages.sh`: builds local `PKGBUILD`s into the pacman repo
- `scripts/sync-pkgbuilds.sh`: refreshes `pkgbuilds/` from the source `endeavouros-pipa` repo
- `scripts/fetch-upstream.py`: downloads selected upstream packages into the pacman repo
- `scripts/compose-repo.sh`: regenerates the pacman database from all package files
- `scripts/stage-pages.sh`: prepares the GitHub Pages site output
- `.github/workflows/publish.yml`: builds and publishes the repo to GitHub Pages

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
pkgbuilds/linux-pipa/PKGBUILD -> pkgver=7.0.8
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
  -v "$PWD/pkgbuilds:/work/pkgbuilds" \
  pipa-pkgs-builder /usr/local/bin/build-local-packages.sh

python scripts/fetch-upstream.py
scripts/compose-repo.sh
scripts/stage-pages.sh
```

The builder container uses an Arch Linux ARM `base-devel` image so it can run on `aarch64` runners and hosts.

To refresh the local `pkgbuilds/` tree from your main source repo:

```bash
scripts/sync-pkgbuilds.sh
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
- The local kernel source in this repo is the Xiaomi Pad 6 `linux-pipa` package pinned to 7.0.8.
- `packages.upstream.txt` now represents only the packages that still have no local `PKGBUILD` sources in this workspace.
- Local packages win over mirrored upstream packages because overlapping package names are intentionally excluded from `packages.upstream.txt`.
