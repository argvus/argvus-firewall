---
title: Firewall
description: Kiểm tra và điều khiển dịch vụ tường lửa ARGVUS.
---

`argvus-firewall` cung cấp lệnh tường lửa và dịch vụ hệ thống `argvus-firewall.service`. Cấu hình của nó nằm dưới `/etc/argvus/firewall/`.

Lệnh này hỗ trợ các hành động vận hành `on`, `off`, `status`, `config`, `rules` và giao diện có cấu trúc `manage`. Các thay đổi hành chính có thể yêu cầu ủy quyền polkit.

Các cổng TCP và UDP cục bộ được mở với `OPEN_PORTS_TCP` và `OPEN_PORTS_UDP` trong `/etc/argvus/firewall/config.conf`, hoặc trong trang quản lý tường lửa của Trung tâm Điều khiển như **cổng TCP** và **cổng UDP**. Mỗi giá trị là danh sách các cổng cách nhau bằng dấu phẩy từ 1 đến 65535, chẳng hạn như `3000,8080`. Trống có nghĩa là không có cổng bổ sung. Mỗi cổng chấp nhận các kết nối MỚI trên bất kỳ giao diện nào.
