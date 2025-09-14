import sqlite3
from fastapi import FastAPI, Request ,Query
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

@app.get("/atividades_professor")
def listar_atividades_professor(id_professor: int = Query(..., description="ID do professor")):
    banco = get_banco()
    cursor = banco.cursor()

    # Pega todas as atividades do professor
    cursor.execute("""
        SELECT A.id_atividade, A.nome_atividade, A.descricao, A.data_entrega
        FROM Atividades A
        WHERE A.id_professor = ?
    """, (id_professor,))
    atividades = cursor.fetchall()

    resultado = []
    for a in atividades:
        # Pega as turmas vinculadas a cada atividade
        cursor.execute("""
            SELECT T.id_turma, T.nome_turma
            FROM Turma T
            LEFT JOIN Turma_Atividade TA ON T.id_turma = TA.id_turma
            WHERE TA.id_atividade = ?
        """, (a["id_atividade"],))
        turmas = [dict(t) for t in cursor.fetchall()]

        resultado.append({
            "id_atividade": a["id_atividade"],
            "nome_atividade": a["nome_atividade"],
            "descricao": a["descricao"],
            "data_entrega": a["data_entrega"],
            "turmas": turmas
        })

    banco.close()
    return {"sucesso": True, "atividades": resultado}


@app.post("/criar_atividades")
async def criar_atividade(request: Request):
    """
    Recebe dados de uma nova atividade do frontend e salva no banco.
    Espera um JSON com:
    {
        "nome_atividade": "...",
        "descricao": "...",
        "data_entrega": "yyyy-mm-dd",
        "professor_id": 1,
        "turmas": [1, 2]   # IDs das turmas vinculadas
    }
    """
    dados = await request.json()
    nome_atividade = dados.get("nome_atividade")
    descricao = dados.get("descricao")
    data_entrega = dados.get("data_entrega")
    professor_id = dados.get("professor_id")
    turmas = dados.get("turmas", [])

    banco = get_banco()
    cursor = banco.cursor()

    try:
        # Inserir atividade
        cursor.execute(
            "INSERT INTO Atividades (id_professor, nome_atividade, descricao, data_entrega) VALUES (?, ?, ?, ?)",
            (professor_id, nome_atividade, descricao, data_entrega)
        )
        id_atividade = cursor.lastrowid

        # Vincular atividade às turmas
        for turma_id in turmas:
            cursor.execute(
                "INSERT INTO Turma_Atividade (id_turma, id_atividade) VALUES (?, ?)",
                (turma_id, id_atividade)
            )

        banco.commit()
        banco.close()
        return {"sucesso": True, "id_atividade": id_atividade}

    except Exception as e:
        banco.rollback()
        banco.close()
        return {"sucesso": False, "mensagem": str(e)}

@app.put("/editar_atividade")
async def editar_atividade(request: Request):
    """
    {
        "id_atividade": 1,
        "nome_atividade": "...",
        "descricao": "...",
        "data_entrega": "yyyy-mm-dd",
        "professor_id": 1
    }
    """
    dados = await request.json()
    id_atividade = dados.get("id_atividade")
    nome_atividade = dados.get("nome_atividade")
    descricao = dados.get("descricao")
    data_entrega = dados.get("data_entrega")
    professor_id = dados.get("professor_id")

    if not id_atividade:
        return {"sucesso": False, "mensagem": "ID da atividade não fornecido"}

    banco = get_banco()
    cursor = banco.cursor()

    try:
        # Atualizar apenas dados da atividade (sem alterar turmas)
        cursor.execute(
            """
            UPDATE Atividades
            SET nome_atividade = ?, descricao = ?, data_entrega = ?, id_professor = ?
            WHERE id_atividade = ?
            """,
            (nome_atividade, descricao, data_entrega, professor_id, id_atividade)
        )

        banco.commit()
        banco.close()
        return {"sucesso": True}

    except Exception as e:
        banco.rollback()
        banco.close()
        return {"sucesso": False, "mensagem": str(e)}

@app.delete("/excluir_atividade")
async def excluir_atividade(request: Request):
    """
    Exclui uma atividade do banco de dados.
    Espera um JSON com:
    {
        "id_atividade": 1,
        "professor_id": 1
    }
    """
    dados = await request.json()
    id_atividade = dados.get("id_atividade")

    if not id_atividade:
        return {"sucesso": False, "mensagem": "ID da atividade não fornecido"}

    banco = get_banco()
    cursor = banco.cursor()

    try:
        # 1. Excluir notas vinculadas à atividade
        cursor.execute("DELETE FROM Notas WHERE id_atividade = ?", (id_atividade,))
        
        # 2. Excluir vínculo da atividade com turmas
        cursor.execute("DELETE FROM Turma_Atividade WHERE id_atividade = ?", (id_atividade,))
        
        # 3. Excluir a própria atividade
        cursor.execute("DELETE FROM Atividades WHERE id_atividade = ?", (id_atividade,))

        banco.commit()
        banco.close()
        return {"sucesso": True}

    except Exception as e:
        banco.rollback()
        banco.close()
        return {"sucesso": False, "mensagem": str(e)}

@app.post("/salvar_nota")
async def salvar_nota(request: Request):
    """
    Recebe dados do frontend para salvar a nota e o status de entrega de um aluno.
    Espera um JSON com:
    {
        "id_aluno": 1,
        "id_atividade": 1,
        "nota": 8.5,
        "entregue": True  # opcional, padrão é False
    }
    """
    dados = await request.json()
    id_aluno = dados.get("id_aluno")
    id_atividade = dados.get("id_atividade")
    nota = dados.get("nota")
    entregue = dados.get("entregue", False)  # se não informado, assume False

    if id_aluno is None or id_atividade is None or nota is None:
        return {"sucesso": False, "mensagem": "Campos obrigatórios não fornecidos"}

    banco = get_banco()
    cursor = banco.cursor()

    try:
        # Insere a nota ou atualiza se já existir, incluindo o status de entrega
        cursor.execute("""
            INSERT INTO Notas (id_aluno, id_atividade, nota, entregue)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id_aluno, id_atividade)
            DO UPDATE SET 
                nota=excluded.nota,
                entregue=excluded.entregue
        """, (id_aluno, id_atividade, nota, int(entregue)))  # sqlite usa 0/1 para booleanos

        banco.commit()
        banco.close()
        return {"sucesso": True}

    except Exception as e:
        banco.rollback()
        banco.close()
        return {"sucesso": False, "mensagem": str(e)}
