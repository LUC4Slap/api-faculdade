from typing import List
from pydantic import BaseModel

# Assumindo que AlunoComCursosModel já foi definido
from models.alunoComCursosModel import AlunoComCursosModel

class PaginacaoAlunosResponse(BaseModel):
    page: int
    limit: int
    total: int
    has_next: bool
    data: List[AlunoComCursosModel]
