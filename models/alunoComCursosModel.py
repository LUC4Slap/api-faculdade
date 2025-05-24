from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
import uuid

# Reaproveitando seu modelo de curso:
class CursoModel(BaseModel):
    id: str = Field(alias="_id")
    nome: str
    carga_horaria: str
    descricao: str
    media_aprovacao: float

class AlunoComCursosModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    nome: str
    sobrenome: str
    email: EmailStr
    cpf: str
    rua: str
    bairro: str
    cep: str
    cursos: List[str]
    cursos_info: List[CursoModel]
    cursos_info: Optional[List[CursoModel]] = None

    class Config:
        allow_population_by_field_name = True
