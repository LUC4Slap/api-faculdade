from typing import Optional
import uuid;
from pydantic import BaseModel, Field, EmailStr
from typing import List

class ListModel(BaseModel):
    id:str = Field(default_factory=uuid.uuid4, alias="_id")
    nome: str
    sobrenome: str
    email: EmailStr
    cpf: str
    rua: str
    bairro: str
    cep: str
    cursos: List[str]

class UpdateModel(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    rua: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cursos: Optional[List[str]] = None