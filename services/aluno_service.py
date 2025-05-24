from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

from models.alunos import ListModel, UpdateModel

class AlunoService:
    def __init__(self, request: Request):
        self.db = request.app.database
        self.collection = self.db["alunos"]
        self.request = request

    def listar_usuarios(self, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000)):
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
        alunos = list(self.collection.aggregate(pipeline))

        # Total de documentos (sem filtros adicionais)
        total = self.collection.count_documents({})

        # Verifica se há próxima página
        has_next = (page * limit) < total

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "has_next": has_next,
            "data": alunos
        }

    def criar_aluno(self, aluno: ListModel):
        list = jsonable_encoder(aluno)
        jaExiste = self.collection.find_one({
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

        new_list_item = self.collection.insert_one(list)
        created_list_item = self.collection.find_one({
            "_id": new_list_item.inserted_id
        })

        return created_list_item

    def deletar_aluno(self, id: str):
        delete_result = self.collection.delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return True  # sucesso

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com ID {id} não encontrado"
        )

    def atualizar_aluno(self, id: str, aluno_update: UpdateModel = Body(...)):
        update_data = aluno_update.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado fornecido para atualização"
            )

        update_result = self.collection.update_one(
            {"_id": id},
            {"$set": update_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail=f"Curso com ID {id} não foi modificado"
            )

        if (
                updated_curso := self.collection.find_one({"_id": id})
        ) is not None:
            return updated_curso

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {id} não encontrado"
        )

    def burcar_aluno_por_cpf(self, cpf: str):
        aluno = self.collection.find_one({"cpf": cpf})
        if aluno is not None:
            return aluno
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe aluno para este cpf: {cpf}")