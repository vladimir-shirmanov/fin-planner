from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Groceries"
            }
        }
    }