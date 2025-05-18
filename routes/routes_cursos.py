from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.cursos import ListModelCursos, ListUpdateModelCursos

router = APIRouter()
COLLECTION_NAME = "cursos"

@router.get("/listar-cursos", response_description='Listar cursos', status_code=status.HTTP_201_CREATED, response_model=List[ListModelCursos])
def listar_cursos(request: Request):
    cusosDb = list(request.app.database[COLLECTION_NAME].find(limit=50))
    return cusosDb

@router.post("/criar-curso", response_description='Cadastrar curso', status_code=status.HTTP_201_CREATED,response_model=ListModelCursos)
def create_list(request: Request, list: ListModelCursos = Body(...)):
    list = jsonable_encoder(list)
    new_list_item = request.app.database[COLLECTION_NAME].insert_one(list)
    created_list_item = request.app.database[COLLECTION_NAME].find_one({
        "_id": new_list_item.inserted_id
    })
    return created_list_item

@router.put("/atualizar-curso",response_description="Atualizar Curso", response_model=ListModelCursos)
def update_curso(id: str, request: Request, list: ListModelCursos = Body(...)):
    listItems = {}
    for k,v in list.dict().items():
        if v is not None:
            listItems = {k:v}

    print(listItems)
    # if list.title | list.description:
    update_result = request.app.database[COLLECTION_NAME].update_one({"_id": id }, {"$set": listItems })
    # print("update result ",update_result.modified_count)

    if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Item with ID {id} has not been modified")


    if (
        updated_list_item := request.app.database[COLLECTION_NAME].find_one({"_id": id})
    ) is not None:
        return updated_list_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ListItem with ID {id} not found")

@router.delete('/delete-curso', response_description="Deleta Curso")
def delete_curso(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLLECTION_NAME].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Item with {id} not found")