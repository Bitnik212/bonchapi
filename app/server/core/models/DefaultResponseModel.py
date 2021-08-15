from typing import Any

from pydantic import BaseModel


class DefaultResponseModel(BaseModel):
    data: dict or list
    info: str or None
