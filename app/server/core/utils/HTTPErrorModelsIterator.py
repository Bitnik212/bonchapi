import inspect

from app.server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass


class HTTPErrorModelsIterator:

    def __init__(self, errors):
        self._index = 0
        self._errors = errors
        self._members = self.__members()
        self._size = len(self._members)

    def __next__(self) -> HTTPStatusClass:
        if self._index < self._size:
            member = self._members[self._index]
            self._index += 1
            return member[1]
        else:
            raise StopIteration

    def __members(self) -> list:
        members = []
        for member in inspect.getmembers(self._errors):
            if not member[0].startswith("_"):
                members.append(member)
        return members
