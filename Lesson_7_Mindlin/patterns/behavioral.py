from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class SMSNotifier(Observer):
    def update(self, subject):
        print(f'[SMS -->] новый заказ от {subject.buyers[-1].name}')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'[EMAIL -->] новый заказ от {subject.buyers[-1].name}')


class FileWriter:
    def __init__(self, file_name='logger.log'):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(text)


class ConsoleWriter:
    @staticmethod
    def write(text):
        print(text)
