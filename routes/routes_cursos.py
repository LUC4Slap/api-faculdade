from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from dependencias.curso_dependece import get_curso_service
from models.cursos import ListModelCursos, UpdateModelCursos
from services.curso_service import CursoService

router = APIRouter()
COLLECTION_NAME = "cursos"

@router.get("/listar-cursos", response_description='Listar cursos', status_code=status.HTTP_201_CREATED, response_model=List[ListModelCursos])
def listar_cursos(service: CursoService = Depends(get_curso_service)):
    return service.listar_cursos()

@router.post("/criar-curso", response_description='Cadastrar curso', status_code=status.HTTP_201_CREATED,response_model=ListModelCursos)
def create_list(request: Request, list: ListModelCursos = Body(...)):
    list = jsonable_encoder(list)
    new_list_item = request.app.database[COLLECTION_NAME].insert_one(list)
    created_list_item = request.app.database[COLLECTION_NAME].find_one({
        "_id": new_list_item.inserted_id
    })
    return created_list_item

@router.put("/atualizar-curso", response_description="Atualizar Curso", response_model=ListModelCursos)
def update_curso(id: str, request: Request, curso_update: UpdateModelCursos = Body(...)):
    update_data = curso_update.dict(exclude_unset=True)

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

@router.delete('/delete-curso', response_description="Deleta Curso")
def delete_curso(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLLECTION_NAME].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Item with {id} not found")