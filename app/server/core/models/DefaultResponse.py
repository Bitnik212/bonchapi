from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    data: dict or None
    info: str or None
