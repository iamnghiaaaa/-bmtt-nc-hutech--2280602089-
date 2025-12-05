import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests
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
        with open(self.keys(), "w") as f:
            f.write(f"{d},{n}")

        with open(self.keys(), "w") as f:
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



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Fail")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())