from fastapi import FastAPI, Request
from typing import Optional
from urllib.parse import urljoin

app = FastAPI()

class Category:
    id: int
    name: str

class Pagination:
    page: int
    per_page: int
    next_page: str
    prev_page: Optional[str]
    items: list
    def __init__(self, page: int, per_page: int, items: list, url = None):
        self.page = page
        self.per_page = per_page
        self.items = items
        if page == 0:
            self.prev_page = None
        else:
            self.prev_page = '{}?page={}&per_page={}'.format(url, page - 1, per_page)
        self.next_page = '{}?page={}&per_page={}'.format(url, page + 1, per_page)


fake_items = [{'id': i, 'name': 'task {}'.format(i)} for i in range(20)]


@app.get('/items/')
async def get_items(request: Request, page: int = 1, per_page: int = 3):
    result = Pagination(page, per_page, fake_items[(page-1)*per_page: page*per_page], urljoin(str(request.base_url), request.url.path))
    return result

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{item_id}")
async def get_item(item_id: int):
    return {"item_id":item_id}