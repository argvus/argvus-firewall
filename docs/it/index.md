---
title: Firewall
description: Ispezionare e controllare il servizio firewall ARGVUS.
---
`argvus-firewall` fornisce il comando del firewall e il servizio di sistema `argvus-firewall.service`. La sua configurazione si trova sotto `/etc/argvus/firewall/`.

Il comando supporta le azioni operative `on`, `off`, `status`, `config`, `rules` e l'interfaccia strutturata `manage`. Le modifiche amministrative possono richiedere l'autorizzazione polkit.

Le porte TCP e UDP locali vengono aperte con `OPEN_PORTS_TCP` e `OPEN_PORTS_UDP` in `/etc/argvus/firewall/config.conf`, o nella pagina di amministrazione del firewall del Centro di Controllo come **porte TCP** e **porte UDP**. Ogni valore è una lista separata da virgola di porte da 1 a 65535, come `3000,8080`. Vuoto significa nessuna porta aggiuntiva. Ogni porta accetta nuove connessioni su qualsiasi interfaccia.
