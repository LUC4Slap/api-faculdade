from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from typing import List

from models.alunos import ListModel, UpdateModel
from models.alunoComCursosModel import AlunoComCursosModel
from models.paginacaoModel import PaginacaoAlunosResponse

router = APIRouter()
COLLECTION_NAME = "alunos"

@router.post("/", response_description='Cadastrar aluno', status_code=status.HTTP_201_CREATED,response_model=ListModel)
def create_list(request: Request, list: ListModel = Body(...)):
    list = jsonable_encoder(list)
    jaExiste = request.app.database[COLLECTION_NAME].find_one({
        "$or": [
            {"email": list["email"]},
            {"cpf": list["cpf"]}
        ]
    })
    if jaExiste is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um aluno com este email ou cpf"
        )

    new_list_item = request.app.database[COLLECTION_NAME].insert_one(list)
    created_list_item = request.app.database[COLLECTION_NAME].find_one({
        "_id": new_list_item.inserted_id
    })

    return created_list_item

@router.get('/listar-alunos', response_description='Cadastrar aluno', status_code=status.HTTP_201_CREATED,response_model=PaginacaoAlunosResponse)
def listar_alunos(request: Request, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000)):
    skip = (page - 1) * limit

    # Pipeline com lookup, paginação
    pipeline = [
        {
            "$lookup": {
                "from": "cursos",
                "localField": "cursos",
                "foreignField": "_id",
                "as": "cursos_info"
            }
        },
        {"$skip": skip},
        {"$limit": limit}
    ]

    # Executa agregação
    alunos = list(request.app.database["alunos"].aggregate(pipeline))

    # Total de documentos (sem filtros adicionais)
    total = request.app.database["alunos"].count_documents({})

    # Verifica se há próxima página
    has_next = (page * limit) < total

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "has_next": has_next,
        "data": alunos
    }

@router.delete('/delete-aluno', response_description="Deleta aluno")
def delete_aluno(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLLECTION_NAME].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Item with {id} not found")

@router.put("/atualizar-aluno",response_description="update the item in list", response_model=ListModel)
def update_item(id: str, request: Request, aluno_update: UpdateModel = Body(...)):
    update_data = aluno_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum dado fornecido para atualização"
        )

    update_result = request.app.database[COLLECTION_NAME].update_one(
        {"_id": id},
        {"$set": update_data}
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail=f"Curso com ID {id} não foi modificado"
        )

    if (
            updated_curso := request.app.database[COLLECTION_NAME].find_one({"_id": id})
    ) is not None:
        return updated_curso

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Curso com ID {id} não encontrado"
    )

@router.get("/buscar-aluno-cpf", response_description="Buscar aluno pelo CPF", response_model=ListModel)
def buscar_aluno_cpf(cpf: str, request: Request):
    aluno = request.app.database[COLLECTION_NAME].find_one({"cpf": cpf})
    if aluno is not None:
        return aluno
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe aluno para este cpf: {cpf}")