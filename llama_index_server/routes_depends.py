from pydantic import BaseModel

class QueryItem(BaseModel):
    query: str