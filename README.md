# argvus-firewall

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
sudo argvus-firewall on
sudo argvus-firewall off
sudo argvus-firewall status
sudo argvus-firewall config
sudo argvus-firewall rules
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
makepkg -p packaging/arch/ci/PKGBUILD --printsrcinfo
makepkg -p packaging/arch/local/PKGBUILD --printsrcinfo
```

See [DEVELOPMENT.md](DEVELOPMENT.md) and
[packaging/arch/README.md](packaging/arch/README.md) for the release layout.

## License

GPL-3.0-only; see [LICENSE](LICENSE).
