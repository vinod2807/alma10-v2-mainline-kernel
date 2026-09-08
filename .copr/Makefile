# COPR make_srpm method: `make -f .copr/Makefile srpm outdir=$outdir`
# ELRepo kernel-ml rebuild for AlmaLinux 10 x86_64_v2.
# SPEC is auto-discovered (packaging/elrepo/kernel-ml-*.spec) so
# check-upstream bumps and future 7.2 -> 7.3 renames don't break COPR.

TOP := $(dir $(lastword $(MAKEFILE_LIST)))/..
VER := $(shell cat $(TOP)/VERSION | tr -d ' \n')
MAJOR := $(shell cat $(TOP)/VERSION | tr -d ' \n' | cut -d. -f1)
SPEC_FILE := $(firstword $(wildcard $(TOP)/packaging/elrepo/kernel-ml-*.spec))
SPEC_NAME := $(notdir $(SPEC_FILE))
outdir ?= /tmp
OUTDIR ?= $(outdir)

srpm:
	set -e; \
	if [ -z "$(SPEC_FILE)" ]; then echo "no spec matching packaging/elrepo/kernel-ml-*.spec" >&2; exit 1; fi; \
	echo "SPEC=$(SPEC_FILE) VER=$(VER)"; \
	rm -rf /tmp/copr-kernel-srpm; mkdir -p /tmp/copr-kernel-srpm/{SOURCES,SPECS,SRPMS}; \
	cp $(SPEC_FILE) /tmp/copr-kernel-srpm/SPECS/; \
	cp $(TOP)/packaging/elrepo/config-* $(TOP)/packaging/elrepo/filter-*.sh $(TOP)/packaging/elrepo/mod-*.sh $(TOP)/packaging/elrepo/mod-*.list $(TOP)/packaging/elrepo/*.logrotate /tmp/copr-kernel-srpm/SOURCES/ 2>/dev/null || true; \
	spectool -g -C /tmp/copr-kernel-srpm/SOURCES /tmp/copr-kernel-srpm/SPECS/$(SPEC_NAME) || curl -L -o /tmp/copr-kernel-srpm/SOURCES/linux-$(VER).tar.xz https://www.kernel.org/pub/linux/kernel/v$(MAJOR).x/linux-$(VER).tar.xz; \
	rpmbuild -bs /tmp/copr-kernel-srpm/SPECS/$(SPEC_NAME) --define "_topdir /tmp/copr-kernel-srpm" --with src; \
	mkdir -p $(OUTDIR); cp /tmp/copr-kernel-srpm/SRPMS/*.rpm $(OUTDIR)/
