---
title: Güvenlik Duvarı
description: ARGVUS güvenlik duvarı hizmetini inceleyin ve kontrol edin.
---

`argvus-firewall`, güvenlik duvarı komutunu ve `argvus-firewall.service` sistem hizmetini sağlar. Yapılandırması `/etc/argvus/firewall/` altında bulunur.

Komut, `on`, `off`, `status`, `config`, `rules` operasyonel eylemlerini ve yapılandırılmış `manage` arayüzünü destekler. Yönetimsel değişiklikler polkit yetkilendirmesi gerektirebilir.

Yerel TCP ve UDP portları, /etc/argvus/firewall/config.conf'de `OPEN_PORTS_TCP` ve `OPEN_PORTS_UDP` ile veya Kontrol Merkezi güvenlik duvarı yönetim sayfasında **TCP portları** ve **UDP portları** olarak açılır. Her değer,  `/etc/argvus/firewall/config.conf` `3000,8080` gibi 1 ila 65535 arası portların virgülle ayrılmış bir listesidir. Boş olması ekstra port olmadığını gösterir. Her port, herhangi bir arayüzde YENİ bağlantıları kabul eder.
