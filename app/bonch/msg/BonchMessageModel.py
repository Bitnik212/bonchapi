from typing import List, Optional

from pydantic import BaseModel, Field


class BonchMessageModel(BaseModel):
    class Files(BaseModel):
        name: str = Field(description="Название файла")
        href: str = Field(description="Ссылка на файл")

    id: Optional[int] = Field(description="Id сообщения")
    readed: bool = Field(description="Прочитано ли сообщение")
    sender: Optional[str] = Field(description="Отправитель")
    date: Optional[str] = Field(description="Дата сообщения")
    time: Optional[str] = Field(description="Время сообщения")
    title: str = Field(description="Заголовок сообщения")
    files: Optional[List[Files]] = Field(description="Файлы сообщения. Могут быть пустыми. none не используется")
    message: Optional[str] = Field(description="Содержимое сообщения")
