import requests

#sempre altetar caso mude de ip e porta

SERVIDOR = "http://26.207.69.216:8000"


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
    """
    Chama a API para listar alunos de uma turma específica.
    Retorna um dicionário com 'sucesso' e a lista de alunos.
    """
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

def listar_atividades_api(id_professor):
    url = f"{SERVIDOR}/atividades_professor?id_professor={id_professor}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro de conexão: {str(e)}"}
    
def criar_atividade_api(payload):
    """
    Chama a API para criar uma nova atividade.
    payload deve conter:
    - nome_atividade
    - descricao
    - turmas (lista de ids)
    - data_entrega
    - professor_id
    """
    url = f"{SERVIDOR}/criar_atividades"

    try:
        resposta = requests.post(url, json=payload)
        resposta.raise_for_status()  # dispara erro se status != 200
        return resposta.json()  # deve retornar {'sucesso': True, ...} ou {'sucesso': False, 'mensagem': ...}
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}
    
def editar_atividade_api(payload):
    """
    Chama a API para editar uma atividade existente.
    payload deve conter:
    - id_atividade
    - nome_atividade
    - descricao
    - data_entrega
    - professor_id
    """
    url = f"{SERVIDOR}/editar_atividade"

    try:
        resposta = requests.put(url, json=payload)  
        resposta.raise_for_status()  
        return resposta.json()  
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}
    
def excluir_atividade_api(payload):
    """
    Chama a API para excluir uma atividade existente.
    payload deve conter:
    - id_atividade
    - professor_id
    """
    url = f"{SERVIDOR}/excluir_atividade"

    try:
        resposta = requests.delete(url, json=payload)  # DELETE para exclusão
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"sucesso": False, "mensagem": f"Erro ao conectar na API: {str(e)}"}
