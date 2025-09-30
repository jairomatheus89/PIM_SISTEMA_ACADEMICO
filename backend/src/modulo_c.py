#uma funcao em relatorio e outra na aluno_screen
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
