import os
import socket
from aes_socket_utils import (
    parse_key_packet,
    parse_length_header,
    decrypt_aes_cbc,
)

RECEIVER_HOST = os.getenv("RECEIVER_HOST", "127.0.0.1")
DATA_PORT = int(os.getenv("DATA_PORT", "6000"))
KEY_PORT = int(os.getenv("KEY_PORT", "6001"))
SOCKET_TIMEOUT = int(os.getenv("SOCKET_TIMEOUT", "10"))

key = None
iv = None


def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket closed")
        data += chunk
    return data


# ================= KEY CHANNEL =================
def handle_key_channel():
    global key, iv

    print("kênh khóa", flush=True)  

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((RECEIVER_HOST, KEY_PORT))
    server.listen(1)

    conn, _ = server.accept()

    try:
        raw_len = recv_exact(conn, 4)
        length = int.from_bytes(raw_len, "big")

        packet = recv_exact(conn, length)

        key, iv = parse_key_packet(raw_len + packet)

        print(f"Key: {key}", flush=True)
        print(f"IV: {iv}", flush=True)

    finally:
        conn.close()
        server.close()


# ================= DATA CHANNEL =================
def handle_data_channel():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((RECEIVER_HOST, DATA_PORT))
    server.listen(1)

    conn, _ = server.accept()

    try:
        raw_len = recv_exact(conn, 4)
        length = int.from_bytes(raw_len, "big")

        ciphertext = recv_exact(conn, length)

        plain = decrypt_aes_cbc(key, iv, ciphertext)

        print(f"[+] Bản tin gốc: {plain.decode()}", flush=True)

    finally:
        conn.close()
        server.close()


def main():

    handle_key_channel()
    handle_data_channel()


if __name__ == "__main__":
    main()
