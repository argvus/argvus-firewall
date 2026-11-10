---
title: Pare-feu
description: Inspecter et contrôler le service de pare-feu ARGVUS.
---
`argvus-firewall` fournit la commande de pare-feu et le service système `argvus-firewall.service`. Sa configuration se trouve sous `/etc/argvus/firewall/`.

La commande prend en charge les actions opérationnelles `on`, `off`, `status`, `config`, `rules` et l'interface structurée `manage`. Les modifications administratives peuvent nécessiter une autorisation polkit.

Les ports TCP et UDP locaux sont ouverts avec `OPEN_PORTS_TCP` et `OPEN_PORTS_UDP` dans `/etc/argvus/firewall/config.conf`, ou dans la page d'administration du pare-feu du Centre de Contrôle en tant que **ports TCP** et **ports UDP**. Chaque valeur est une liste de ports séparés par des virgules allant de 1 à 65535, comme `3000,8080`. Vide signifie aucun port supplémentaire. Chaque port accepte les nouvelles connexions sur n'importe quelle interface.
