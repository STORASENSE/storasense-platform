from __future__ import annotations

import math
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable

from pydantic import BaseModel
from sqlalchemy.orm import Query, Mapped


class HTTPNumberedPageRequest(BaseModel):
    page_number: int
    page_size: int


class HTTPNumberedPageResponse[T](BaseModel):
    page_number: int
    page_size: int
    total_pages: int
    items: list[T]


class HTTPCursorBasedPageRequest(BaseModel):
    page_number: int
    cursor: timedelta


class HTTPCursorBasedPageResponse[T](BaseModel):
    page_number: int
    cursor: timedelta
    total_pages: int
    items: list[T]


class PageRequest[ID]:
    def __init__(self, page_number: int, page_size: ID):
        self.page_number = page_number
        self.page_size = page_size


class NumberedPageRequest(PageRequest[int]):
    """
    This class represents the request for a page. The request entails the page's number
    and the size of each page.

    Attributes:
        page_number (int): The page's number.
        page_size (int): The size of each page.
    """

    @staticmethod
    def from_http_request(
        request: HTTPNumberedPageRequest,
    ) -> NumberedPageRequest:
        return NumberedPageRequest(request.page_number, request.page_size)

    def __init__(self, page_number: int, page_size: int):
        super().__init__(page_number, page_size)


class CursorBasedPageRequest(PageRequest[timedelta]):
    @staticmethod
    def from_http_request(
        request: HTTPCursorBasedPageRequest,
    ) -> CursorBasedPageRequest:
        return CursorBasedPageRequest(request.page_number, request.cursor)

    def __init__(self, page_number: int, cursor: timedelta):
        super().__init__(page_number, cursor)


class Page[T, ID](ABC):
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
        page_number: int,
        page_size: ID,
        total_pages: int,
    ) -> None:
        self.items = items
        self.page_size = page_size
        self.page_number = page_number
        self.total_pages = total_pages

    def __iter__(self):
        return iter(self.items)

    def has_previous(self) -> bool:
        return self.page_number > 0

    def has_next(self) -> bool:
        return self.page_number < self.total_pages

    @abstractmethod
    def map[Q](self, transformer: Callable[[T], Q]) -> Page[Q, ID]:
        pass

    @abstractmethod
    def previous_page_request(self) -> PageRequest[ID]:
        pass

    @abstractmethod
    def next_page_request(self) -> PageRequest[ID]:
        pass


class NumberedPage[T](Page[T, int]):
    @staticmethod
    def from_query(
        query: Query[T], request: NumberedPageRequest
    ) -> NumberedPage[T]:
        q = query.limit(request.page_size).offset(
            request.page_number * request.page_size
        )
        count = math.ceil(query.count() / q.count())
        items = q.all()
        return NumberedPage(
            items, request.page_number, request.page_size, count
        )

    def __init__(
        self,
        items: list[T],
        page_number: int,
        page_size: int,
        total_pages: int,
    ):
        super().__init__(items, page_number, page_size, total_pages)

    def map[Q](self, transformer: Callable[[T], Q]) -> NumberedPage[Q]:
        items = [transformer(item) for item in self.items]
        return NumberedPage(
            items, self.page_number, self.page_size, self.total_pages
        )

    def previous_page_request(self) -> NumberedPageRequest:
        if not self.has_previous():
            raise IndexError(
                "Could not create a request for previous page because this is the first page."
            )
        return NumberedPageRequest(self.page_number - 1, self.page_size)

    def next_page_request(self) -> NumberedPageRequest:
        if not self.has_next():
            raise IndexError(
                "Could not create a request for next page because this is the last page."
            )
        return NumberedPageRequest(self.page_number + 1, self.page_size)

    def to_http_response(self) -> HTTPNumberedPageResponse[T]:
        return HTTPNumberedPageResponse(
            page_number=self.page_number,
            page_size=self.page_size,
            total_pages=self.total_pages,
            items=self.items,
        )


class CursorBasedPage[T](Page[T, timedelta]):
    @staticmethod
    def from_query(
        query: Query[T],
        request: CursorBasedPageRequest,
        cursor_target: Mapped[datetime],
    ):
        date_start = cursor_target - request.page_size * (
            request.page_number + 1
        )
        date_end = cursor_target - request.page_size * request.page_number
        q = query.where(cursor_target >= date_start).where(
            cursor_target <= date_end
        )
        count = math.ceil(query.count() / q.count())
        items = q.all()
        return CursorBasedPage(
            items, request.page_number, request.page_size, count
        )

    def __init__(
        self,
        items: list[T],
        page_number: int,
        cursor: timedelta,
        total_pages: int,
    ):
        super().__init__(items, page_number, cursor, total_pages)

    def map[Q](self, transformer: Callable[[T], Q]) -> CursorBasedPage[Q]:
        items = [transformer(item) for item in self.items]
        return CursorBasedPage(
            items, self.page_number, self.page_size, self.total_pages
        )

    def previous_page_request(self) -> CursorBasedPageRequest:
        if not self.has_previous():
            raise IndexError(
                "Could not create a request for previous page because this is the first page."
            )
        return CursorBasedPageRequest(self.page_number - 1, self.page_size)

    def next_page_request(self) -> CursorBasedPageRequest:
        if not self.has_next():
            raise IndexError(
                "Could not create a request for next page because this is the last page."
            )
        return CursorBasedPageRequest(self.page_number + 1, self.page_size)

    def to_http_response(self) -> HTTPCursorBasedPageResponse[T]:
        return HTTPCursorBasedPageResponse(
            page_number=self.page_number,
            cursor=self.page_size,
            total_pages=self.total_pages,
            items=self.items,
        )
