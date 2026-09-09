# argvus-firewall

iptables-based firewall management tool for ARGVUS.

A POSIX shell script that provides a complete, configurable firewall solution
for Arch Linux using iptables and ip6tables. Part of the ARGVUS desktop
environment ecosystem.

## Features

- SYN Flood Protection
- DDoS Prevention
- Port Scan Detection
- Anti-Spoofing
- Advanced Rate Limiting
- IPv6 Protection
- Malformed Packet Chaining
- Sysctl Hardening
- Detailed Logging
- Multiple Protection Levels (`low`, `medium`, `high`, `paranoid`)
- SSH access control with IP whitelisting and brute-force protection
- Samba access control with IP whitelisting and brute-force protection
- NAT masquerading with LAN-to-WAN forwarding
- Custom user rules via `/etc/argvus/firewall/rules.fw`

## Configuration

All settings live in `/etc/argvus/firewall/config.conf`:

| Variable | Default | Description |
|---|---|---|
| `INTERFACE_WAN` | `""` | WAN interface (e.g. `enp0s3`, `eno1`) |
| `INTERFACE_LAN` | `""` | LAN interface (e.g. `enp0s8`) |
| `MASQUERADE_ENABLE` | `n` | NAT masquerading toggle |
| `PROTECTION_LEVEL` | `high` | `low`, `medium`, `high`, or `paranoid` |
| `ALLOW_SSH` | `n` | SSH access toggle |
| `SSH_CLIENTS_IP` | `""` | Comma-separated SSH client IPs |
| `SSH_PORT` | `22` | SSH port |
| `ALLOW_SAMBA` | `n` | Samba access toggle |
| `SAMBA_CLIENTS_IP` | `""` | Comma-separated Samba client IPs |
| `ALLOW_ICMP` | `y` | ICMP/ping toggle |
| `SYN_FLOOD_PROTECTION` | `y` | SYN flood protection toggle |
| `DDOS_PROTECTION` | `y` | DDoS protection toggle |
| `PORT_SCAN_PROTECTION` | `y` | Port scan protection toggle |
| `ANTI_SPOOFING` | `y` | Anti-spoofing toggle |

## Install

```sh
make DESTDIR=/tmp/argvus-firewall-dest PREFIX=/usr install
```

Installed paths:

```text
/usr/bin/argvus-firewall
/etc/argvus/firewall/config.conf
/etc/argvus/firewall/rules.fw
/usr/lib/systemd/system/argvus-firewall.service
/usr/share/argvus/argvus-firewall.install
/usr/share/licenses/argvus-firewall/LICENSE
```

## Usage

```sh
# Enable the firewall
sudo argvus-firewall on

# Disable the firewall
sudo argvus-firewall off

# Edit configuration (opens nano, then reloads)
sudo argvus-firewall config

# Edit custom rules (opens nano, then reloads)
sudo argvus-firewall rules

# Show current rules
sudo argvus-firewall status
```

### systemd

```sh
sudo systemctl enable --now argvus-firewall
sudo systemctl status argvus-firewall
sudo systemctl reload argvus-firewall
```

## Arch Linux Packaging

### Build with makepkg (CI / release)

```sh
cd packaging/arch
makepkg -p PKGBUILD --nodeps --noconfirm --cleanbuild
```

### Build locally

```sh
make build
```

This uses `tools/build-local-package.sh` which:

1. Locates `packaging/arch/PKGBUILD.local`
2. Creates a source tarball from the working tree
3. Runs `makepkg -p PKGBUILD.local`
4. Moves the resulting `.pkg.tar.zst` to `dist/`

### Install the package

```sh
sudo pacman -U dist/argvus-firewall-*.pkg.tar.zst
```

## Validate

```sh
make validate
makepkg --printsrcinfo
```

## License

GPL-3.0-only -- see [LICENSE](LICENSE).
