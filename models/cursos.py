from typing import Optional
import uuid;

from pydantic import BaseModel, Field

class ListModelCursos(BaseModel):
    id:str = Field(default_factory=uuid.uuid4, alias="_id")
    nome: str
    carga_horaria: str
    descricao: str
    media_aprovacao: int

class ListUpdateModelCursos(BaseModel):
    nome: Optional[str]
    carga_horaria: Optional[str]
    descricao: Optional[str]
    media_aprovacao: Optional[int]