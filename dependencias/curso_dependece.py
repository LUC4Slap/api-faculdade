from fastapi import Request

from services.curso_service import CursoService


def get_curso_service(request: Request) -> CursoService:
    return CursoService(request)