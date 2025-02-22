from abc import ABC, abstractmethod
from typing import Any

class Specification(ABC):
    """Abstract base class for query specifications"""
    @abstractmethod
    def resolve(self, resolver: 'SpecificationResolver') -> Any:
        pass


class SpecificationResolver(ABC):
    """Translates specifications to ORM-specific constructs"""
    @abstractmethod
    def resolve(self, spec: Specification):
        pass