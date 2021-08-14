from pydantic import BaseModel


class DefaultResponseModel(BaseModel):
    data: dict or None
    info: str or None
