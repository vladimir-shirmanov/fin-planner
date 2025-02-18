from pydantic import BaseModel

class Pagination:
    page: int
    per_page: int
    next_page: str
    prev_page: str | None = None
    items: list[BaseModel]
    def __init__(self, page: int, per_page: int, items: list[BaseModel], url = None):
        self.page = page
        self.per_page = per_page
        self.items = items
        if page == 0:
            pass
        else:
            self.prev_page = '{}?page={}&per_page={}'.format(url, page - 1, per_page)
        self.next_page = '{}?page={}&per_page={}'.format(url, page + 1, per_page)
