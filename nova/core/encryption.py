"""Encryption and Decryption Utilities"""

from cryptography.fernet import Fernet
from nova.config import settings
from nova.logger import get_logger
import base64
import os

logger = get_logger(__name__)


class EncryptionManager:
    """Manage encryption and decryption of sensitive data"""

    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)

    @staticmethod
    def _get_or_create_key() -> bytes:
        """Get or create encryption key"""
        if settings.DB_ENCRYPTION_KEY:
            try:
                return base64.urlsafe_b64decode(settings.DB_ENCRYPTION_KEY)
            except Exception as e:
                logger.warning(f"Invalid encryption key: {e}, generating new one")

        # Generate new key
        key = Fernet.generate_key()
        logger.info(f"Generated new encryption key: {key.decode()}")
        return key

    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data

    def encrypt_dict(self, data: dict, keys_to_encrypt: list) -> dict:
        """Encrypt specific keys in dictionary"""
        encrypted_data = data.copy()
        for key in keys_to_encrypt:
            if key in encrypted_data and isinstance(encrypted_data[key], str):
                encrypted_data[key] = self.encrypt(encrypted_data[key])
        return encrypted_data

    def decrypt_dict(self, data: dict, keys_to_decrypt: list) -> dict:
        """Decrypt specific keys in dictionary"""
        decrypted_data = data.copy()
        for key in keys_to_decrypt:
            if key in decrypted_data and isinstance(decrypted_data[key], str):
                decrypted_data[key] = self.decrypt(decrypted_data[key])
        return decrypted_data
