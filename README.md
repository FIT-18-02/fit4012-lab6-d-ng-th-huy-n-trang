[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/pP7_NUvP)
# FIT4012 - Lab 6 - Hệ thống gửi và nhận dữ liệu mã hóa AES-CBC qua Socket

Repo starter kit này dùng cho **Lab 6**: gửi và nhận dữ liệu mã hóa bằng **AES-CBC** qua **TCP socket**.

Lab này kế thừa ý tưởng từ Lab 3 DES Socket, nhưng nâng cấp theo 2 hướng:

1. Chuyển từ **DES-CBC** sang **AES-CBC**.
2. Tách thành **2 kênh TCP**:
   - `KEY_PORT`: kênh giả lập trao đổi AES key và IV.
   - `DATA_PORT`: kênh gửi ciphertext.

> Lưu ý quan trọng: kênh khóa trong bài này chỉ là mô phỏng học tập. Key và IV vẫn được gửi plaintext, vì vậy thiết kế này **không an toàn để dùng trong hệ thống thật**.

---

## Team members

- **Thành viên 1**: TODO_MEMBER_1 - MSSV: TODO_MEMBER_1_ID
- **Thành viên 2**: TODO_MEMBER_2 - MSSV: TODO_MEMBER_2_ID

## Task division

- **Thành viên 1 phụ trách chính**: TODO_ROLE_MEMBER_1
- **Thành viên 2 phụ trách chính**: TODO_ROLE_MEMBER_2
- **Phần làm chung**: TODO_SHARED_WORK

## Demo roles

- **Demo Sender / kênh khóa / log gửi**: TODO_DEMO_ROLE_1
- **Demo Receiver / kênh dữ liệu / giải mã**: TODO_DEMO_ROLE_2
- **Cả hai cùng trả lời threat model và ethics**: TODO_DEMO_ROLE_SHARED

---

## Mục tiêu học tập

Sau bài lab này, sinh viên có thể:

- Mô tả được luồng Sender/Receiver qua TCP socket.
- Phân biệt được kênh khóa và kênh dữ liệu.
- Cài đặt được AES-CBC với key, IV và PKCS#7 padding.
- Thiết kế được header độ dài cho dữ liệu truyền qua socket.
- Viết test cho các tình huống đúng và sai.
- Nhận diện được điểm yếu của việc gửi key/IV plaintext.

---

## Cấu trúc repo

```text
.
├── aes_socket_utils.py
├── sender.py
├── receiver.py
├── requirements.txt
├── sample_input.txt
├── sample_output.txt
├── report-1page.md
├── threat-model-1page.md
├── peer-review-response.md
├── logs/
├── tests/
└── .github/workflows/ci.yml
```

---

## Protocol

### 1. Key channel

Sender gửi AES key và IV qua `KEY_PORT`.

```text
[key_length: 4 bytes][key: 16 hoặc 32 bytes][iv: 16 bytes]
```

### 2. Data channel

Sender gửi ciphertext qua `DATA_PORT`.

```text
[ciphertext_length: 4 bytes][ciphertext: N bytes]
```

---

## Cài đặt môi trường

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Chạy demo local

### Terminal 1 - Receiver

```bash
RECEIVER_HOST=127.0.0.1 DATA_PORT=6000 KEY_PORT=6001 python receiver.py
```

### Terminal 2 - Sender

```bash
SERVER_IP=127.0.0.1 DATA_PORT=6000 KEY_PORT=6001 MESSAGE="Xin chao FIT4012 - Lab 6 AES Socket" python sender.py
```

---

## Chạy có log minh chứng

Terminal 1:

```bash
RECEIVER_HOST=127.0.0.1 \
DATA_PORT=6000 \
KEY_PORT=6001 \
RECEIVER_LOG_FILE=logs/receiver_success.log \
OUTPUT_FILE=sample_output.txt \
python receiver.py
```

Terminal 2:

```bash
SERVER_IP=127.0.0.1 \
DATA_PORT=6000 \
KEY_PORT=6001 \
MESSAGE="Xin chao FIT4012 - Lab 6 AES Socket" \
SENDER_LOG_FILE=logs/sender_success.log \
python sender.py
```

---

## Gửi dữ liệu từ file

Terminal 1:

```bash
RECEIVER_HOST=127.0.0.1 DATA_PORT=6000 KEY_PORT=6001 OUTPUT_FILE=sample_output.txt python receiver.py
```

Terminal 2:

```bash
SERVER_IP=127.0.0.1 DATA_PORT=6000 KEY_PORT=6001 INPUT_FILE=sample_input.txt python sender.py
```

---

## Chạy test

```bash
pytest -q
```

---

## Deliverables bắt buộc

- `README.md`
- `sender.py`
- `receiver.py`
- `aes_socket_utils.py`
- `tests/`
- `logs/`
- `report-1page.md`
- `threat-model-1page.md`
- `sample_input.txt`
- `sample_output.txt`

---

## Submission contract cho CI

CI sẽ kiểm tra:

- Có đủ file bắt buộc.
- Không còn import `DES`.
- Có sử dụng `AES`.
- Có ít nhất 6 test.
- Có test padding.
- Có test key channel.
- Có test data channel.
- Có test wrong key.
- Có test tamper.
- Có test local sender-receiver.
- README có thông tin nhóm 2 người.
- Các file báo cáo không còn `TODO_STUDENT`.
- Có ít nhất 1 file log thật trong `logs/`.

---

## Ethics & Safe use

- Chỉ chạy demo trên máy cá nhân, VM hoặc mạng nội bộ phục vụ học tập.
- Không quét cổng hoặc thử nghiệm trên hệ thống không được phép.
- Không dùng dữ liệu cá nhân thật hoặc dữ liệu nhạy cảm để demo.
- Không trình bày hệ thống này như một giải pháp an toàn sẵn sàng triển khai thực tế.
- Nếu tham khảo code/tài liệu, hãy ghi nguồn rõ ràng.

---

## Bài học chính

Một hệ thống có mã hóa chưa chắc đã là một hệ thống an toàn.

AES-CBC giúp che nội dung plaintext, nhưng chưa tự động đảm bảo xác thực, toàn vẹn, chống replay hay bảo vệ key.
