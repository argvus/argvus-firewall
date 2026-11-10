---
title: Firewall
description: Überprüfen und steuern Sie den ARGVUS-Firewall-Dienst.
---
`argvus-firewall` bietet den Firewall-Befehl und den Systemdienst `argvus-firewall.service`. Die Konfiguration befindet sich unter `/etc/argvus/firewall/`.

Der Befehl unterstützt die operativen Aktionen `on`, `off`, `status`, `config`, `rules` und die strukturierte `manage`-Schnittstelle. Administrativen Änderungen kann eine Polkit-Autorisierung erforderlich sein.

Lokale TCP- und UDP-Ports werden mit `OPEN_PORTS_TCP` und `OPEN_PORTS_UDP` in `/etc/argvus/firewall/config.conf` geöffnet oder auf der Firewall-Verwaltungsseite des Kontrollzentrums als **TCP-Ports** und **UDP-Ports**. Jeder Wert ist eine durch Kommas getrennte Liste von Ports von 1 bis 65535, wie `3000,8080`. Leer bedeutet keine zusätzlichen Ports. Jeder Port akzeptiert NEUE Verbindungen auf beliebiger Schnittstelle.
