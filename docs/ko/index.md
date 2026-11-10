---
title: 방화벽
description: ARGVUS 방화벽 서비스를 점검하고 제어하십시오.
---
`argvus-firewall`는 방화벽 명령과 시스템 서비스 `argvus-firewall.service`를 제공합니다. 그 구성은 `/etc/argvus/firewall/`에 있습니다.

이 명령은 운영 작업 `on`, `off`, `status`, `config`, `rules`와 구조화된 `manage` 인터페이스를 지원합니다. 관리 변경은 polkit 권한 승인을 요구할 수 있습니다.

로컬 TCP 및 UDP 포트는 /etc/argvus/firewall/config.conf에서 `OPEN_PORTS_TCP`와 `OPEN_PORTS_UDP`로 열리거나, 제어 센터 방화벽 관리 페이지에서 **TCP 포트** 및 **UDP 포트**로 열릴 수 있습니다. 각 값은 1부터 65535까지의 포트가 쉼표로 구분된 목록이며, 예를 들어  `/etc/argvus/firewall/config.conf` `3000,8080`과 같습니다. 비어 있으면 추가 포트가 없음을 의미합니다. 각 포트는 모든 인터페이스에서 NEW 연결을 허용합니다.
