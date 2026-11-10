---
title: Cortafuegos
description: Inspeccione y controle el servicio de firewall ARGVUS.
---
`argvus-firewall` proporciona el comando de firewall y el servicio del sistema `argvus-firewall.service`. Su configuración está bajo `/etc/argvus/firewall/`.

El comando soporta las acciones operativas `on`, `off`, `status`, `config`, `rules` y la interfaz estructurada `manage`. Los cambios administrativos pueden requerir autorización polkit.

Los puertos TCP y UDP locales se abren con `OPEN_PORTS_TCP` y `OPEN_PORTS_UDP` en `/etc/argvus/firewall/config.conf`, o en la página de administración del firewall del Centro de Control como **puertos TCP** y **puertos UDP**. Cada valor es una lista de puertos separados por comas, del 1 al 65535, como `3000,8080`. Vacío significa que no hay puertos adicionales. Cada puerto acepta conexiones NUEVAS en cualquier interfaz.
