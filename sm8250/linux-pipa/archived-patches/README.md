Patches previously applied on top of vanilla kernel.org for Xiaomi Pad 6.

Active packaging keeps the current device patch series next to the PKGBUILD,
plus local `0017` (single DTB unify).

- Numbered `0001`–`0018` here: historical snapshot. Prefer the live copies
  beside the PKGBUILD.
- Live `0020-HACK-…ignore-clock-set-param…` restores the archived audio AFE
  clock hack (was `0018-HACK-…` here; number reused by FSA4480 USB patch).
- `softisp/`: older SoftISP camera bring-up patches (not applied).
