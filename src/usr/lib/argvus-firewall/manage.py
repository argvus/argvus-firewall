#!/usr/bin/python3
"""Structured configuration API; called by argvus-firewall manage."""
import fcntl
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

CONFIG = Path('/etc/argvus/firewall/config.conf')
RULES = Path('/etc/argvus/firewall/rules.fw')
DEFAULTS = {
    'INTERFACE_WAN': '', 'INTERFACE_LAN': '', 'MASQUERADE_ENABLE': 'n',
    'PROTECTION_LEVEL': 'high', 'ALLOW_SSH': 'n', 'SSH_CLIENTS_IP': '',
    'SSH_PORT': '22', 'ALLOW_SAMBA': 'n', 'SAMBA_CLIENTS_IP': '',
    'ALLOW_ICMP': 'y', 'OPEN_PORTS_UDP': '', 'SYN_FLOOD_PROTECTION': 'y',
    'DDOS_PROTECTION': 'y', 'PORT_SCAN_PROTECTION': 'y', 'ANTI_SPOOFING': 'y',
}
BOOLS = {key for key, value in DEFAULTS.items() if value in ('y', 'n')}


def validate(values):
    if set(values) != set(DEFAULTS) or not all(isinstance(v, str) for v in values.values()):
        raise ValueError('configuration must contain exactly the supported fields')
    for key, value in values.items():
        if any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise ValueError(f'{key}: control characters are not allowed')
        if key in BOOLS and value not in ('y', 'n'):
            raise ValueError(f'{key}: expected y or n')
        if key.startswith('INTERFACE_') and value and not re.fullmatch(r'[a-zA-Z0-9_.:-]{1,15}', value):
            raise ValueError(f'{key}: invalid interface')
        if key.endswith('_CLIENTS_IP') and value:
            for network in value.split(','):
                if ipaddress.ip_network(network.strip(), strict=False).version != 4:
                    raise ValueError(f'{key}: only IPv4 networks are supported')
        if key in ('SSH_PORT', 'OPEN_PORTS_UDP'):
            ports = value.split(',') if key == 'OPEN_PORTS_UDP' and value else [value]
            for port in ports:
                if key == 'OPEN_PORTS_UDP' and not value:
                    continue
                if not port.strip().isascii() or not port.strip().isdigit() or not 1 <= int(port) <= 65535:
                    raise ValueError(f'{key}: expected ports between 1 and 65535')
    if values['PROTECTION_LEVEL'] not in ('low', 'medium', 'high', 'paranoid'):
        raise ValueError('invalid protection level')
    if values['MASQUERADE_ENABLE'] == 'y' and not values['INTERFACE_WAN']:
        raise ValueError('masquerading requires a WAN interface')


def parse_config(text):
    values = dict(DEFAULTS)
    for line in text.splitlines():
        tokens = shlex.split(line, comments=True)
        if not tokens:
            continue
        if len(tokens) != 1 or '=' not in tokens[0]:
            raise ValueError('unsupported config syntax; expected KEY="value"')
        key, value = tokens[0].split('=', 1)
        if key not in DEFAULTS:
            raise ValueError(f'unsupported configuration field: {key}')
        values[key] = value
    validate(values)
    return values


def render_config(original, values):
    validate(values)
    seen = set()
    lines = []
    for line in original.splitlines():
        match = re.match(r'\s*([A-Z_]+)=', line)
        if match and match[1] in values:
            key = match[1]
            # Values are validated identifiers, ports, networks or enum values.
            lines.append(f'{key}="{values[key]}"')
            seen.add(key)
        else:
            lines.append(line)
    lines.extend(f'{key}="{value}"' for key, value in values.items() if key not in seen)
    return '\n'.join(lines) + '\n'


def atomic_write(path, content):
    if path.is_symlink():
        raise ValueError('refusing to replace a symlink')
    fd, temporary = tempfile.mkstemp(prefix='.control-center-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as output:
            os.fchmod(output.fileno(), 0o644)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run(*args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError((result.stderr or result.stdout or 'operation failed').strip())
    return result.stdout.strip()


def handle(request):
    action = request['action']
    if action == 'snapshot':
        config = CONFIG.read_text()
        return {'config': parse_config(config), 'config_text': config, 'rules': RULES.read_text(),
                'active': subprocess.run(['/usr/bin/systemctl', 'is-active', '--quiet', 'argvus-firewall.service'], check=False).returncode == 0,
                'enabled': subprocess.run(['/usr/bin/systemctl', 'is-enabled', '--quiet', 'argvus-firewall.service'], check=False).returncode == 0}
    if os.geteuid() != 0:
        raise PermissionError('administration requires pkexec argvus-firewall manage')
    with open('/run/lock/argvus-firewall-config.lock', 'a', encoding='utf-8') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if action in ('save-config', 'save-rules'):
            path = CONFIG if action == 'save-config' else RULES
            current = path.read_text()
            if request['original'] != current:
                raise ValueError('file changed since loading; reload before saving')
            if action == 'save-config':
                content = render_config(current, request['config'])
            else:
                content = request['rules']
                if not isinstance(content, str) or '\0' in content or len(content.encode()) > 262144:
                    raise ValueError('invalid rules document')
                syntax = subprocess.run(['/usr/bin/sh', '-n'], input=content, capture_output=True, text=True, check=False)
                if syntax.returncode:
                    raise ValueError(syntax.stderr)
            atomic_write(path, content)
        elif action in ('start', 'stop', 'restart', 'enable', 'disable'):
            run('/usr/bin/systemctl', 'reload-or-restart' if action == 'restart' else action, 'argvus-firewall.service')
        else:
            raise ValueError('unsupported operation')
    return {'ok': True}


def main():
    try:
        if sys.argv[1:] == ['--check-files']:
            parse_config(CONFIG.read_text())
            run('/usr/bin/sh', '-n', str(RULES))
            return 0
        raw = sys.stdin.buffer.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('request too large')
        print(json.dumps(handle(json.loads(raw))))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
