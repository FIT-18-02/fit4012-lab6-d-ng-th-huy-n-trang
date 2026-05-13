import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from aes_socket_utils import (
    build_data_packet,
    build_key_packet,
    encrypt_aes_cbc,
    parse_key_packet,
    parse_length_header,
    pad,
    unpad,
)
# Sau khi pad rồi unpad phải trả về dữ liệu ban đầu
def test_pad_unpad_roundtrip():
    data = b"hello AES socket"
    assert unpad(pad(data)) == data


# Test AES-CBC encrypt hoạt động đúng
# Ciphertext phải có độ dài là bội số của block size 16 byte
def test_aes_cbc_roundtrip():
    plain = b"FIT4012 Lab 6 AES-CBC"
    key, iv, cipher_bytes = encrypt_aes_cbc(
        plain,
        key=b"1" * 16,
        iv=b"2" * 16
    )

    assert len(key) == 16
    assert len(iv) == 16
    assert len(cipher_bytes) % 16 == 0


# Test build và parse key packet đúng dữ liệu ban đầu
def test_key_packet_roundtrip():
    key = b"1" * 16
    iv = b"2" * 16

    packet = build_key_packet(key, iv)
    parsed_key, parsed_iv = parse_key_packet(packet)

    assert parsed_key == key
    assert parsed_iv == iv


# Test data packet chứa đúng length header và ciphertext
def test_data_packet_contains_correct_length():
    _, _, cipher_bytes = encrypt_aes_cbc(
        b"FIT4012",
        key=b"1" * 16,
        iv=b"2" * 16
    )

    packet = build_data_packet(cipher_bytes)

    length = parse_length_header(packet[:4])

    assert length == len(cipher_bytes)
    assert packet[4:] == cipher_bytes
