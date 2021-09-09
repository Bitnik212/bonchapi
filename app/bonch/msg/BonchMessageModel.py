from typing import List

from pydantic import BaseModel, Field


class BonchMessageModel(BaseModel):
    class Files(BaseModel):
        name: str = Field(description="Название файла")
        href: str = Field(description="Ссылка на файл")

    id: int = Field(description="Id сообщения")
    readed: bool = Field(description="Прочитано ли сообщение")
    sender: str = Field(description="Отправитель")
    date: str = Field(description="Дата сообщения")
    time: str = Field(description="Время сообщения")
    title: str = Field(description="Заголовок сообщения")
    files: List[Files] = Field(description="Файлы сообщения. Могут быть пустыми. none не используется")
