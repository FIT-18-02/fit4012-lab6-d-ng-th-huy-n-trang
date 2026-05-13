import os
import socket
import time
from pathlib import Path

from aes_socket_utils import (
    build_data_packet,
    build_key_packet,
    encrypt_aes_cbc,
)

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
DATA_PORT = int(os.getenv("DATA_PORT", "6000"))
KEY_PORT = int(os.getenv("KEY_PORT", "6001"))

MESSAGE = os.getenv("MESSAGE", "")
INPUT_FILE = os.getenv("INPUT_FILE", "")
LOG_FILE = os.getenv("SENDER_LOG_FILE", "")


def send_packet(host: str, port: int, packet: bytes) -> None:
    """
    Gửi packet qua TCP socket.
    Có retry để tránh ConnectionRefusedError
    khi receiver chưa listen kịp.
    """
    for _ in range(10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(packet)
                return
        except ConnectionRefusedError:
            time.sleep(0.5)

    raise ConnectionRefusedError(
        f"Không thể kết nối tới {host}:{port}"
    )


def get_plaintext() -> bytes:
    """Lấy plaintext từ MESSAGE hoặc INPUT_FILE."""
    if INPUT_FILE:
        return Path(INPUT_FILE).read_bytes()

    return MESSAGE.encode("utf-8")


def main() -> None:
    plaintext = get_plaintext()

    key, iv, ciphertext = encrypt_aes_cbc(plaintext)

    key_packet = build_key_packet(key, iv)
    data_packet = build_data_packet(ciphertext)

    send_packet(SERVER_IP, KEY_PORT, key_packet)

    print("[+] Đã gửi key/IV qua kênh khóa.")

    send_packet(SERVER_IP, DATA_PORT, data_packet)

    print("[+] Đã gửi ciphertext qua kênh dữ liệu.")

    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")

    if LOG_FILE:
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

        Path(LOG_FILE).write_text(
            "\n".join([
                "[+] Đã gửi key/IV qua kênh khóa.",
                "[+] Đã gửi ciphertext qua kênh dữ liệu.",
                f"Key: {key.hex()}",
                f"IV: {iv.hex()}",
                f"Ciphertext: {ciphertext.hex()}",
            ]) + "\n",
            encoding="utf-8"
        )


if __name__ == "__main__":
    main()
