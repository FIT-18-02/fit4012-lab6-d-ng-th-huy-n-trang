# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Dương Thị Huyền Trang
- Thành viên 2: Phạm Ánh Tuyết 

## Assets

 Dương Thị Huyền Trang: Liệt kê tài sản cần bảo vệ, ví dụ plaintext, AES key, IV, ciphertext, file đầu vào, file đầu ra và log.
 Các tài sản cần bảo vệ gồm:

- Plaintext trước khi mã hóa
- AES key
- IV
- Ciphertext
- File input và output
- Log hệ thống Sender/Receiver

## Attacker model

Phạm Ánh Tuyết : Mô tả đối tượng tấn công có thể nghe lén mạng LAN, bắt gói tin, sửa ciphertext, replay packet hoặc đọc log.
Kẻ tấn công có thể:

- Nghe lén mạng LAN
- Bắt gói tin TCP
- Sửa đổi ciphertext
- Gửi lại packet cũ (replay)
- Đọc file log nếu có quyền truy cập

---

## Threats

## Thành viên 1 - Dương Thị Huyền Trang
- Key disclosure do AES key và IV được gửi plaintext qua key channel
- Tampering do ciphertext có thể bị sửa đổi khi truyền
- Replay attack do packet cũ có thể bị gửi lại nhiều lần

## Thành viên 2 - Phạm Ánh Tuyết
- Log leakage do key hoặc IV có thể xuất hiện trong log
- No authentication do Receiver chưa xác thực Sender
- Có nguy cơ đọc được dữ liệu nếu attacker chiếm được key

---
## Mitigations

## Thành viên 1 - Dương Thị Huyền Trang

- Không gửi key plaintext trong hệ thống thực tế
- Sử dụng TLS hoặc cơ chế trao đổi khóa an toàn
- Không lưu key thật trong log

## Thành viên 2 - Phạm Ánh Tuyết

- Sử dụng AES-GCM để tăng tính toàn vẹn dữ liệu
- Thêm nonce hoặc timestamp để giảm replay attack
- Thêm cơ chế xác thực Sender và Receiver

---
## Residual risks

 Dương Thị Huyền Trang: Nêu ít nhất 1 rủi ro còn lại, ví dụ hệ thống vẫn chưa an toàn vì key channel chỉ là mô phỏng, chưa có TLS, chưa có xác thực và chưa chống replay đầy đủ.
 
Hệ thống vẫn chưa an toàn hoàn toàn vì key channel chỉ mang tính mô phỏng học tập. Hiện tại chưa có TLS, chưa có xác thực đầy đủ và chưa chống replay hoàn chỉnh nên vẫn có nguy cơ bị tấn công trong môi trường thực tế.
