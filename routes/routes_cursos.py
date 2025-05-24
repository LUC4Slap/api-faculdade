from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, Query
from fastapi.encoders import jsonable_encoder
from typing import List

from starlette.responses import StreamingResponse

from dependencias.curso_dependece import get_curso_service
from dependencias.relatorio_dependece import get_relatorio_service
from models.cursos import ListModelCursos, UpdateModelCursos
from models.paginacaoModel import PaginacaoAlunosResponse
from services.curso_service import CursoService
from services.relatorio_curso_service import RelatorioService

router = APIRouter()
COLLECTION_NAME = "cursos"

@router.get("/listar-cursos", response_description='Listar cursos', status_code=status.HTTP_201_CREATED, response_model=List[ListModelCursos])
def listar_cursos(service: CursoService = Depends(get_curso_service)):
    return service.listar_cursos()

@router.get("/listar-curso-id", response_description="Buscar curso por id", status_code=status.HTTP_200_OK, response_model=ListModelCursos)
def buscar_curso_id(id: str, service: CursoService = Depends(get_curso_service)):
    return service.buscar_curso_por_id(id)

@router.get("/listar-alunos-por-curso", response_description="Lista alunos por curso paginado", status_code=status.HTTP_200_OK, response_model=PaginacaoAlunosResponse)
def listar_alunos_por_curso(id: str, page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0, le=100), service: CursoService = Depends(get_curso_service)):
    return service.listar_curso_alunos(id, page, limit)

@router.post("/criar-curso", response_description='Cadastrar curso', status_code=status.HTTP_201_CREATED,response_model=ListModelCursos)
def create_list(list: ListModelCursos = Body(...), service: CursoService = Depends(get_curso_service)):
    return service.criar_curso(list)

@router.put("/atualizar-curso", response_description="Atualizar Curso", response_model=ListModelCursos)
def update_curso(id: str, curso_update: UpdateModelCursos = Body(...), service: CursoService = Depends(get_curso_service)):
    return service.update_curso(id, curso_update)

@router.delete('/delete-curso', response_description="Deleta Curso")
def delete_curso(id: str, service: CursoService = Depends(get_curso_service)):
    return service.deletar_curso(id)

@router.get("/relatorio-cusos", response_description="Relatório de curso", response_class=StreamingResponse)
def relatorio_curso(media: float, service: RelatorioService = Depends(get_relatorio_service)):
    headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    path = service.gerar_relatorio_curso(media)
    file_like = open(path, mode="rb")
    return StreamingResponse(file_like, headers=headers, media_type='application/pdf')