# alma10-v2-mainline-kernel

Mainline kernels from kernel.org rebuilt for **AlmaLinux 10 x86_64_v2** (v2-only CPUs like Intel i5-650, no AVX).

ELRepo EL10 `kernel-ml` targets `x86_64_v3` and will not boot here. This repo builds vanilla stable with `-march=x86-64-v2` + Alma stock config.

## Layout

- `VERSION` – current tracked stable (e.g. `7.2.3`)
- `config/alma10-v2-base.config` – stock Alma 10.2 v2 config as base
- `scripts/build-v2.sh` – local / CI build via `make binrpm-pkg`
- `packaging/kernel-mainline-v2.spec` – COPR SCM spec (starter, iterates to full dracut/BLS support)
- `.copr/Makefile` – COPR `make_srpm` method
- `.github/workflows/check-upstream.yml` – daily cron, bumps VERSION + tags on new kernel.org stable
- `.github/workflows/build-rpm.yml` – builds RPM artifact on push/tag

## Auto-update flow (GitHub + COPR)

1. `check-upstream.yml` (cron `0 6 * * *`) fetches `https://www.kernel.org/releases.json`, compares `stable` to `VERSION`.
2. On new version: updates `VERSION`, commits, tags `vX.Y.Z`, pushes.
3. COPR webhook (push/tag event) auto-submits build for all enabled chroots.
4. On your Alma box:
```bash
sudo dnf copr enable vinod2807/alma10-v2-mainline-kernel
sudo dnf update -y
```

COPR one-time setup (web UI at copr.fedorainfracloud.org):
1. Create project `alma10-v2-mainline-kernel`.
2. Enable chroots: `epel-10-x86_64` (builders are v3 hosts, but output is forced to v2 via CFLAGS/config — see spec).
3. Add package SCM: clone URL of this repo, spec `packaging/kernel-mainline-v2.spec`, method `make_srpm` (uses `.copr/Makefile`), check `webhook rebuild`.
4. Settings → Integrations: copy webhook URL → GitHub repo Settings → Webhooks → Add (pushes + tag creation, `application/json`).

## Fast trimmed build (this PC only)

`config/lsmod-v2-pc.txt` (`115` loaded modules) + `make localmodconfig` trims the
full Alma config (thousands of modules, ~1h+) down to this machine's hardware
(~10-15min). DWARF/BTF debug info and SBAT are also disabled (legacy BIOS box,
no SecureBoot/shim, personal kernel).

Refresh after plugging in every device you use (USB, etc.) — unplugged hardware
has no driver in a trimmed build:
```bash
lsmod > config/lsmod-v2-pc.txt
git add config/lsmod-v2-pc.txt && git commit -m "chore: refresh lsmod" && git push
```
Delete `config/lsmod-v2-pc.txt` to fall back to the full (slow) Alma config build.

## Manual build (GitHub Actions artifact or local)

```bash
./scripts/build-v2.sh 7.2.3
# output: ~/rpmbuild/RPMS/x86_64/kernel-*.rpm
sudo dnf install -y ~/rpmbuild/RPMS/x86_64/kernel-7.2.3-*.x86_64.rpm
sudo dracut -f /boot/initramfs-7.2.3.img 7.2.3
sudo grubby --add-kernel=/boot/vmlinuz-7.2.3 --initrd=/boot/initramfs-7.2.3.img --title="7.2.3-v2" --copy-default
sudo grubby --set-default /boot/vmlinuz-7.2.3
sudo reboot
uname -r
```

## Notes

- Vanilla `binrpm-pkg` RPMs lack Alma scriptlets — initramfs/BLS entry created manually above. COPR spec adds `%post` dracut/grubby.
- Unsigned for SecureBoot. You boot legacy BIOS, so fine. For EFI, disable SecureBoot or sign with MOK.
- You own CVEs/rebuilds. Stock 6.12 v2 kernel stays installed as fallback.
