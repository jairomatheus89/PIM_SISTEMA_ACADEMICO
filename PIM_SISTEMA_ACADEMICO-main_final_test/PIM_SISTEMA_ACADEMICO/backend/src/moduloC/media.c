#include <stdio.h>
#include <stdlib.h>


float calcular_media(float* notas, int qtd) {
    if (qtd == 0) return 0.0f;

    float soma = 0.0f;
    for (int i = 0; i < qtd; i++) {
        soma += notas[i];
    }
    return soma / qtd;
}
