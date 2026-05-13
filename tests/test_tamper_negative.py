import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from aes_socket_utils import decrypt_aes_cbc, encrypt_aes_cbc
def test_tampered_ciphertext_should_fail_or_change_plaintext():
    plain = b"Thong diep dung de test tamper"
    key = b"1" * 16
    iv = b"2" * 16
    _, _, cipher_bytes = encrypt_aes_cbc(plain, key=key, iv=iv)

    tampered = bytearray(cipher_bytes)
    tampered[-1] ^= 0x01

    try:
        recovered = decrypt_aes_cbc(key, iv, bytes(tampered))
        assert recovered != plain
    except ValueError:
        assert True
