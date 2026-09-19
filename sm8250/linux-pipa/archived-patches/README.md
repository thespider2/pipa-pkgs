Patches previously applied on top of vanilla kernel.org for Xiaomi Pad 6.

The **7.1.4 kernel.org patch series** is archived here. Packaging now tracks
[PAD6-DEV/linux-7.xx](https://github.com/PAD6-DEV/linux-7.xx) branch
`pipa/7.1.7-Stable` instead; most of those device patches are integrated
upstream of that tree.

**AFE audio hacks** (archived, not applied — speakers may need them restored):

- `0011` — FROMLIST q6afe clk vote response fix
- `0012` — pretend AFE vote errors succeeded
- `0020` — ignore AFE clock set_param errors (speakers)
- `0018` — older variant of the ignore-clock hack (superseded by `0020`)

**Integrated upstream of pipa/7.1.7-Stable** (archived, not applied):

- Device tree, single `sm8250-xiaomi-pipa.dtb`, mdss_dp / USB-C DisplayPort
- FSA4480 chip-id read retries (upstream uses a retry loop without usleep)
- nt36523 touch driver (pipa dual-firmware auto-select in `0017-Input-…` is
  not upstream; DT may specify firmware-name instead)
- nu1665 / nuvolta RX1665 wireless charger driver
- aw88261 pipa speaker hacks and the rest of the 7.1.4 device series

- `softisp/`: older SoftISP camera bring-up patches (not applied).
