import ctypes
import os

# Puxa a dll

funcao = ctypes.CDLL("C:/Users/USER/Documents/GitHub/PIM_SISTEMA_ACADEMICO/Backend/src/moduloC/ra_gerador.dll")


# Oq a funçao retorna?

funcao.gerador_ra.restype = ctypes.c_int #retorna int

# Função que será chamada externamente
def geradorzin():
    return funcao.gerador_ra()