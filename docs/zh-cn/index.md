---
title: 防火墙
description: 检查并控制 ARGVUS 防火墙服务。
---
`argvus-firewall` 提供防火墙命令和系统服务 `argvus-firewall.service`。其配置位于 `/etc/argvus/firewall/`。

该命令支持操作动作 `on`、`off`、`status`、`config`、`rules` 以及结构化的 `manage` 接口。管理更改可能需要 polkit 授权。

本地 TCP 和 UDP 端口可通过 `OPEN_PORTS_TCP` 和 `OPEN_PORTS_UDP` 在 `/etc/argvus/firewall/config.conf` 中打开，或在控制中心防火墙管理页面中作为 **TCP 端口** 和 **UDP 端口** 设置。每个值都是 1 到 65535 之间端口的逗号分隔列表，例如 `3000,8080`。为空表示没有额外端口。每个端口都允许在任何接口上建立新的连接。
