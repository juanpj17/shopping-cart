import hashlib

class CryptoService():
    
    def encrypt_password(password: str) -> str:
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    def check_password(plain_password: str, hashed_password: str) -> bool:
        sha_signature = hashlib.sha256(plain_password.encode()).hexdigest()
        return sha_signature == hashed_password