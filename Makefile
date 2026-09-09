PREFIX ?= /usr
DESTDIR ?=
INSTALL ?= install
RM ?= rm -f

.DEFAULT_GOAL := help

.PHONY: help install uninstall validate release-archive build clean

help:
	@echo "Available targets:"
	@echo "  make build"
	@echo "  make install"
	@echo "  make uninstall"
	@echo "  make validate"
	@echo "  make release-archive"
	@echo "  make clean"

install:
	$(INSTALL) -Dm644 src/usr/lib/argvus-firewall/manage.py \
		"$(DESTDIR)$(PREFIX)/lib/argvus-firewall/manage.py"
	$(INSTALL) -Dm755 src/usr/bin/argvus-firewall \
		"$(DESTDIR)$(PREFIX)/bin/argvus-firewall"
	$(INSTALL) -Dm644 src/etc/argvus/firewall/config.conf \
		"$(DESTDIR)/etc/argvus/firewall/config.conf"
	$(INSTALL) -Dm644 src/etc/argvus/firewall/rules.fw \
		"$(DESTDIR)/etc/argvus/firewall/rules.fw"
	$(INSTALL) -Dm644 src/usr/lib/systemd/system/argvus-firewall.service \
		"$(DESTDIR)$(PREFIX)/lib/systemd/system/argvus-firewall.service"
	$(INSTALL) -Dm644 packaging/arch/argvus-firewall.install \
		"$(DESTDIR)$(PREFIX)/share/argvus/argvus-firewall.install"
	$(INSTALL) -Dm644 LICENSE \
		"$(DESTDIR)$(PREFIX)/share/licenses/argvus-firewall/LICENSE"
	$(INSTALL) -dm755 "$(DESTDIR)/var/log/argvus-firewall"

uninstall:
	$(RM) "$(DESTDIR)$(PREFIX)/lib/argvus-firewall/manage.py"
	$(RM) "$(DESTDIR)$(PREFIX)/bin/argvus-firewall"
	$(RM) -r "$(DESTDIR)/etc/argvus/firewall"
	$(RM) "$(DESTDIR)$(PREFIX)/lib/systemd/system/argvus-firewall.service"
	$(RM) "$(DESTDIR)$(PREFIX)/share/argvus/argvus-firewall.install"
	$(RM) "$(DESTDIR)$(PREFIX)/share/licenses/argvus-firewall/LICENSE"

validate:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
	@set -eu; \
	sh -n src/usr/bin/argvus-firewall; \
	if command -v shellcheck >/dev/null 2>&1; then \
		shellcheck -e SC1090 -e SC1091 -e SC2034 src/usr/bin/argvus-firewall; \
	else \
		echo "shellcheck not found; skipped"; \
	fi; \
	echo "argvus-firewall validation ok"

release-archive:
	mkdir -p .release
	git archive --format=tar.gz --prefix="argvus-firewall-$$(git rev-parse --short HEAD)/" \
		--output=".release/argvus-firewall-$$(git rev-parse --short HEAD).tar.gz" HEAD

.PHONY: build

build:
	@tools/build-local-package.sh

clean:
	rm -rf dist
	rm -f packaging/arch/*.zst packaging/arch/*.tar.gz
