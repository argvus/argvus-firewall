# Arch packaging layout

This project keeps separate PKGBUILDs for local and tagged release builds:

| Path | Use | Source |
| --- | --- | --- |
| `local/PKGBUILD` | `make build` from the working tree | generated local archive |
| `ci/PKGBUILD` | tagged release | GitHub tag archive |

The package metadata and payload checks are equivalent. Only the source
definition and checksum handling differ. Shared source normalization and
payload installation live in `common/functions.sh`.

The installation hook is kept in `common/argvus-firewall.install` and is
referenced by both PKGBUILDs. Do not commit generated `src/`, `pkg/`, archives,
or packages.

Inspect metadata without building:

```sh
makepkg -p packaging/arch/ci/PKGBUILD --printsrcinfo
makepkg -p packaging/arch/local/PKGBUILD --printsrcinfo
```
