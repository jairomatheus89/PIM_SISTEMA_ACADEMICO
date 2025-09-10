import sqlite3
from fastapi import FastAPI, Request , Query
from fastapi.middleware.cors import CORSMiddleware

#python -m uvicorn main:app --host 26.207.69.216 --port 8000 --reload

# Função para conectar no banco
def get_banco():
    banco = sqlite3.connect("database.db")
    banco.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return banco

app = FastAPI()

# Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, colocar apenas o domínio do frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"mensagem": "conectou"}


@app.post("/login")
async def login(request: Request):
    dados = await request.json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    banco = get_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM Professores WHERE usuario = ? AND senha = ?", (usuario, senha))

    professor = cursor.fetchone()
    banco.close()

    if professor:
        return {"sucesso": True,
                "id_professor": professor["id_professor"],
                "nome": professor["nome"],
                "materia": professor["materia"]}
    else:
        return {"sucesso": False, "mensagem": "Usuário ou senha incorretos"}
    

@app.get("/turmas")
def listar_turmas(id_professor: int):
    banco = get_banco()
    cursor = banco.cursor()
    
    cursor.execute("SELECT id_turma FROM Turma_Professor WHERE id_professor = ?", (id_professor,))
    turmas_ids = [row["id_turma"] for row in cursor.fetchall()]
    
    if turmas_ids:
        cursor.execute(f"SELECT * FROM Turma WHERE id_turma IN ({','.join(['?']*len(turmas_ids))})", turmas_ids)
        turmas = [dict(row) for row in cursor.fetchall()]
    else:
        turmas = []

    banco.close()
    return {"sucesso": True, "turmas": turmas}

@app.get("/alunos")
def listar_alunos(id_turma: int = Query(..., description="ID da turma")):
    banco = get_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT * FROM Aluno WHERE id_turma = ?", (id_turma,))
    alunos = [dict(row) for row in cursor.fetchall()]

    banco.close()

    if alunos:
        return {"sucesso": True, "alunos": alunos}
    else:
        return {"sucesso": False, "mensagem": "Nenhum aluno encontrado para essa turma"}
    
    
@app.get("/atividades_aluno")
def listar_atividades_aluno(ra: str = Query(..., description="RA do aluno")):
    banco = get_banco()
    cursor = banco.cursor()

    # Primeiro pega o ID do aluno pelo RA
    cursor.execute("SELECT id_aluno FROM Aluno WHERE ra = ?", (ra,))
    aluno = cursor.fetchone()
    if not aluno:
        banco.close()
        return {"sucesso": False, "mensagem": "Aluno não encontrado"}

    id_aluno = aluno["id_aluno"]

    cursor.execute("""
        SELECT A.nome_atividade, A.data_entrega, N.nota, N.entregue
        FROM Atividades A
        LEFT JOIN Turma_Atividade TA ON A.id_atividade = TA.id_atividade
        LEFT JOIN Aluno Al ON Al.id_turma = TA.id_turma
        LEFT JOIN Notas N ON A.id_atividade = N.id_atividade AND N.id_aluno = Al.id_aluno
        WHERE Al.id_aluno = ?
    """, (id_aluno,))

    atividades = [dict(row) for row in cursor.fetchall()]
    banco.close()

    return {"sucesso": True, "atividades": atividades}