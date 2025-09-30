import ctypes
import os

#------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- MODULO  RA ----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#



# pega a pasta onde está este arquivo (conversor.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# monta o caminho até a DLL (na mesma pasta do conversor.py)
caminho_ra = os.path.join(BASE_DIR, "ra_gerador.dll")

# Carrega a DLL
funcao_ra = ctypes.CDLL(caminho_ra)

# Oq a funçao retorna:
funcao_ra.gerador_ra.restype = ctypes.c_int #retorna int

# Função que será chamada externamente
def geradorzin():
    return funcao_ra.gerador_ra()

#------------------------------------------------------------------------------------------------------------------#








#------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- MODULO  MEDIA ----------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------#


# Monta o caminho até a DLL
caminho_media = os.path.join(BASE_DIR, "calcular.dll")

# Carrega a DLL
funcao_media = ctypes.CDLL(caminho_media)

# Definição da função C
funcao_media.calcular_media.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int) #argumentos -> ponteiro pro vetor & tamanho inteiro
funcao_media.calcular_media.restype = ctypes.c_float #retorna float






def calcular_media_status(notas, media_minima=7):
    if not notas:
        return 0, "Reprovado"
    

    #------------------------------------------------------------#
    #     Convertendo a lista de python pra -> array de C        #
    vetor_vazio = ctypes.c_float * len(notas) 
    """
    array_type gera um vetor em C com o tamanho passado em (notas) 
    exemplo: notas[3] = {? , ? , ?}
    """
    preenche_vetor = vetor_vazio(*notas)
    """
    preenche_vetor pega o (vetor_vazio) e com um ponteiro *notas 
    cada nota é instanciada e atribuida ao vetor_vazio.
    """
    #------------------------------------------------------------#

    #------------------------------------------------------------#
    #                   Chama a função C                         #
    """
    aqui é onde vai instaciar a função do modulo C, puxando a função
    calcular_media e passando os parametros:

    -> preenche_vetor como : notas   ---------->  float* notas
    -> len(notas) como : tamanho do vetor ----->  int qtd
    """
    media = funcao_media.calcular_media(preenche_vetor, len(notas))
    #------------------------------------------------------------#
    
    #------------------------------------------------------------#
    #                 Aprovado ou Reprovado                      #
    status = "Aprovado" if media >= media_minima else "Reprovado"
    #                                                            #   
    #------------------------------------------------------------#
    return media, status
    #------------------------------------------------------------#

