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
        self.caminho_wkhtmltopdf = None #os.path.join("htmlToPdfBin", "wkhtmltopdf")

    def gerar_relatorio_curso(self, filtros):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("relatorio_cursos.html")

        cursos_cursor = self.collection.find({"media_aprovacao": {"$gt": filtros}})
        relatorio_dados = []

        for curso_doc in cursos_cursor:
            curso = CursoModel(**curso_doc)

            alunos_cursor = self.alunoCollection.find({"cursos": curso.id})
            alunos = [AlunoComCursosModel(**a) for a in alunos_cursor]

            relatorio_dados.append({
                "curso": curso,
                "alunos": alunos
            })

        html = template.render(dados=relatorio_dados)
        config = pdfkit.configuration()

        pdf_path = "/tmp/relatorio_cursos.pdf"
        pdfkit.from_string(html, pdf_path, configuration=config)

        return pdf_path