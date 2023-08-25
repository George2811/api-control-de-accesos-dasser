from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    name: str
    last_name: str
    login: str
    password: Optional[str] = None
    status: str