#!/usr/bin/env bash
# shellcheck shell=bash
# shellcheck disable=SC2154
# srcdir, pkgdir, pkgname, and pkgver are supplied by makepkg.

arch_normalize_source_tree() {
	local expected="${srcdir}/${pkgname}-${pkgver}"
	local -a roots=()

	while IFS= read -r -d '' root; do
		roots+=("$root")
	done < <(find "$srcdir" -mindepth 1 -maxdepth 1 -type d -print0)

	if (( ${#roots[@]} != 1 )); then
		printf 'error: expected exactly one extracted source directory in %s\n' "$srcdir" >&2
		return 1
	fi

	if [[ "${roots[0]}" != "$expected" ]]; then
		[[ ! -e "$expected" ]] || {
			printf 'error: source destination already exists: %s\n' "$expected" >&2
			return 1
		}
		mv -- "${roots[0]}" "$expected"
	fi
}

arch_check_firewall_payload() {
	local source_root="${srcdir}/${pkgname}-${pkgver}"

	test -x "${source_root}/src/usr/bin/argvus-firewall"
	test -f "${source_root}/src/usr/lib/argvus-firewall/manage.py"
	test -f "${source_root}/src/usr/lib/systemd/system/argvus-firewall.service"
	sh -n "${source_root}/src/usr/bin/argvus-firewall"
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s "${source_root}/tests"
}

arch_package_firewall_payload() {
	local source_root="${srcdir}/${pkgname}-${pkgver}"

	install -Dm755 "${source_root}/src/usr/bin/argvus-firewall" \
		"${pkgdir}/usr/bin/argvus-firewall"
	install -Dm644 "${source_root}/src/usr/lib/argvus-firewall/manage.py" \
		"${pkgdir}/usr/lib/argvus-firewall/manage.py"
	install -Dm644 "${source_root}/src/etc/argvus/firewall/config.conf" \
		"${pkgdir}/etc/argvus/firewall/config.conf"
	install -Dm644 "${source_root}/src/etc/argvus/firewall/rules.fw" \
		"${pkgdir}/etc/argvus/firewall/rules.fw"
	install -Dm644 "${source_root}/src/usr/lib/systemd/system/argvus-firewall.service" \
		"${pkgdir}/usr/lib/systemd/system/argvus-firewall.service"
	install -Dm644 "${source_root}/LICENSE" \
		"${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
