# linux-pipa (Ubuntu)

Debian packaging for the Xiaomi Pad 6 kernel.

Source: [PAD6-DEV/linux-7.xx](https://github.com/PAD6-DEV/linux-7.xx) branch
`pipa/7.1.7-Stable` (commit `f6344729eb71`) with pipa config only — no local
kernel patches. AFE audio hacks are archived under `sm8250/linux-pipa/archived-patches/`;
`scripts/build-ubuntu-debs.sh` stages only the config into `debian/extras/`.
