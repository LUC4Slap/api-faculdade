import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

from dtos.relatorio_curso_dto import RelatroioCursoDto
from models.alunoComCursosModel import CursoModel, AlunoComCursosModel
from models.cursos import ListModelCursos
from models.paginacaoModel import PaginacaoAlunosResponse


class RelatorioService():
    def __init__(self, request: Request):
        self.db = request.app.database
        self.collection = self.db["cursos"]
        self.alunoCollection = self.db["alunos"]
        self.request = request
        self.caminho_wkhtmltopdf = None #os.path.join("htmlToPdfBin", "wkhtmltopdf")

    def gerar_relatorio_curso(self, dto: RelatroioCursoDto):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("relatorio_cursos.html")
        operator = ""
        titulo = ""

        if dto.gte:
            operator = "$gte"
            titulo = f"Relatório para media maiores que {dto.media}"
        elif dto.lte:
            operator = "$lte"
            titulo = f"Relatório para media menores que {dto.media}"
        elif dto.lte == False and dto.gte == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deve se passar algum parametro com True para gerar o relatorio"
            )

        cursos_cursor = self.collection.find({"media_aprovacao": {operator: dto.media}})
        relatorio_dados = []

        for curso_doc in cursos_cursor:
            curso = CursoModel(**curso_doc)

            alunos_cursor = self.alunoCollection.find({"cursos": curso.id})
            alunos = [AlunoComCursosModel(**a) for a in alunos_cursor]

            relatorio_dados.append({
                "curso": curso,
                "alunos": alunos
            })

        html = template.render(dados=relatorio_dados, titulo=titulo)
        config = pdfkit.configuration()

        pdf_path = "/tmp/relatorio_cursos.pdf"
        pdfkit.from_string(html, pdf_path, configuration=config)

        return pdf_path