---
title: ファイアウォール
description: ARGVUSファイアウォールサービスを検査して制御してください。
---
`argvus-firewall` はファイアウォールコマンドとシステムサービス `argvus-firewall.service` を提供します。その設定は `/etc/argvus/firewall/` の下にあります。

ファイアウォールの設定とルールの編集は下書きに保持されます。保存すると両方が書き込まれ、サービスが再起動します。キャンセルで下書きを破棄し、再起動で保存済みのファイルを適用します。

このコマンドは、操作アクション `on`、`off`、`status`、`config`、`rules` と構造化された `manage` インターフェースをサポートしています。管理変更には polkit 認証が必要な場合があります。

ローカルの TCP および UDP ポートは、/etc/argvus/firewall/config.conf の `OPEN_PORTS_TCP` および `OPEN_PORTS_UDP`、またはコントロールセンターのファイアウォール管理ページで **TCP ポート**、**UDP ポート** として開かれます。各値は 1 から 65535 までのポートのカンマ区切りリストであり、例として  `/etc/argvus/firewall/config.conf` `3000,8080` があります。空の場合は追加ポートはありません。各ポートは任意のインターフェースでの NEW 接続を受け入れます。
