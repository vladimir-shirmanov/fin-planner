from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    email: str
    user_id: UUID