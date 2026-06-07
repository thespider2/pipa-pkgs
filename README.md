# pipa-pkgs

`pipa-pkgs` is a pacman repository for Xiaomi Pad 6 / Pipa packages, published with GitHub Pages.
It is designed to replace or reduce dependency on the upstream `pipa-alarm` feed during image builds.

## Goals

- Build the packages maintained in `endeavouros-pipa`
- Mirror selected upstream Pipa packages into the same repo
- Publish a pacman repository at `https://<user>.github.io/pipa-pkgs/repo/`
- Make `pipa-endeavouros-builder/build-image.sh` faster by pointing `PIPA_REPO_URL` at a single cached feed

## Repository Layout

- `config/packages.local.txt`: packages built from your source repo
- `config/packages.upstream.txt`: packages mirrored from the upstream Pipa repo
- `config/repo.env`: main configuration for source and upstream repos
- `scripts/build-local-packages.sh`: builds local `PKGBUILD`s into the pacman repo
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

This repo expects your package sources to come from:

```text
https://github.com/aymanrgab/endeavouros-pipa.git
```

To build locally on an ARM64 Arch host:

```bash
git clone https://github.com/aymanrgab/pipa-pkgs.git
cd pipa-pkgs
docker build -t pipa-pkgs-builder .
mkdir -p repo work

git clone https://github.com/aymanrgab/endeavouros-pipa.git work/endeavouros-pipa

docker run --rm   -v "$PWD/repo:/repo"   -v "$PWD/config:/config"   -v "$PWD/work/endeavouros-pipa:/src/endeavouros-pipa"   pipa-pkgs-builder /usr/local/bin/build-local-packages.sh

python scripts/fetch-upstream.py
scripts/compose-repo.sh
scripts/stage-pages.sh
```

## Use In Image Builds

Point the builder at your published repo:

```bash
PIPA_REPO_URL="https://<your-github-username>.github.io/pipa-pkgs/repo/"   docker run --privileged   -v "$(pwd)/images:/build/images"   -v "/dev:/dev"   pipa-endeavouros-builder plasma
```

## GitHub Setup

1. Create a new GitHub repository named `pipa-pkgs`.
2. Push this local scaffold to `main`.
3. In GitHub repo settings, enable Pages with GitHub Actions.
4. Edit `config/repo.env` so `PAGES_BASE_URL` matches your GitHub Pages URL.
5. Run the `Publish pacman repo` workflow.

## Notes

- The workflow assumes an ARM64 runner because these packages target `aarch64`.
- If `ubuntu-24.04-arm` is unavailable for your repository, use a self-hosted ARM64 runner.
- Local packages win over mirrored upstream packages because overlapping package names are intentionally excluded from `packages.upstream.txt`.
