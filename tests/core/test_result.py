import pytest
from typing import Optional
from core.application.results import result 


def test_success_case():
    # Arrange
    resultado = result.Result.make_success(42)
    
    # Assert
    assert resultado.is_success() is True  # Debería ser un éxito
    assert resultado.is_failure() is False  # No debería ser un fallo
    assert resultado.unwrap() == 42  # Debería devolver el valor 42


def test_failure_case():
    # Arrange
    error = Exception("Something went wrong")
    resultado = result.Result.make_failure(error)
    
    # Assert
    assert resultado.is_success() is False  # No es un éxito
    assert resultado.is_failure() is True  # Es un fallo
    assert resultado.unwrap() == error  # Debería devolver el error

def test_invalid_initialization_both_value_and_error():
    # Arrange & Act & Assert
    with pytest.raises(ValueError, match="Either value or error should be provided"):
        result.Result(value=42, error=Exception("Some error"))

def test_invalid_initialization_neither_value_nor_error():
    # Arrange & Act & Assert
    with pytest.raises(ValueError, match="Either value or error should be provided"):
        result.Result(value=None, error=None)

def test_initialization_with_value():
    # Arrange
    resultado = result.Result(value=42)
    
    # Assert
    assert resultado.is_success() is True
    assert resultado.unwrap() == 42


def test_initialization_with_error():
    # Arrange
    error = Exception("An error occurred")
    resultado = result.Result(error=error)
    
    # Assert
    assert resultado.is_failure() is True
    assert resultado.unwrap() == error