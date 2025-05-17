from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes.routes_user import router as list_router
from routes.routes_cursos import router as cursos_controller

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(list_router, tags=["Alunos"], prefix="/alunos")
app.include_router(cursos_controller, tags=["Cursos"], prefix="/cursos")