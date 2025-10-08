#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Função que gera um RA 
int gerador_ra() 
{

    // Inicia a semente do tempo atual do pc
    srand(time(NULL));


    int ra = 0;
    // RA de 6 digitos
    // A cada laço gera um numero aleatorio pro RA
    // No final retorna o RA inteiro com os 6 digitos aleatorios
    for(int i = 0; i < 6; i++)
    {
        int numero = 1 + rand() % 9;
        ra = ra * 10 + numero; // adiciona o numero a direita
    }
    
    return ra;
}
