from pydantic import BaseModel, Extra, Field

class GetQuery(BaseModel, extra=Extra.forbid):
    author: str | None = None
    search: str | None = None
    limit: int | None = None


class PostQuery(BaseModel):
    text: str = Field(min_length = 1, max_length = 500)
    author: str = Field(min_length = 1, max_length = 500)


class PutQuery(BaseModel):
    text: str | None = Field(default=None, min_length = 1, max_length = 500)
    author: str | None = Field(default=None, min_length = 1, max_length = 500)