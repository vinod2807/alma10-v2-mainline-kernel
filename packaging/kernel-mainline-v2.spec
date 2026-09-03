Name:           kernel-mainline-v2
Version:        7.2.3
Release:        1%{?dist}
Summary:        Vanilla mainline kernel rebuilt for AlmaLinux 10 x86_64_v2
License:        GPLv2
URL:            https://kernel.org
Source0:        https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-%{version}.tar.xz
Source1:        alma10-v2-base.config

BuildRequires:  gcc, make, bison, flex, elfutils-libelf-devel, openssl-devel, bc, dwarves, rpm-build, python3, perl, rsync
ExclusiveArch:  x86_64 x86_64_v2
%global debug_package %{nil}

%description
Starter spec for v2-only builders. Forces -march=x86-64-v2 and Alma stock
config. For production, align with Fedora kernel spec (dracut, BLS, SELinux
policies). Pair with .copr/Makefile (make_srpm) + COPR webhook.

%prep
%setup -q -n linux-%{version}
cp %{SOURCE1} .config
make olddefconfig
scripts/config --set-str SYSTEM_TRUSTED_KEYS "" || :
scripts/config --set-str MODULE_SIG_KEY "" || :

%build
# No global -march here: it breaks arch/x86/boot real-mode code.
# v2 baseline comes from the Alma v2 base config in %prep.
make -j$(nproc)
make modules

%install
mkdir -p %{buildroot}/boot %{buildroot}/lib/modules
make INSTALL_PATH=%{buildroot}/boot install
make INSTALL_MOD_PATH=%{buildroot} modules_install
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
* Thu Sep 04 2026 Vinod <vinod@localhost> - 7.2.3-1
- Initial starter spec for Alma10 v2
