from typing import Any, Optional, List, Tuple, Union

from pydantic import BaseModel


class DefaultResponseModel(BaseModel):
    data: Union[None, List[dict], dict]
    info: str or None
