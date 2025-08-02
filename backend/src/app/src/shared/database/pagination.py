from typing import Any

from sqlalchemy.orm import Query


class PageRequest:
    """
    This class represents the request for a page. The request entails the page's number
    and the size of each page.

    Attributes:
        page_number (int): The page's number.
        page_size (int): The size of each page.
    """

    def __init__(self, page_number: int, page_size: int):
        self.page_number = page_number
        self.page_size = page_size


class Page[T]:
    """
    This class represents a page, which is a slice of paginated data.
    Instances of this class contain a list of paginated items, as well as
    information about the page itself.

    Attributes:
        items (list[T]): A list of paginated items.
        page_number (int): The page's number.
        page_size (int): The size of each page.
        total_pages (int): The total number of pages.
    """

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
    """
    This method is used for implementing pagination on a query.
    In specific, applies LIMIT and OFFSET parameters to the query
    and then finds all queried rows. The result is a page with the
    queried items.

    :param query: The query to apply pagination to.
    :param request: The pagination request.
    :return: A page containing the requested data.
    """
    q = query.limit(request.page_size).offset(
        request.page_number * request.page_size
    )
    count = q.count()
    items = q.all()
    return Page(items, request.page_size, request.page_number, count)
