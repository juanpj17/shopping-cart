import pytest
from core.application.events import publisher  # Aquí estamos importando el módulo 'publisher'

# Clase "mock" que actúe como suscriptor
class MockSubscriber:
    def __init__(self):
        self.received_data = None
    
    def update(self, data):
        self.received_data = data

def test_subscribe():
    # Arrange
    publisher_instance = publisher.Publisher[MockSubscriber]()  # Se crea el Publisher
    subscriber = MockSubscriber()  # Se crea un suscriptor

    # Act
    publisher_instance.subscribe(subscriber)  # Se agrega un suscriptor

    # Assert
    assert subscriber in publisher_instance.subscribers  # El suscriptor debe estar en la lista de suscriptores

def test_unsubscribe():
    # Arrange
    publisher_instance = publisher.Publisher[MockSubscriber]()  # Crear el Publisher
    subscriber = MockSubscriber()  # Crear un suscriptor
    publisher_instance.subscribe(subscriber)  # Agregar suscriptor

    # Act
    publisher_instance.unsubscribe(subscriber)  # Eliminar suscriptor

    # Assert
    assert subscriber not in publisher_instance.subscribers  # El suscriptor no debe estar en la lista de suscriptores

def test_notify():
    # Arrange
    publisher_instance = publisher.Publisher[MockSubscriber]()  # Crear el Publisher
    subscriber = MockSubscriber()  # Crear un suscriptor
    publisher_instance.subscribe(subscriber)  # Agregar suscriptor

    data = "Test Data"  # Datos de prueba

    # Act
    publisher_instance.notify(data)  # Notificar a los suscriptores

    # Assert
    assert subscriber.received_data == data  # El suscriptor debe recibir los datos correctamente