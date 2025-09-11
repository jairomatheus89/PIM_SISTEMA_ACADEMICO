import requests

#sempre altetar caso mude de ip e porta

SERVIDOR = "http://26.207.69.216:8000"


def autenticar_usuario_api(login, senha):

    url = f"{SERVIDOR}/login"

    dados = {"usuario": login, "senha": senha}
    
    resposta = requests.post(url, json=dados)
    
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return {"erro": "Falha na requisição"}


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

