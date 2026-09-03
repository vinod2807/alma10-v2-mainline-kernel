Name:           kernel-mainline-v2
Version:        7.2.3
Release:        2%{?dist}
Summary:        Vanilla mainline kernel rebuilt for AlmaLinux 10 x86_64_v2
License:        GPLv2
URL:            https://kernel.org
Source0:        https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-%{version}.tar.xz
Source1:        alma10-v2-base.config
Source2:        lsmod-v2-pc.txt

BuildRequires:  gcc, make, bison, flex, elfutils-libelf-devel, kmod, openssl, openssl-devel, bc, dwarves, rpm-build, python3, perl, rsync
ExclusiveArch:  x86_64 x86_64_v2
%global debug_package %{nil}

%description
Starter spec for v2-only builders. Forces -march=x86-64-v2 and Alma stock
config. For production, align with Fedora kernel spec (dracut, BLS, SELinux
policies). Pair with .copr/Makefile (make_srpm) + COPR webhook.

%prep
%setup -q -n linux-%{version}
cp %{SOURCE1} .config
# Trim to target PC's loaded modules (Source2 captured via `lsmod` on that box).
yes "" | make LSMOD=%{SOURCE2} localmodconfig
make olddefconfig
scripts/config --set-str SYSTEM_TRUSTED_KEYS "" || :
# Leave MODULE_SIG_KEY at default (auto-generates); emptying it breaks sign-file.
# Vanilla tarball lacks distro kernel.sbat; no SecureBoot/shim here, drop SBAT.
# Skip DWARF+BTF debug info for build speed (personal kernel).
for opt in EFI_SBAT DEBUG_INFO DEBUG_INFO_BTF DEBUG_INFO_BTF_MODULES; do
  scripts/config --disable $opt || :
done
scripts/config --set-str EFI_SBAT_FILE "" || :
make olddefconfig

%build
# No global -march here: it breaks arch/x86/boot real-mode code.
# v2 baseline comes from the Alma v2 base config in %prep.
make -j$(nproc)
make modules

%install
mkdir -p %{buildroot}/boot %{buildroot}/lib/modules
make INSTALL_PATH=%{buildroot}/boot install
make INSTALL_MOD_PATH=%{buildroot} modules_install
# Vanilla `make install` writes unversioned names (vmlinuz, System.map);
# rename to the versioned names %files expects, and ship the .config used.
for f in vmlinuz System.map; do
  if [ ! -f %{buildroot}/boot/$f-%{version} -a -f %{buildroot}/boot/$f ]; then
    mv %{buildroot}/boot/$f %{buildroot}/boot/$f-%{version}
  fi
done
cp .config %{buildroot}/boot/config-%{version}
# remove build symlinks that break RPM
rm -f %{buildroot}/lib/modules/%{version}/build %{buildroot}/lib/modules/%{version}/source || :

%files
/boot/vmlinuz-%{version}
/boot/System.map-%{version}
/boot/config-%{version}
/lib/modules/%{version}/

%post
if [ -x /usr/bin/dracut ]; then
  /usr/bin/dracut -f /boot/initramfs-%{version}.img %{version} || :
fi
if [ -x /usr/sbin/grubby ]; then
  /usr/sbin/grubby --add-kernel=/boot/vmlinuz-%{version} --initrd=/boot/initramfs-%{version}.img --title="%{version}-v2" --copy-default || :
fi

%changelog
* Thu Sep 03 2026 Vinod <vinod@localhost> - 7.2.3-2
- Add kmod to BuildRequires so depmod runs at build time (modules.dep present, dracut works in %post)
* Thu Sep 03 2026 Vinod <vinod@localhost> - 7.2.3-1
- Fix install section: rename unversioned vmlinuz/System.map from vanilla
  make install to versioned names and ship .config
* Thu Sep 03 2026 Vinod <vinod@localhost> - 7.2.3-1
- Initial starter spec for Alma10 v2
