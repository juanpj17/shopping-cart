from abc import ABC

from typing import TypeVar, Generic

T = TypeVar('T')

class Publisher(ABC, Generic[T]):

    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber: T):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: T):
        self.subscribers.remove(subscriber)

    def notify(self, data: T):
        for subscriber in self.subscribers:
            subscriber.update(data)