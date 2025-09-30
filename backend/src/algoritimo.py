import random

# -----------------------------
# Função Merge Sort
# -----------------------------
def merge_sort(arr):
    """Ordena uma lista de números usando Merge Sort."""
    if len(arr) <= 1:
        return arr
    meio = len(arr) // 2
    left = merge_sort(arr[:meio])
    right = merge_sort(arr[meio:])
    return merge(left, right)

def merge(left, right):
    """Auxiliar para Merge Sort: une duas listas ordenadas."""
    resultado = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            resultado.append(left[i])
            i += 1
        else:
            resultado.append(right[j])
            j += 1
    # Adiciona o que sobrou
    resultado.extend(left[i:])
    resultado.extend(right[j:])
    return resultado

# -----------------------------
# Função Busca Binária
# -----------------------------
def busca_binaria(arr, alvo):
    """Faz busca binária em uma lista ordenada.
    Retorna a posição do alvo ou -1 se não encontrado.
    """
    inicio = 0
    fim = len(arr) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if arr[meio] == alvo:
            return meio
        elif arr[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


# -----------------------------
# Função para criar mapeamento RA → id_aluno
# -----------------------------

def criar_mapeamento(ras):
    """Cria um dicionário RA → id_aluno (posição na lista + 1)."""
    return {ra: idx + 1 for idx, ra in enumerate(ras)}

# -----------------------------
# Função de busca de RA e retorno do id
# -----------------------------
def buscar_aluno(ras_ordenados, ra_para_id, ra_aluno):
    """Busca um RA na lista ordenada e retorna o id do aluno."""
    posicao = busca_binaria(ras_ordenados, ra_aluno)
    if posicao == -1:
        return None  # RA não encontrado
    return ra_para_id[ra_aluno]



# ras = gerar_ras(qtd=10)
# ra_para_id = criar_mapeamento(ras)
# ras_ordenados = merge_sort(ras)


# print("RAs gerados:", ras)
# print("RAs ordenados:", ras_ordenados)
# print("Mapeamento RA → id:", ra_para_id)


# ra_do_aluno = int(input("Digite um RA: "))
# id_aluno = buscar_aluno(ras_ordenados, ra_para_id, ra_do_aluno)

# if id_aluno:
#     print(f"RA {ra_do_aluno} encontrado! ID do aluno: {id_aluno}")
# else:
#     print("RA não encontrado!")
