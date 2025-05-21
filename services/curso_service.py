from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

class CursoService():
    def __init__(self, request: Request):
        self.db = request.app.database
        self.collection = self.db["cursos"]
        self.request = request

    def listar_cursos(self, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=10000)):
        cusosDb = list(self.collection.find(limit=50))
        return cusosDb