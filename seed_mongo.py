from pymongo import MongoClient
from faker import Faker
import uuid
import random
from dotenv import dotenv_values

config = dotenv_values(".env")

# Conectar ao MongoDB
client = MongoClient(config["MONGODB_CONNECTION_URI"])
db = client[config["DB_NAME"]]
cursos_collection = db["cursos"]
alunos_collection = db["alunos"]

# Limpar coleções
cursos_collection.delete_many({})
alunos_collection.delete_many({})

# Faker
faker = Faker("pt_BR")

# Gerar cursos
def seed_cursos(qtd=50000):
    cursos = []
    for _ in range(qtd):
        curso = {
            "_id": str(uuid.uuid4()),
            "nome": faker.job(),
            "carga_horaria": f"{random.randint(20, 100)} horas",
            "descricao": faker.sentence(),
            "media_aprovacao": round(random.uniform(6.0, 9.0), 1)
        }
        cursos.append(curso)
    cursos_collection.insert_many(cursos)
    print(f"{qtd} cursos inseridos.")
    return [curso["_id"] for curso in cursos]

# Gerar alunos
def seed_alunos(qtd=1000000, curso_ids=None):
    alunos = []
    for i in range(qtd):
        aluno = {
            "_id": str(uuid.uuid4()),
            "nome": faker.first_name(),
            "sobrenome": faker.last_name(),
            "email": f"aluno{i}@teste.com",  # garante unicidade
            "cpf": f"{random.randint(10000000000, 99999999999)}",  # também único
            "rua": faker.street_name(),
            "bairro": faker.bairro(),
            "cep": faker.postcode(),
            "cursos": random.sample(curso_ids, random.randint(1, 3))
        }
        alunos.append(aluno)

        # Inserção em blocos para evitar uso excessivo de memória
        if len(alunos) >= 10000:
            alunos_collection.insert_many(alunos)
            print(f"{i + 1} alunos inseridos...")
            alunos = []

    # Inserir o restante
    if alunos:
        alunos_collection.insert_many(alunos)
        print(f"{qtd} alunos inseridos.")

if __name__ == "__main__":
    curso_ids = seed_cursos(qtd=50000)
    seed_alunos(qtd=1000000, curso_ids=curso_ids)
