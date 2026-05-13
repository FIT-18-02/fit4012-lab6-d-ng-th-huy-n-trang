import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from aes_socket_utils import decrypt_aes_cbc, encrypt_aes_cbc

def test_wrong_key_should_not_recover_original_plaintext():
    plain = b"Thong diep dung de test wrong key"
    key = b"1" * 16
    iv = b"2" * 16
    _, _, cipher_bytes = encrypt_aes_cbc(plain, key=key, iv=iv)

    wrong_key = b"3" * 16

    try:
        recovered = decrypt_aes_cbc(wrong_key, iv, cipher_bytes)
        assert recovered != plain
    except ValueError:
        assert True
