---
title: Firewall
description: Inspect and control the ARGVUS firewall service.
---

`argvus-firewall` provides the firewall command and the system service `argvus-firewall.service`. Its configuration is under `/etc/argvus/firewall/`.

The command supports the operational actions `on`, `off`, `status`, `config`, `rules` and the structured `manage` interface. Administrative changes may request polkit authorization.
