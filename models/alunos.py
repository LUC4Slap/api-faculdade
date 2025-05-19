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

class ListUpdateModel(BaseModel):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[str]
    cpf: Optional[str]
    rua: Optional[str]
    bairro: Optional[str]
    cep: Optional[str]
    cursos: Optional[List[str]]