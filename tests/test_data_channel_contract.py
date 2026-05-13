import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest
from aes_socket_utils import build_data_packet, parse_length_header

# Test packet trên data channel đúng format:
# [ciphertext_length][ciphertext]
def test_data_channel_contract():
    ciphertext = b"x" * 32

    packet = build_data_packet(ciphertext)

    assert packet[:4] == (32).to_bytes(4, "big")
    assert parse_length_header(packet[:4]) == 32
    assert packet[4:] == ciphertext


# Không cho phép ciphertext rỗng
def test_empty_ciphertext_should_fail():
    with pytest.raises(ValueError):
        build_data_packet(b"")


# Length header phải đủ 4 byte
def test_bad_length_header_should_fail():
    with pytest.raises(ValueError):
        parse_length_header(b"\x00\x01")
