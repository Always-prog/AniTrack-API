from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def run(self):
        pass



