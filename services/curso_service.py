from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

from models.alunoComCursosModel import CursoModel, AlunoComCursosModel
from models.cursos import ListModelCursos
from models.paginacaoModel import PaginacaoAlunosResponse


class CursoService():
    def __init__(self, request: Request):
        self.db = request.app.database
        self.collection = self.db["cursos"]
        self.alunoCollection = self.db["alunos"]
        self.request = request

    def listar_cursos(self, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000)):
        cusosDb = list(self.collection.find(limit=50))
        return cusosDb

    def criar_curso(self, curso: ListModelCursos):
        list = jsonable_encoder(curso)
        new_list_item = self.collection.insert_one(list)
        created_list_item = self.collection.find_one({
            "_id": new_list_item.inserted_id
        })
        return created_list_item

    def update_curso(self, id: str, curso: ListModelCursos):
        update_data = curso.dict(exclude_unset=True)

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

    def deletar_curso(self, id: str):
        delete_result = self.collection.delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Item with {id} excluido com sucesso")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item with {id} not found")

    def buscar_curso_por_id(self, id: str):
        curso = self.collection.find_one({ "_id": id })
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item with {id} not found")
        return curso

    def listar_curso_alunos(self, curso_id: str, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000)):
        skip = (page - 1) * limit

        total = self.alunoCollection.count_documents({"cursos": curso_id})
        cursor = self.alunoCollection.find({"cursos": curso_id}).skip(skip).limit(limit)

        alunos = []
        for aluno in cursor:
            cursos_info = []
            for c_id in aluno.get("cursos", []):
                curso_doc = self.collection.find_one({"_id": c_id})
                if curso_doc:
                    cursos_info.append(CursoModel(**curso_doc))
            aluno["cursos_info"] = cursos_info
            alunos.append(AlunoComCursosModel(**aluno))

        return PaginacaoAlunosResponse(
            page=page,
            limit=limit,
            total=total,
            has_next=(page * limit < total),
            data=alunos
        )
