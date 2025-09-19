import ctypes
import os

# Puxa a dll

funcao = ctypes.CDLL("C:/Users/USER/Documents/GitHub/PIM_SISTEMA_ACADEMICO/Backend/src/ra_gerador.dll")


# Oq a funçao retorna?

funcao.gerar_ra.restype = ctypes.c_int #retorna int

# Função que será chamada externamente
def geradorzin():
    return funcao.gerar_ra()

def calcular_media_status(notas, media_minima=7):
    """
    Calcula a média de uma lista de notas e retorna a média e status.
    notas: lista de números
    media_minima: valor mínimo para aprovação
    Retorna: (media, status)
    """
    if not notas:
        return 0, "Reprovado"
    
    # Converte todos os valores para float, garantindo que strings não quebrem
    notas_numericas = [float(n) for n in notas]
    media = sum(notas_numericas) / len(notas_numericas)
    status = "Aprovado" if media >= media_minima else "Reprovado"
    return media, status

