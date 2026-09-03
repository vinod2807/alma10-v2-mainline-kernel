#!/bin/bash
# Build vanilla kernel.org tarball for AlmaLinux 10 x86_64_v2 via make binrpm-pkg.
# Usage: ./scripts/build-v2.sh [VERSION]  (default: cat VERSION)
set -euo pipefail

VER="${1:-$(cat "$(dirname "$0")/../VERSION" | tr -d ' \n')}"
MAJOR="${VER%%.*}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK=/tmp/kbuild-v2

echo "== Building kernel $VER for x86_64_v2 =="
mkdir -p "$WORK"
cd "$WORK"

TARBALL="linux-${VER}.tar.xz"
URL="https://cdn.kernel.org/pub/linux/kernel/v${MAJOR}.x/${TARBALL}"
if [ ! -f "$TARBALL" ]; then
  curl -LO "$URL"
fi

rm -rf "linux-${VER}"
tar xf "$TARBALL"
cd "linux-${VER}"

# Base on Alma v2 stock config
cp "$REPO_ROOT/config/alma10-v2-base.config" .config
make olddefconfig

# Drop distro signing keys (ephemeral build). Do NOT pass global
# -march via KCFLAGS: it breaks arch/x86/boot real-mode code
# (bzImage link failure). v2 baseline comes from the Alma v2 base
# config above, which olddefconfig preserves.
scripts/config --set-str SYSTEM_TRUSTED_KEYS "" || true
scripts/config --set-str SYSTEM_REVOCATION_KEYS "" || true
scripts/config --set-str MODULE_SIG_KEY "" || true
make olddefconfig
grep -E "X86_64_VERSION|GENERIC_CPU|MCORE2|MPROCESSOR" .config || true

make -j"$(nproc)" binrpm-pkg

echo "== RPMs in ~/rpmbuild/RPMS/x86_64/ =="
ls -lh ~/rpmbuild/RPMS/x86_64/ | tail -20
