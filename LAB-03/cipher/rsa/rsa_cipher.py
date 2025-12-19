import random
from math import gcd

class RSACipher:
    def __init__(self):
        self.private_key_file = "private_key.txt"
        self.public_key_file = "public_key.txt"

    # ---------------------------------------
    # 1. SINH KHÓA
    # ---------------------------------------
    def generate_keys(self):
        # Sử dụng 2 số nguyên tố nhỏ để minh họa
        p = 61
        q = 53
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 17                       # số mũ công khai
        d = pow(e, -1, phi)          # nghịch đảo modular

        # Ghi file
        with open(self.private_key_file, "w") as f:
            f.write(f"{d},{n}")

        with open(self.public_key_file, "w") as f:
            f.write(f"{e},{n}")

    # ---------------------------------------
    # 2. LOAD KEY TỪ FILE
    # ---------------------------------------
    def load_keys(self):
        with open(self.private_key_file, "r") as f:
            d, n1 = map(int, f.read().split(","))

        with open(self.public_key_file, "r") as f:
            e, n2 = map(int, f.read().split(","))

        return (d, n1), (e, n2)

    # ---------------------------------------
    # 3. MÃ HÓA
    # ---------------------------------------
    def encrypt(self, message, key):
        e, n = key
        m_int = int.from_bytes(message.encode(), "big")
        c_int = pow(m_int, e, n)
        return c_int.to_bytes((c_int.bit_length() + 7) // 8, "big")

    # ---------------------------------------
    # 4. GIẢI MÃ
    # ---------------------------------------
    def decrypt(self, ciphertext, key):
        d, n = key
        c_int = int.from_bytes(ciphertext, "big")
        m_int = pow(c_int, d, n)
        return m_int.to_bytes((m_int.bit_length() + 7) // 8, "big")

    # ---------------------------------------
    # 5. KÝ SỐ
    # ---------------------------------------
    def sign(self, message, private_key):
        d, n = private_key
        hashed = int.from_bytes(message.encode(), "big")
        sig_int = pow(hashed, d, n)
        return sig_int.to_bytes((sig_int.bit_length() + 7) // 8, "big")

    # ---------------------------------------
    # 6. XÁC THỰC CHỮ KÝ
    # ---------------------------------------
    def verify(self, message, signature, public_key):
        e, n = public_key
        hashed = int.from_bytes(message.encode(), "big")
        decrypted_sig = pow(int.from_bytes(signature, "big"), e, n)
        return hashed == decrypted_sig
