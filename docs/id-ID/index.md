---
title: Firewall
description: Periksa dan kendalikan layanan firewall ARGVUS.
---

`argvus-firewall` menyediakan perintah firewall dan layanan sistem `argvus-firewall.service`. Konfigurasinya berada di bawah `/etc/argvus/firewall/`.

Perintah ini mendukung tindakan operasional `on`, `off`, `status`, `config`, `rules` dan antarmuka terstruktur `manage`. Perubahan administratif mungkin memerlukan otorisasi polkit.

Port TCP dan UDP lokal dibuka dengan `OPEN_PORTS_TCP` dan `OPEN_PORTS_UDP` di `/etc/argvus/firewall/config.conf`, atau di halaman administrasi firewall Control Center sebagai **port TCP** dan **port UDP**. Setiap nilai adalah daftar port yang dipisahkan koma dari 1 hingga 65535, seperti `3000,8080`. Kosong berarti tidak ada port tambahan. Setiap port menerima koneksi BARU pada antarmuka apa pun.
