# Força Bruta em Carteiras de Bitcoin.

A geração de carteiras de Bitcoin é feita através de criptografia assimétrica, onde a partir de uma chave privada, gera-se uma chave pública e a partir dela, o endereço da carteira que é usado para receber moedas. Devido ao algoritmo de Curvas Elípticas utilizado na criptografia de geração de chaves, só pode-se fazer um caminho de mão única como é visto na imagem abaixo, ou seja, partindo da geração da chave privada até chegar no endereço da carteira.

![Geração de chaves de Bitcoin - Fonte: Oreilly](https://github.com/clebrw/Parallel-Bitcoin-Brute-Force/blob/main/private-public-address-oreilly.png?raw=true)

Em termos de segurança, temos 256 bits de possibilidades para geração de carteiras, isso representa um número de 78 dígitos, ou seja, só não é maior que a quantidade de átomos do universo observável.

|Objeto |Qtde |
|---------------------|---------------------------|
| Galáxias            | 10^11 à 10^12 galáxias |
| Estrelas            | 10^22 à 10^24 estrelas |
| Uma pessoa          | 7*10^27 átomos |
| População Mundial   | 5*10^37 átomos |
| Endereços Bitcoin   | 1,15*10^77 endereços |
| Universo Observável | 10^82 átomos |
 
Com base nesses dados, é possível notar que é bastante improvável gerar duas vezes o mesmo endereço de Bitcoin se usados métodos seguros de randomização na geração das chaves. Assim sendo, é praticamente impossível conseguir a chave privada de algum endereço com saldo diferente de zero utilizando força bruta, pois levaria muitos anos de computação para encontrar algum.

## Resumo

Partindo do princípio de que se tem curiosidade e pretende-se tirar a prova real de quão difícil é achar um endereço com saldo diferente de zero, foi desenvolvido um algoritmo que gera um novo endereço de bitcoin e testa se o mesmo encontra-se em uma lista de endereços de bitcoin com saldo diferente de zero. Em caso afirmativo, o que é raro de acontecer, o endereço e sua chave privada serão salvos em um arquivo de texto.

Aproveitando dos conhecimentos de paralelização adquiridos ao longo da Disciplina de Programação Paralela (ELC139), foram desenvolvidos dois algoritmos em Python, um utilizando Process e outro Threads para efeitos de comparação, cujos dados de SpeedUp serão mostrados em seguida.

## Diferenças entre Processos e Threads

Em Python, quando criamos um **Processo**, um núcleo do processador pode ser atribuído à ele, logo, se temos um processador Quadcore, podemos criar quatro processos e o desempenho será quase quatro vezes superior ao de um núcleo. Ele não será exatamente quatro vezes mais rápido, porque o sistema gerencia os processos e entre eles temos os processos do sistema operacional que também estão requisitando CPU.

Quando estamos trabalhando com **Threads**, pode-se criar várias dentro de um processo, porém eles sofrem um bloqueio, onde apenas um núcleo da CPU é destinado às infinitas threads que podem ser criadas. Este bloqueio é gerenciado pelo Global Interpreter Lock (GIL) que restringe as threads e faz com que funcione como uma única thread se faz necessário porque o interpretador Python não é seguro para threads.

Comprova-se isso através do gráfico de SpeedUp gerado a partir de um código que foi paralelizado usando threads e processos. É possível observar que há um ganho de desempenho quando trabalhamos com processos e o mesmo não ocorre quando estamos usando threads no Python.

![SpeedUp - Threads vs Process ](https://github.com/clebrw/Parallel-Bitcoin-Brute-Force/blob/main/SpeedUp.png?raw=true)
