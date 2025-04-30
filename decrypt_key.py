import os
from dotenv import load_dotenv
import subprocess
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

load_dotenv()
KEY_PASSWORD = os.getenv("KEY_PASSWORD")

# 加载私钥
def load_private_key(path="static/keys/privatekey.pem.enc"):
    # 使用 OpenSSL 解密私钥
    result = subprocess.run(
        ['openssl', 'enc', '-aes-256-cbc', '-d', '-in', path, '-pass', f'pass:{KEY_PASSWORD}'],
        capture_output=True,
        check=True
    )
    decrypted_key = result.stdout

    # 加载为 RSA 私钥对象
    private_key = serialization.load_pem_private_key(
        decrypted_key,
        password=None,
        backend=default_backend()
    )
    return private_key

def rsa_decrypt_pkcs1v15(encrypted_b64: str) -> str:
    """
    解密 base64 编码的 JSEncrypt 密文（默认使用 PKCS1 v1.5 padding）
    """
    try:
        encrypted_data = base64.b64decode(encrypted_b64)
        private_key = load_private_key()
        decrypted = private_key.decrypt(
            encrypted_data,
            asym_padding.PKCS1v15()
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"RSA 解密失败: {e}")

