from fastapi import Request
from services.aluno_service import AlunoService

def get_aluno_service(request: Request) -> AlunoService:
    return AlunoService(request)