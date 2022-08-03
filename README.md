# Parallel Bitcoin Brute Force in Wallets.

A geração de carteiras de Bitcoin é feita através de criptografia assimétrica, onde a partir de uma chave privada, gera-se uma  chave pública e o endereço da carteira conseguentemente. Em termos de segurança, pode-se ser gerada carteiras com 128bits (2^128^)  até endereços de 256 bits (2^256^), ou seja, são mais endereços que o numeros de grão de areia que existem no planeta terra. 

## Diferenças entre Processos e Threads

Em Python, quando criamos um **Processo**, um nucleo do processador pode ser atribuido á ele, logo, se temos um processador  Quadcore, podemos criar quatro processos e o desempenho será quase quatro vezes superiror ao de um núcleo. Ele não será exatamente quatro vezes mais rápido, porque o sistema gerencia os processos e entre eles temos os processos do sistema operacional que também estão requisitando CPU.

Quando estamos trabalhando com **Threads**, pode-se criar várias dentro de um processo, porém eles sofrem um bloqueio, onde apenas um núcleo da CPU é destinado às infinitas threads que podem ser criadas. Este bloqueio é gerenciado pelo Global Interpreter Lock (GIL) que restringe as threads e faz com que funcione como uma única thread se faz necessário porque o interpretador Python não é seguro para threads.

Comprova-se isso através do grafico de SpeedUp gerado a partir de um codigo que foi paralelizado usando threads e processos. É possivel observar que há um ganho de desempenho quando trabalhamos com processos e o mesmo não cocorre quando estamos usando threads no Python.

![SpeedUp - Threads vs Process ](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/speedup.png?token=GHSAT0AAAAAABXIFM3WGB3ZLJ5YTTSWSVFYYXJ6PWA)
