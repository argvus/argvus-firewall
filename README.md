# argvus-firewall

<div align="center">

[![CI](https://github.com/argvus/argvus-firewall/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/argvus/argvus-firewall/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/argvus/argvus-firewall)](./LICENSE)
[![Language: Shell](https://img.shields.io/badge/Shell-POSIX-4EAA25?logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Platform: Arch Linux | Wayland](https://img.shields.io/badge/platform-Arch%20Linux%20%7C%20Wayland-1793D1?logo=archlinux&logoColor=white)](https://archlinux.org/)
[![Pull requests](https://img.shields.io/github/issues-pr/argvus/argvus-firewall)](https://github.com/argvus/argvus-firewall/pulls)
[![Issues](https://img.shields.io/github/issues/argvus/argvus-firewall)](https://github.com/argvus/argvus-firewall/issues)
[![Last commit](https://img.shields.io/github/last-commit/argvus/argvus-firewall)](https://github.com/argvus/argvus-firewall/commits/main)
[![Docs](https://img.shields.io/badge/docs-project-blue)](./docs/)

</div>

iptables-based firewall management tool for the ARGVUS desktop.

The package provides a configurable POSIX shell firewall using `iptables` and
`ip6tables`, with a Python management API for safe configuration and rules
updates.

## Features

- SYN flood, DDoS, port-scan and malformed-packet protection
- Anti-spoofing, IPv6 protection and sysctl hardening
- Configurable protection levels and detailed logging
- SSH and Samba access control with optional IP allowlists
- NAT masquerading and custom rules from `/etc/argvus/firewall/rules.fw`

## Configuration and usage

The installed configuration is `/etc/argvus/firewall/config.conf`.

```sh
sudo argvus firewall on
sudo argvus firewall off
sudo argvus firewall status
sudo argvus firewall config
sudo argvus firewall rules
sudo argvus firewall manage        # structured interface (see the documentation)
sudo systemctl enable --now argvus-firewall
```

## Repository layout

```text
packaging/arch/{ci,local}/  release and local PKGBUILDs
packaging/arch/common/      shared packaging functions and install hook
src/                        installed firewall payload
tests/                      management and shell integration tests
tools/sh/                   local build and validation scripts
build/                      ignored build outputs
```

## Build and validation

On Arch Linux or a compatible distribution:

```sh
sudo pacman -S --needed base-devel git iptables python shellcheck
make validate
make build
```

`make build` creates a deterministic source archive under
`build/artifacts/` and the package under `build/dist/`. Install a locally
built package with `make install`.

For metadata-only checks:

```sh
makepkg -p packaging/arch/remote/PKGBUILD --printsrcinfo
makepkg -p packaging/arch/local/PKGBUILD --printsrcinfo
```

See [DEVELOPMENT.md](DEVELOPMENT.md) and
[packaging/arch/README.md](packaging/arch/README.md) for the release layout.

## Contributing and policies

- [CONTRIBUTING.md](https://github.com/argvus/.github/blob/main/CONTRIBUTING.md) — contribution workflow
- [SECURITY.md](https://github.com/argvus/.github/blob/main/SECURITY.md) — private vulnerability reports
- [Code of Conduct](https://github.com/argvus/.github/blob/main/policies/CODE_OF_CONDUCT.md) — community standards
- [AI usage policy](https://github.com/argvus/.github/blob/main/policies/IA_USAGE.md) — rules for AI-assisted contributions

## License

GPL-3.0-only; see [LICENSE](LICENSE).
