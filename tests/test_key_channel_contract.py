import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest
from aes_socket_utils import build_key_packet, parse_key_packet

# Test key channel với AES-128
def test_key_channel_contract_aes_128():
    key = b"a" * 16
    iv = b"b" * 16

    packet = build_key_packet(key, iv)

    assert packet[:4] == (16).to_bytes(4, "big")
    assert packet[4:20] == key
    assert packet[20:36] == iv

    parsed_key, parsed_iv = parse_key_packet(packet)

    assert parsed_key == key
    assert parsed_iv == iv


# Test key channel với AES-256
def test_key_channel_contract_aes_256():
    key = b"a" * 32
    iv = b"b" * 16

    packet = build_key_packet(key, iv)

    assert packet[:4] == (32).to_bytes(4, "big")

    parsed_key, parsed_iv = parse_key_packet(packet)

    assert parsed_key == key
    assert parsed_iv == iv


# Key AES chỉ hợp lệ khi dài 16 hoặc 32 byte
def test_invalid_key_size_should_fail():
    with pytest.raises(ValueError):
        build_key_packet(b"short", b"b" * 16)
