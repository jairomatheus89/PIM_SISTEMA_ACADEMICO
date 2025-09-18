#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Função para gerar RA aleatório
int gerar_ra() {
    // Inicializa seed para números aleatórios
    srand(time(NULL) ^ (rand() << 15));
    
    // RA de 8 dígitos (ex: 12345678)
    int ra = 10000000 + rand() % 90000000;
    return ra;
}

int main()
{
    printf("%d", gerar_ra());
    return 0;
}