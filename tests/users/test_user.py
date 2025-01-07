import pytest
from core.domain.entity.domain_entity import DomainEntity
from enum import Enum
from apps.users.domain.user import User, RoleEnum  # Ajusta la importación según la ubicación de tu archivo

# Prueba para la creación de un usuario
def test_user_creation():
    user = User(_id="123", username="john_doe", email="john.doe@example.com", password="securepassword", role=RoleEnum.ADMIN)
    
    assert user._id == "123"
    assert user.username == "john_doe"
    assert user.email == "john.doe@example.com"
    assert user.password == "securepassword"
    assert user.role == RoleEnum.ADMIN

# Prueba para la actualización del nombre de usuario
def test_update_username():
    user = User(_id="123", username="john_doe", email="john.doe@example.com", password="securepassword", role=RoleEnum.MANAGER)
    
    user.update_username("jane_doe")
    
    assert user.username == "jane_doe"

# Prueba para la actualización del correo electrónico
def test_update_email():
    user = User(_id="123", username="john_doe", email="john.doe@example.com", password="securepassword", role=RoleEnum.CLIENT)
    
    user.update_email("jane.doe@example.com")
    
    assert user.email == "jane.doe@example.com"

# Prueba para la actualización de la contraseña
def test_update_password():
    user = User(_id="123", username="john_doe", email="john.doe@example.com", password="securepassword", role=RoleEnum.ADMIN)
    
    user.update_password("newpassword")
    
    assert user.password == "newpassword"

