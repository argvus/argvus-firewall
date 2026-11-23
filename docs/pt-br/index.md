---
title: Firewall
description: Consulte e controle o firewall ARGVUS.
---

O **Firewall** mantém as alterações de configuração e regras em um rascunho. **Salvar** grava ambas e reinicia o serviço. **Cancelar** descarta o rascunho. **Reiniciar** aplica os arquivos salvos. Use `Tab` para focar a barra de ações.

`argvus-firewall` fornece o comando e o serviço `argvus-firewall.service`. A configuração fica em `/etc/argvus/firewall/`. As ações incluem `on`, `off`, `status`, `config`, `rules` e `manage`; alterações administrativas podem solicitar autorização polkit.

Portas TCP e UDP locais são abertas com `OPEN_PORTS_TCP` e `OPEN_PORTS_UDP` em `/etc/argvus/firewall/config.conf`, ou na página de administração do firewall no Control Center, como **Portas TCP** e **Portas UDP**. Cada valor é uma lista separada por vírgulas de portas de 1 a 65535, como `3000,8080`. Vazio significa nenhuma porta extra. Cada porta aceita conexões NEW em qualquer interface.
