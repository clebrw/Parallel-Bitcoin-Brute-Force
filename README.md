
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

## Código
A geração de chaves é feita utilizando a função *Key()* da biblioteca **bit**. Utilizamos neste caso a *Key.from_int()* para que o teste de desempenho seja o mais controlado possível, assim todos os testes irão gerar os mesmos endereços e testá-los.

    def test_wallet(start, end):
        for i in range(start, end+1):
            pk = Key.from_int(i)
            if pk.address in wallets:
                with open('found.txt', 'a') as result:
                    result.write(f'ADDR:{pk.address} - PK:{pk.to_wif()}\n')
                print(f'\n *** Added address to found.txt ***')

Uma das formas de descobrir se uma carteira gerada possui saldo é verificado online em alguns sites de exploradores de blockchain, porém isso é algo que demora alguns segundos e na maioria das vezes é imposto um limite de consultas por IP. Outro método bem mais rápido que pode ser usado é baixar um arquivo de texto com as carteiras que possuem saldo diferente de zero, assim toda verificação é local e não demanda consultas online para funcionar. Esta segunda abordagem foi utilizada neste trabalho, onde baixou-se um compilado de endereços, mais de 42 milhões, no site (http://addresses.loyce.club/), extraiu-se o arquivo de texto *Bitcoin_addresses_LATEST.txt* no mesmo diretório dos arquivos Python. 

Na função *test_wallet()*, após ser gerado uma carteira, verificamos se este endereço existe dentro do arquivo de carteiras com saldo não nulo, caso exista, o endereço e a chave privada são gravados no arquivo *found.txt*, senão o próximo endereço é testado.

## Paralelismo
Como este algoritmo envolve operações mais básicas, como uma busca em uma string que contém as carteiras separadas pelos caracteres */n*, não foi difícil paralelizar suas operações. 
No primeiro momento foi utilizada a função *Process( )* da biblioteca *multiprocessing* que chegou no objetivo de paralelizar os testes de endereços. Num segundo momento, foi testado a função *Thread( )* da biblioteca *threading*, que não funcionou como esperava-se por causa de um bloqueio que existe na linguagem Python se tratando da parte de thread. 


## Diferenças entre Processos e Threads

Em Python, quando criamos um **Processo**, um núcleo do processador pode ser atribuído à ele, logo, se temos um processador Quadcore, podemos criar quatro processos e o desempenho será quase quatro vezes superior ao de um núcleo. Ele não será exatamente quatro vezes mais rápido, porque o sistema gerencia os processos e entre eles temos os processos do sistema operacional que também estão requisitando CPU.

Quando estamos trabalhando com **Threads**, pode-se criar várias dentro de um processo, porém eles sofrem um bloqueio, onde apenas um núcleo da CPU é destinado às infinitas threads que podem ser criadas. Este bloqueio é gerenciado pelo Global Interpreter Lock (GIL) que restringe as threads e faz com que funcione como uma única thread se faz necessário porque o interpretador Python não é seguro para threads.

Comprova-se isso através do gráfico de SpeedUp gerado a partir de um código que foi paralelizado usando threads e processos. É possível observar que há um ganho de desempenho quando trabalhamos com processos e o mesmo não ocorre quando estamos usando threads no Python.

Para gerar o grafico de SpeedUp, foram testados 1 Milhão de endereços para cada processo ou thread que era adicionado e além disso, cada teste era repetido três vezes para então fazer uma média dos valores e ter um resultado mais confiável de tempo de execução.

![SpeedUp - Threads vs Process ](https://github.com/clebrw/Parallel-Bitcoin-Brute-Force/blob/main/SpeedUp.png?raw=true)

## Profilers


Para entender melhor o fluxo de dados, optou-se por fazer uma análise do código usando o profiler *cProfiler*. 
No entanto, este profiler não consegue obter informações de processos que foram criados, é como se ele não conseguisse rastrear o que acontece depois que eles são iniciados e somente detecta quando os processos retornam sua execução pela chamada *join( )*.

![cProfiler](https://github.com/clebrw/Parallel-Bitcoin-Brute-Force/blob/main/cProfile.png?raw=true)

Outra forma de analisar o fluxo de dados é através do gprof2dot que gera um grafico onde as cores quentes indicam maior execução.

![image](https://github.com/clebrw/Parallel-Bitcoin-Brute-Force/blob/main/gprof2dot_output_cProfile.png?raw=true)

