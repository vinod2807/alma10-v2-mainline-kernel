# COPR make_srpm method: `make -f .copr/Makefile srpm outdir=$outdir`
# ELRepo kernel-ml rebuild for AlmaLinux 10 x86_64_v2.
# Produces SRPM from packaging/elrepo/kernel-ml-7.2.spec.

TOP := $(dir $(lastword $(MAKEFILE_LIST)))/..
VER := $(shell cat $(TOP)/VERSION | tr -d ' \n')
SPEC := packaging/elrepo/kernel-ml-7.2.spec
outdir ?= /tmp
OUTDIR ?= $(outdir)

srpm:
	set -e; \
	rm -rf /tmp/copr-kernel-srpm; mkdir -p /tmp/copr-kernel-srpm/{SOURCES,SPECS,SRPMS}; \
	cp $(TOP)/$(SPEC) /tmp/copr-kernel-srpm/SPECS/; \
	cp $(TOP)/packaging/elrepo/config-* $(TOP)/packaging/elrepo/filter-*.sh $(TOP)/packaging/elrepo/mod-*.sh $(TOP)/packaging/elrepo/mod-*.list $(TOP)/packaging/elrepo/*.logrotate /tmp/copr-kernel-srpm/SOURCES/ 2>/dev/null || true; \
	spectool -g -C /tmp/copr-kernel-srpm/SOURCES /tmp/copr-kernel-srpm/SPECS/kernel-ml-7.2.spec || curl -L -o /tmp/copr-kernel-srpm/SOURCES/linux-$(VER).tar.xz https://www.kernel.org/pub/linux/kernel/v7.x/linux-$(VER).tar.xz; \
	rpmbuild -bs /tmp/copr-kernel-srpm/SPECS/kernel-ml-7.2.spec --define "_topdir /tmp/copr-kernel-srpm"; \
	mkdir -p $(OUTDIR); cp /tmp/copr-kernel-srpm/SRPMS/*.src.rpm $(OUTDIR)/
