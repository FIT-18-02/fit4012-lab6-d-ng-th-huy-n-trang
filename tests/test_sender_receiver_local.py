import os
import socket
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_output(process, text: str, timeout: float = 5.0) -> str:
    collected = []
    start = time.time()
    while time.time() - start < timeout:
        line = process.stdout.readline()
        if line:
            collected.append(line)
            if text in line:
                return "".join(collected)
    raise AssertionError(f"Không thấy output '{text}'. Output đã nhận: {''.join(collected)}")


def test_local_sender_receiver_roundtrip():
    data_port = find_free_port()
    key_port = find_free_port()

    receiver_env = os.environ.copy()
    receiver_env.update({
        "PYTHONUNBUFFERED": "1",
        "RECEIVER_HOST": "127.0.0.1",
        "DATA_PORT": str(data_port),
        "KEY_PORT": str(key_port),
        "SOCKET_TIMEOUT": "5",
    })

    sender_env = os.environ.copy()
    sender_env.update({
        "PYTHONUNBUFFERED": "1",
        "SERVER_IP": "127.0.0.1",
        "DATA_PORT": str(data_port),
        "KEY_PORT": str(key_port),
        "MESSAGE": "Xin chao FIT4012 - local AES integration test",
    })

    receiver = subprocess.Popen(
        [sys.executable, "-u", "receiver.py"],
        cwd=REPO_ROOT,
        env=receiver_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

   try:
    time.sleep(2)

    first_output = wait_for_output(receiver, "kênh khóa")

        sender = subprocess.run(
            [sys.executable, "sender.py"],
            cwd=REPO_ROOT,
            env=sender_env,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        receiver_out, _ = receiver.communicate(timeout=10)
        full_receiver_output = first_output + receiver_out

        assert "[+] Đã gửi key/IV qua kênh khóa." in sender.stdout
        assert "[+] Đã gửi ciphertext qua kênh dữ liệu." in sender.stdout
        assert "Key:" in sender.stdout
        assert "IV:" in sender.stdout
        assert "Ciphertext:" in sender.stdout
        assert "[+] Bản tin gốc: Xin chao FIT4012 - local AES integration test" in full_receiver_output

    finally:
        if receiver.poll() is None:
            receiver.kill()
