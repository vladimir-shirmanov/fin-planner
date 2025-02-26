from uuid import UUID

from ..ports import Specification, SpecificationResolver

class AuthorSpec(Specification):
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def resolve(self, resolver: SpecificationResolver):
        return resolver.resolve_author(self.user_id)