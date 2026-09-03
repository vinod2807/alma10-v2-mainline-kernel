# COPR make_srpm method: `make -f .copr/Makefile srpm outdir=$outdir`
# Produces SRPM from packaging/kernel-mainline-v2.spec + VERSION.

TOP := $(dir $(lastword $(MAKEFILE_LIST)))/..
VER := $(shell cat $(TOP)/VERSION | tr -d ' \n')
outdir ?= /tmp
OUTDIR ?= $(outdir)

srpm:
	set -e; \
	rm -rf /tmp/copr-kernel-srpm; mkdir -p /tmp/copr-kernel-srpm/{SOURCES,SPECS,SRPMS}; \
	cp $(TOP)/packaging/kernel-mainline-v2.spec /tmp/copr-kernel-srpm/SPECS/; \
	cp $(TOP)/config/alma10-v2-base.config /tmp/copr-kernel-srpm/SOURCES/alma10-v2-base.config; \
	cp $(TOP)/config/lsmod-v2-pc.txt /tmp/copr-kernel-srpm/SOURCES/lsmod-v2-pc.txt; \
	spectool -g -C /tmp/copr-kernel-srpm/SOURCES /tmp/copr-kernel-srpm/SPECS/kernel-mainline-v2.spec || curl -L -o /tmp/copr-kernel-srpm/SOURCES/linux-$(VER).tar.xz https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-$(VER).tar.xz; \
	rpmbuild -bs /tmp/copr-kernel-srpm/SPECS/kernel-mainline-v2.spec --define "_topdir /tmp/copr-kernel-srpm" --define "version $(VER)"; \
	mkdir -p $(OUTDIR); cp /tmp/copr-kernel-srpm/SRPMS/*.src.rpm $(OUTDIR)/
