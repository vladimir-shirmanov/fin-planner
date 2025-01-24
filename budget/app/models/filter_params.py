from typing import Literal

from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "limit": 100,
                "offset": 0,
                "order_by": "created_at",
                "tags": ["tag1", "tag2"]
            }
        }
    }