from pydantic import BaseModel, Field, EmailStr
from typing import Optional
class RelatroioCursoDto(BaseModel):
    gte: Optional[bool]
    lte: Optional[bool]
    media: float