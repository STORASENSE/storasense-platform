from typing import Any

from sqlalchemy.orm import Query


class PageRequest:
    def __init__(self, page_number: int, page_size: int):
        self.page_number = page_number
        self.page_size = page_size


class Page[T]:
    def __init__(
        self,
        items: list[T],
        page_size: int,
        page_number: int,
        total_pages: int,
    ) -> None:
        self.items = items
        self.page_size = page_size
        self.page_number = page_number
        self.total_pages = total_pages

    def __iter__(self):
        return iter(self.items)


def paginate(query: Query, request: PageRequest) -> Page[Any]:
    q = query.limit(request.page_size).offset(
        request.page_number * request.page_size
    )
    count = q.count()
    items = q.all()
    return Page(items, request.page_size, request.page_number, count)
