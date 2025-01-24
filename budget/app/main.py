from typing import Annotated
from fastapi import FastAPI, Path, Query
from .models.category import Category
from .models.filter_params import FilterParams

app = FastAPI()

fake_items = [Category(id=i, name='task {}'.format(i)) for i in range(20)]

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query.model_dump()

@app.get("/items/{item_id}/")
async def get_item(item_id: Annotated[int, Path(title='The ID of the item to get')],
                   q: Annotated[str | None, Query(alias='item-query')] = None):
    results: dict = fake_items[item_id].model_dump()
    if q:
        results.update({'q': q})
    return results

@app.post("/categories/")
async def create_category(category: Category):
    category_dict:dict = category.model_dump()
    fake_items.append(category)
    return category_dict
