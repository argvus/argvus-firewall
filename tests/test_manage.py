import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('manage', ROOT / 'src/usr/lib/argvus-firewall/manage.py')
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)


class ConfigTests(unittest.TestCase):
    def test_packaged_config_round_trips_all_fields(self):
        original = (ROOT / 'src/etc/argvus/firewall/config.conf').read_text()
        config = manage.parse_config(original)
        self.assertEqual(set(config), set(manage.DEFAULTS))
        self.assertEqual(manage.parse_config(manage.render_config(original, config)), config)

    def test_rejects_injection_and_invalid_values(self):
        for key, value in [('SSH_PORT', '22;id'), ('SSH_PORT', '0'), ('SSH_PORT', '65536'),
                           ('INTERFACE_WAN', '$(id)'), ('ALLOW_SSH', 'true'),
                           ('SSH_CLIENTS_IP', '::1'), ('SAMBA_CLIENTS_IP', '1.2.3.4\n'),
                           ('OPEN_PORTS_UDP', '53,bad'), ('PROTECTION_LEVEL', 'unknown')]:
            with self.subTest(key=key, value=value):
                with self.assertRaises(ValueError):
                    manage.validate(dict(manage.DEFAULTS, **{key: value}))

    def test_masquerading_requires_wan(self):
        with self.assertRaises(ValueError):
            manage.validate(dict(manage.DEFAULTS, MASQUERADE_ENABLE='y'))
        manage.validate(dict(manage.DEFAULTS, MASQUERADE_ENABLE='y', INTERFACE_WAN='eth0'))

    def test_networks_and_ports(self):
        manage.validate(dict(manage.DEFAULTS, SSH_CLIENTS_IP='192.168.1.0/24,10.0.0.2', OPEN_PORTS_UDP='53,443'))

    def test_rejects_unknown_fields_and_shell_statements(self):
        for contents in ['exec id', 'UNKNOWN="x"', 'ALLOW_SSH="y"; id', 'SSH_PORT="$(id)"']:
            with self.assertRaises(ValueError):
                manage.parse_config(contents)

    def test_atomic_write_refuses_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config'
            other = Path(directory) / 'other'
            other.write_text('preserved')
            path.symlink_to(other)
            with self.assertRaises(ValueError):
                manage.atomic_write(path, 'replacement')
            self.assertEqual(other.read_text(), 'preserved')

    def test_mutations_require_root(self):
        with patch.object(manage.os, 'geteuid', return_value=1000):
            with self.assertRaises(PermissionError):
                manage.handle({'action': 'stop'})

    def test_save_rules_validates_and_detects_stale_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'rules.fw'
            path.write_text('# original\n')
            lock = Path(directory) / 'lock'
            real_open = open
            def local_open(name, *args, **kwargs):
                return real_open(lock if name == '/run/lock/argvus-firewall-config.lock' else name, *args, **kwargs)
            with patch.object(manage, 'RULES', path), patch.object(manage.os, 'geteuid', return_value=0), patch('builtins.open', side_effect=local_open):
                with self.assertRaises(ValueError):
                    manage.handle({'action': 'save-rules', 'original': 'stale', 'rules': 'id'})
                with self.assertRaises(ValueError):
                    manage.handle({'action': 'save-rules', 'original': '# original\n', 'rules': 'if then'})
                self.assertEqual(path.read_text(), '# original\n')
                manage.handle({'action': 'save-rules', 'original': '# original\n', 'rules': '# saved\n'})
                self.assertEqual(path.read_text(), '# saved\n')
                self.assertEqual(path.stat().st_mode & 0o777, 0o644)

    def test_invalid_json_is_reported_without_execution(self):
        output = subprocess.run(['/usr/bin/python3', '-I', str(ROOT / 'src/usr/lib/argvus-firewall/manage.py')], input='not json', text=True, capture_output=True)
        self.assertNotEqual(output.returncode, 0)

    def test_rule_order_allows_custom_rules_and_only_blocks_repeated_scans(self):
        script = (ROOT / 'src/usr/bin/argvus-firewall').read_text()
        self.assertNotIn('$IPTABLES -A INPUT -j PORTSCAN', script)
        self.assertIn('--rcheck --seconds 60 --hitcount 10 -j PORTSCAN', script)
        self.assertNotIn('--limit 60/s --limit-burst 20 -j ACCEPT', script)
        self.assertLess(script.index('. "$RULES_FILE"'), script.index('$IPTABLES -A INPUT -j LOG_DROPPED'))

    def test_failed_apply_restores_both_families_and_does_not_save(self):
        script = (ROOT / 'src/usr/bin/argvus-firewall').read_text()
        functions = script[script.index('_rollback() {'):script.index('### Options')]
        with tempfile.TemporaryDirectory() as directory:
            functions = functions.replace('/run/argvus-firewall.XXXXXX', directory + '/snapshot.XXXXXX')
            functions = functions.replace('/usr/bin/iptables-restore', 'restore4').replace('/usr/bin/ip6tables-restore', 'restore6')
            fixture = '''
_check_config() { :; }
save4() { echo ipv4-snapshot; }
save6() { echo ipv6-snapshot; }
restore4() { cat; }
restore6() { cat; }
_off() { :; }
_on() { false; echo SHOULD-NOT-CONTINUE; }
_save() { echo SHOULD-NOT-SAVE; }
IPTABLES_SAVE=save4
IP6TABLES_SAVE=save6
'''
            output = subprocess.run(['/usr/bin/sh'], input=fixture + functions + '\nset -e\n_apply\n', text=True, capture_output=True)
            self.assertNotEqual(output.returncode, 0)
            self.assertEqual(output.stdout.splitlines(), ['ipv4-snapshot', 'ipv6-snapshot'])
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
