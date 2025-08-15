import json
import os
from cryptography.fernet import Fernet
from utils.crypto import generate_key, encrypt, decrypt


class APIManager:
    CONFIG_FILE = "api_config.bin"


    def __init__(self):
        self.encrypted_key = None
        self._load_config()

    def _load_config(self):
        """从加密文件加载API配置"""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "rb") as f:
                self.encrypted_key = f.read()

    def set_api(self, api_key: str, api_secret: str, remember: bool = False):
        """设置API密钥"""
        combined = f"{api_key}:{api_secret}"
        self.encrypted_key = encrypt(combined)

        if remember:
            with open(self.CONFIG_FILE, "wb") as f:
                f.write(self.encrypted_key)

    def get_api(self):
        """获取解密的API密钥"""
        if not self.encrypted_key:
            return None, None

        try:
            decrypted = decrypt(self.encrypted_key)
            api_key, api_secret = decrypted.split(":", 1)
            return api_key, api_secret
        except:
            return None, None

    def has_valid_api(self):
        """检查是否有有效的API密钥"""
        return self.get_api() != (None, None)

    def clear_session(self):
        """清除当前会话的API密钥"""
        self.encrypted_key = None