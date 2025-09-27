import requests

#sempre altetar caso mude de ip e porta

SERVIDOR = "http://localhost:8000"


def autenticar_usuario_api(login, senha):
    url = f"{SERVIDOR}/login"

    dados = {"usuario": login, "senha": senha}
    
    
    try:
        resposta = requests.post(url, json=dados, timeout=5)  # timeout evita travar
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e: #nao vou tratar o erro : {str(e)}
        return {"sucesso": False, "mensagem": f"Erro ao conectar no servidor!"}



def listar_turmas_api(id_professor):

    url = f"{SERVIDOR}/turmas?id_professor={id_professor}"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # levanta exceção se status code >= 400
        return resposta.json()       # retorna o JSON do backend
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro de conexão: {str(e)}"}
    
def listar_alunos_api(id_turma):
    # """
    # Chama a API para listar alunos de uma turma específica.
    # Retorna um dicionário com 'sucesso' e a lista de alunos.
    # """
    url = f"{SERVIDOR}/alunos?id_turma={id_turma}"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # dispara erro se status != 200
        return resposta.json()
    except requests.exceptions.RequestException as e:
        # Se houver erro de conexão ou HTTP, retorna sucesso=False e mensagem
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}

def listar_atividades_aluno_api(ra):
   
    url = f"{SERVIDOR}/atividades_aluno?ra={ra}"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # dispara erro se status != 200
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}

def listar_materias_aluno_api(ra: str):
    """
    Chama o endpoint /materias_aluno para listar as matérias do aluno pelo RA.
    Retorna:
        {"sucesso": True, "materias": [...]}
        {"sucesso": False, "mensagem": "..."}
    """
    url = f"{SERVIDOR}/materias_aluno?ra={ra}"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException:
        return {"sucesso": False, "mensagem": "Erro ao conectar no servidor"}


def listar_atividades_api(id_professor):
    url = f"{SERVIDOR}/atividades_professor?id_professor={id_professor}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro de conexão: {str(e)}"}
    
def criar_atividade_api(payload):
    # """
    # Chama a API para criar uma nova atividade.
    # payload deve conter:
    # - nome_atividade
    # - descricao
    # - turmas (lista de ids)
    # - data_entrega
    # - professor_id
    # """
    url = f"{SERVIDOR}/criar_atividades"

    try:
        resposta = requests.post(url, json=payload, timeout=5)  # adiciona timeout para evitar travamento
        resposta.raise_for_status()
        return resposta.json()  # retorna o JSON do backend
    except requests.exceptions.RequestException:
        return {"sucesso": False, "mensagem": "Erro ao conectar no servidor!"}
 
def editar_atividade_api(payload):
    # """
    # Chama a API para editar uma atividade existente.
    # payload deve conter:
    # - id_atividade
    # - nome_atividade
    # - descricao
    # - data_entrega
    # - professor_id
    # """
    url = f"{SERVIDOR}/editar_atividade"

    try:
        resposta = requests.put(url, json=payload)  
        resposta.raise_for_status()  
        return resposta.json()  
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}
    
def excluir_atividade_api(payload):
    # """
    # Chama a API para excluir uma atividade existente.
    # payload deve conter:
    # - id_atividade
    # - professor_id
    # """
    url = f"{SERVIDOR}/excluir_atividade"

    try:
        resposta = requests.delete(url, json=payload)  # DELETE para exclusão
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}

def salvar_nota_api(payload):
    # """
    # Chama a API para salvar ou atualizar a nota e o status de entrega de um aluno.
    
    # payload deve conter:
    # - id_aluno (obrigatório)
    # - id_atividade (obrigatório)
    # - nota (obrigatório)
    # - entregue (opcional, True ou False)
    # - professor_id (opcional)
    # """
    url = f"{SERVIDOR}/salvar_nota"

    try:
        resposta = requests.post(url, json=payload)  # POST para criar ou atualizar
        resposta.raise_for_status()  # dispara erro se status >= 400
        return resposta.json()       # retorna {'sucesso': True} ou {'sucesso': False, 'mensagem': ...}
    except requests.exceptions.RequestException as e:
        # Inclui a mensagem de erro técnico para depuração sem quebrar o fluxo
        return {"sucesso": False, "mensagem": f"Erro ao conectar no servidor"}

def buscar_nota_api(id_aluno, id_atividade):
    # """
    # Busca a nota de um aluno em uma atividade específica.
    
    # Retorna:
    # - {"sucesso": True, "nota": 8.5, "entregue": True}
    # - {"sucesso": False, "mensagem": "..."}
    # """
    url = f"{SERVIDOR}/buscar_nota"

    try:
        resposta = requests.get(url, params={"id_aluno": id_aluno, "id_atividade": id_atividade})
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException:
        return {"sucesso": False, "mensagem": "Erro ao conectar no servidor"}


def listar_materias_aluno_id_api(id_aluno: int):
    url = f"{SERVIDOR}/materias_aluno_id?id_aluno={id_aluno}"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        return {
            "sucesso": dados.get("sucesso", False),
            "materias": dados.get("materias", []),
            "nome_aluno": dados.get("nome_aluno", "Aluno")
        }
    except requests.exceptions.RequestException:
        return {"sucesso": False, "mensagem": "Erro ao conectar no servidor", "nome_aluno": "Aluno"}


def listar_atividades_aluno_id_api(id_aluno: int):
    url = f"{SERVIDOR}/atividades_aluno_id?id_aluno={id_aluno}"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()

        for atividade in dados.get("atividades", []):
            if "materia" not in atividade or atividade["materia"] is None:
                atividade["materia"] = "N/A"
            if "id_professor" not in atividade or atividade["id_professor"] is None:
                atividade["id_professor"] = -1

        return {
            "sucesso": dados.get("sucesso", False),
            "atividades": dados.get("atividades", []),
            "nome_aluno": dados.get("nome_aluno", "Aluno"),
            "ra": dados.get("ra", "")
        }
    except requests.exceptions.RequestException:
        return {
            "sucesso": False,
            "mensagem": "Erro ao conectar no servidor",
            "nome_aluno": "Aluno",
            "ra": ""
        }



def pegar_ra_id_alunos_api():
    # """
    # Chama o endpoint /pegar_ra_id_alunos para obter todos os RAs e IDs.
    # Retorna lista de dicionários: [{"ra": "123456", "id_aluno": 1}, ...]
    # """
    url = f"{SERVIDOR}/pegar_ra_id_alunos"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("sucesso") and "alunos" in dados:
            return dados["alunos"]
        return []
    except requests.exceptions.RequestException:
        return []