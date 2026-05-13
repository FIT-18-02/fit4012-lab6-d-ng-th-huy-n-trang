# Report 1 page - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Dương Thị Huyền Trang
- Thành viên 2: Phạm Ánh Tuyết

## Mục tiêu

Mục tiêu của bài lab là xây dựng hệ thống gửi và nhận dữ liệu qua TCP Socket sử dụng thuật toán mã hóa AES-CBC. Hệ thống được chia thành hai kênh riêng biệt gồm key channel và data channel để mô phỏng quá trình trao đổi khóa và truyền ciphertext. Nhóm thực hiện mã hóa và giải mã dữ liệu bằng AES-CBC kết hợp PKCS#7 padding. Ngoài ra, bài lab còn yêu cầu xây dựng test kiểm thử cho các trường hợp đúng và sai, đồng thời phân tích các điểm yếu bảo mật của hệ thống khi truyền key dưới dạng plaintext.

## Phân công thực hiện

### Dương Thị Huyền Trang

- Phụ trách receiver.py
- Xử lý data channel
- Nhận và giải mã ciphertext
- Xử lý output file
- Hỗ trợ kiểm thử và sửa lỗi

### Phạm Ánh Tuyết

- Phụ trách sender.py
- Xử lý key channel
- Sinh AES key và IV
- Mã hóa AES-CBC
- Hỗ trợ integration test

### Phần làm chung

- Viết README.md
- Viết report và threat model
- Viết test trong thư mục tests/
- Tạo log minh chứng
- Kiểm thử toàn bộ hệ thống
  
## Cách làm

Sender sử dụng AES-CBC để mã hóa plaintext thành ciphertext trước khi gửi. Dữ liệu được padding bằng PKCS#7 để phù hợp block size AES. Hệ thống dùng 2 cổng TCP riêng:

- KEY_PORT gửi AES key và IV
- DATA_PORT gửi ciphertext

Mỗi packet đều có length header 4 byte để Receiver đọc đúng dữ liệu. Receiver sau khi nhận key, IV và ciphertext sẽ giải mã để khôi phục plaintext ban đầu.


## Kết quả

Hệ thống hoạt động thành công trên local machine. Receiver nhận và giải mã đúng plaintext từ Sender.

Các test đã chạy thành công gồm:

- Padding test
- AES-CBC test
- Key channel test
- Data channel test
- Wrong key test
- Tamper test
- Integration test Sender/Receiver

Log minh chứng được lưu trong thư mục logs/.

---
## Kết luận

Qua bài lab, nhóm hiểu rõ hơn về TCP Socket, AES-CBC, packet structure và kiểm thử hệ thống. Bài lab cũng cho thấy rằng mã hóa dữ liệu chưa đủ để đảm bảo an toàn nếu AES key và IV vẫn được gửi plaintext.
