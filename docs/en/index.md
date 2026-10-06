---
title: Firewall
description: Inspect and control the ARGVUS firewall service.
---

`argvus-firewall` provides the firewall command and the system service `argvus-firewall.service`. Its configuration is under `/etc/argvus/firewall/`.

The command supports the operational actions `on`, `off`, `status`, `config`, `rules` and the structured `manage` interface. Administrative changes may request polkit authorization.

Local TCP and UDP ports are opened with `OPEN_PORTS_TCP` and `OPEN_PORTS_UDP` in `/etc/argvus/firewall/config.conf`, or in the Control Center firewall administration page as **TCP ports** and **UDP ports**. Each value is a comma-separated list of ports from 1 to 65535, such as `3000,8080`. Empty means no extra ports. Each port accepts NEW connections on any interface.
