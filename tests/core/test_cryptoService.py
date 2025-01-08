from core.infrastructure.providers import crypto_service

def test_encrypt_password():
    # Arrange
    password = "mysecretpassword"
    
    # Act
    encrypted_password = crypto_service.CryptoService.encrypt_password(password)
    
    # Assert
    assert isinstance(encrypted_password, str)  # El hash debe ser un string
    assert len(encrypted_password) == 64  # El hash SHA-256 siempre debe tener una longitud de 64 caracteres

def test_check_password_valid():
    # Arrange
    password = "mysecretpassword"
    hashed_password =  crypto_service.CryptoService.encrypt_password(password)
    
    # Act
    result =  crypto_service.CryptoService.check_password(password, hashed_password)
    
    # Assert
    assert result is True  # La contraseña debe coincidir con el hash

def test_check_password_invalid():
    # Arrange
    password = "mysecretpassword"
    wrong_password = "wrongpassword"
    hashed_password = crypto_service.CryptoService.encrypt_password(password)
    
    # Act
    result = crypto_service.CryptoService.check_password(wrong_password, hashed_password)
    
    # Assert
    assert result is False  # La contraseña incorrecta no debe coincidir con el hash