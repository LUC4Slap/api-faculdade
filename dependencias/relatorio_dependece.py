from fastapi import Request

from services.relatorio_curso_service import RelatorioService


def get_relatorio_service(request: Request) -> RelatorioService:
    return RelatorioService(request)