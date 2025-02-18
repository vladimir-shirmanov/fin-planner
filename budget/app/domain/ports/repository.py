from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def create(self, schema):
        pass

    @abstractmethod
    def update(self, schema):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass