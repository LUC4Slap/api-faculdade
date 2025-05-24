import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

from models.alunoComCursosModel import CursoModel, AlunoComCursosModel
from models.cursos import ListModelCursos
from models.paginacaoModel import PaginacaoAlunosResponse


class RelatorioService():
    def __init__(self, request: Request):
        self.db = request.app.database
        self.collection = self.db["cursos"]
        self.alunoCollection = self.db["alunos"]
        self.request = request