from typing import Optional
import uuid;

from pydantic import BaseModel, Field

class ListModelCursos(BaseModel):
    id:str = Field(default_factory=uuid.uuid4, alias="_id")
    nome: str
    carga_horaria: str
    descricao: str
    media_aprovacao: float

class UpdateModelCursos(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[str] = None
    descricao: Optional[str] = None
    media_aprovacao: Optional[float] = None