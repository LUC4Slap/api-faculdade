from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from dependencias.aluno_dependece import get_aluno_service
from models.alunos import ListModel, UpdateModel
from models.paginacaoModel import PaginacaoAlunosResponse
from services.aluno_service import AlunoService

router = APIRouter()
COLLECTION_NAME = "alunos"

@router.post("/", response_description='Cadastrar aluno', status_code=status.HTTP_201_CREATED,response_model=ListModel)
def create_list(list: ListModel = Body(...), service: AlunoService = Depends(get_aluno_service)):
    return service.criar_aluno(list)

@router.get('/listar-alunos', response_description='Cadastrar aluno', status_code=status.HTTP_201_CREATED,response_model=PaginacaoAlunosResponse)
def listar_alunos(page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000), service: AlunoService = Depends(get_aluno_service)):
    return service.listar_usuarios(page, limit)

@router.delete('/delete-aluno', response_description="Deleta aluno")
def delete_aluno(id: str, service: AlunoService = Depends(get_aluno_service)):
    return service.deletar_aluno(id)

@router.put("/atualizar-aluno",response_description="update the item in list", response_model=ListModel)
def update_item(id: str, aluno_update: UpdateModel = Body(...), service: AlunoService = Depends(get_aluno_service)):
    return service.atualizar_aluno(id, aluno_update)

@router.get("/buscar-aluno-cpf", response_description="Buscar aluno pelo CPF", response_model=ListModel)
def buscar_aluno_cpf(cpf: str, service: AlunoService = Depends(get_aluno_service)):
    return service.burcar_aluno_por_cpf(cpf)