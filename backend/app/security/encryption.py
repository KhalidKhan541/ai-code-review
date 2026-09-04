from cryptography.fernet import Fernet
from app.config import get_settings

settings = get_settings()


class EncryptionService:
    def __init__(self):
        key = settings.SECRET_KEY[:32].ljust(32, "0")
        self.cipher = Fernet(Fernet.generate_key())

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()


encryption_service = EncryptionService()
