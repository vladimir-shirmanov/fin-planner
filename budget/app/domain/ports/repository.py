from abc import ABC, abstractmethod

class Repository[T](ABC):
    @abstractmethod
    def create(self, **kwargs: object) -> T:
        pass

    @abstractmethod
    def update(self, id: int, **kwargs: object) -> T:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass