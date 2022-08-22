# Força Bruta em Carteiras de Bitcoin.

## Resumo

Partindo do princípio de que se tem curiosidade e pretende-se tirar a prova real de quão difícil é achar um endereço com saldo diferente de zero, foi desenvolvido um algoritmo que gera um novo endereço de bitcoin e testa se o mesmo encontra-se em uma lista de endereços de bitcoin com saldo diferente de zero. Em caso afirmativo, o que é raro de acontecer, o endereço e sua chave privada serão salvos em um arquivo de texto.

Aproveitando dos conhecimentos de paralelização adquiridos ao longo da Disciplina de Programação Paralela (ELC139), foram desenvolvidos dois algoritmos em Python, um utilizando Processos e outro Threads para efeitos de comparação, cujos dados de SpeedUp e Profilers serão mostrados logo mais.

## Introdução

A geração de carteiras de Bitcoin é feita através de criptografia assimétrica, onde a partir de uma chave privada, gera-se uma chave pública e a partir dela, o endereço da carteira que é usado para receber moedas. Devido ao algoritmo de Curvas Elípticas e Hashs utilizados na criptografia de geração de chaves, só pode-se fazer um caminho de mão única como é visto na imagem abaixo, ou seja, partindo da geração da chave privada até chegar no endereço da carteira.

![Geração de chaves de Bitcoin - Fonte: Oreilly](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/private-public-address-oreilly.png)

Em termos de segurança, temos 256 bits de possibilidades para geração de carteiras, isso representa um número de 78 dígitos, ou seja, só não é maior que a quantidade de átomos do universo observável.

|Objeto |Qtde |
|---------------------|---------------------------|
| Galáxias            | 10<sup>11</sup> à 10<sup>12</sup> galáxias |
| Estrelas            | 10<sup>22</sup> à 10<sup>24</sup> estrelas |
| Uma pessoa          | 7*10<sup>27</sup> átomos |
| População Mundial   | 5*10<sup>37</sup> átomos |
| Endereços Bitcoin   | 1,15*10<sup>77</sup> endereços |
| Universo Observável | 10<sup>82</sup> átomos |
 
Com base nesses dados, é possível notar que é bastante improvável gerar duas vezes o mesmo endereço de Bitcoin se usados métodos seguros de randomização na geração das chaves. Assim sendo, **é praticamente impossível conseguir a chave privada de algum endereço com saldo diferente de zero utilizando força bruta**, pois levaria milhares de anos para encontrar algum com o hardware disponível que temos hoje.

## Desenvolvimento
A geração de chaves é feita utilizando a função *Key()* da biblioteca **bit** que gera endereços do tipo *Pagar para Hash de chave pública* **(P2PKH)**. Utilizamos neste caso a *Key.from_int()* para que o teste de desempenho seja o mais controlado possível, assim todos os testes irão gerar os mesmos endereços e testá-los.

    def test_wallet(start, end):
        for i in range(start, end+1):
            pk = Key.from_int(i)
            if pk.address in wallets:
                with open('found.txt', 'a') as result:
                    result.write(f'ADDR:{pk.address} - PK:{pk.to_wif()}\n')
                print(f'\n *** Added address to found.txt ***')

Uma das formas de descobrir se uma carteira gerada possui saldo é verificando online em alguns sites de exploradores de blockchain, porém isso é algo que demora alguns segundos e na maioria das vezes é imposto um limite de consultas por IP. Outro método bem mais rápido que pode ser usado é baixar um arquivo de texto com as carteiras que possuem saldo diferente de zero, assim toda verificação é local e não demanda consultas online para funcionar. Esta segunda abordagem foi utilizada neste trabalho, onde baixou-se um compilado de endereços dos mais variados tipos, mais de 42 milhões, do site (http://addresses.loyce.club/), e extraiu-se o arquivo de texto *Bitcoin_addresses_LATEST.txt* no mesmo diretório dos arquivos Python. Como a função *Key()* trabalha com o tipo P2PKH, vamos filtrar apenas esses tipos de endereços para aumentar a eficiência de busca. Com a versão da data que foi escrito esse relatório(07/2022), tem-se 1.6GB de endereços e depois de aplicar o filtro, gerou-se um arquivo de aproximadamente 800MB. 

Na função *test_wallet()*, após ser gerado uma carteira, verificamos se o  endereço gerado existe dentro do arquivo de carteiras com saldo não nulo, caso exista, o endereço e a chave privada são gravados no arquivo *found.txt*, senão o próximo endereço é testado.

No repositório é possível encontrar **serial_BF_BTC.py** que é a versão não paralela do programa e **parallel_BF_BTC.py** que é a versão paralela usando Process, ambos geram chaves aleatórios e não são tão controlados como as versões **process_BF.py** e **thread_BF.py** que foram usados para fazer os testes de SpeedUp. Além disso, temos **select_P2PKH_text.py** que gera um arquivo de texto somente com endereços P2PKH, **wallets_bitcoin.txt** a partir do arquivo que possui os endereços de carteiras com saldos atualizados.  

### Paralelismo
Como este algoritmo envolve operações mais básicas, como uma busca em uma string que contém as carteiras separadas pelos caracteres *\n*, não foi difícil paralelizar suas operações. 
No primeiro momento foi utilizada a função *Process( )* da biblioteca *multiprocessing* que chegou no objetivo de paralelizar os testes de endereços. Num segundo momento, foi testado a função *Thread( )* da biblioteca *threading*, que não funcionou como esperava-se por causa de um bloqueio que existe na linguagem Python se tratando da parte de thread. 

### Diferenças entre Processos e Threads

![process vs threads_javatpoint](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/process-vs-thread_javatpoint.png)

Em Python, quando criamos um **Processo**, um núcleo do processador pode ser atribuído à ele, logo, se temos um processador Quadcore, podemos criar quatro processos e o desempenho será quase quatro vezes superior ao de um núcleo. Ele não será exatamente quatro vezes mais rápido, porque o sistema gerencia os processos e entre eles temos os processos do sistema operacional que também estão requisitando CPU.

Quando estamos trabalhando com **Threads**, pode-se criar várias dentro de um processo, porém eles sofrem um bloqueio, onde apenas uma thread é executada por vez. Este bloqueio é gerenciado pelo Global Interpreter Lock (**GIL**) que funciona como um *mutex*, fazendo com que apenas uma thread execute enquanto as outras ficam bloqueadas tornando o código *thread-safe*. Este gerenciamento se faz necessário por causa do *reference counting*, que é uma referência de quantas vezes um objeto é usado em Python, caso seja nulo, o *Garbage Collector* irá liberar esse espaço em memória, excluindo esse objeto. Se caso várias threads estiverem executando, ele poderá ser incrementado simultaneamente e assim gerar um problema de *race conditions*, incrementando de forma errônea a quantidade de vezes, podendo causar uma exclusão pelo Garbage Collector antes de realmente se fazer necessário e consequentemente causando *bugs* no código.  

![GIL_threads_packtpub](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/GIL_threads.png)

Comprova-se isso através do gráfico de SpeedUp gerado a partir de um código que foi paralelizado usando threads e processos. É possível observar que há um ganho de desempenho quando trabalhamos com processos e o mesmo não ocorre quando estamos usando threads no Python.

Para gerar o gráfico de SpeedUp, foram testados 1 mil endereços, gerenciados de acordo com a quantidade de processos ou threads que eram criados e além disso, cada teste era repetido três vezes para então fazer uma média dos valores e ter um resultado mais confiável de tempo de execução.

![SpeedUp - Threads vs Process ](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/SpeedUp.png)

Com  o objetivo de obter uma comparação de desempenho entre processadores, foi utilizado o algoritmo feito com processos  **process_FB.py**. Foram testados um Intel Core i7 de terceira geração, um i5 de segunda, um processador genérico que o Google Colab deixa à disposição de quem usa a plataforma e por último um Raspberry pi 4 que possui um ARM Cortex-A72.

![comparacao_entre_cpus](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cpus_comparison.png)

Também foi gerado um gráfico de eficiência de paralelização para o processador Intel Core i7 Quad Core, onde obteve-se **2,72 de SpeedUp** e **68% de eficiência** desta paralelização em comparação com a versão serial do algoritmo, **serial_BF_BTC.py**. Na versão paralela, com processos, temos um tempo maior para configurar o ambiente, porém na parte da execução não nota-se significativa diferença de desempenho.

![Eficiência](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/eficiencia.png)

### Profilers
Para entender melhor o fluxo de dados, optou-se por fazer uma análise do código usando o profiler **cProfile**, no entanto, este profiler não consegue obter informações de processos que foram criados. É como se ele não conseguisse rastrear o que acontece depois que eles são iniciados e somente detecta quando os processos retornam sua execução pela chamada *join( )*.

![cProfile](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cProfile.png)

Outra forma de analisar o fluxo de dados é através do gprof2dot que gera um gráfico onde as cores quentes indicam maior execução.

![gprof2dot](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/gprof2dot_output_cProfile.png)

Também foi usado o software *pyinstrument* para recolher informações sobre os processos que foram criados e infelizmente não foi possível obter informações além das que o cProfile gerou.  

![pyinstrument](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/pyinstrument.png)

Uma provável maneira de analisar os processos criados seria rodar algum software que analise todos os processos que estão executando no Sistema Operacional, provavelmente teríamos muito ruído de outros serviços, mas seria possível obter mais informações sobre essa execução. Também é possível fazer um código não paralelo, em que não são criados processos, assim é possível analisar melhor as funções que são chamadas e se o tempo é gasto na busca que é realizada ou na geração de chaves assimétricas.
Nesta análise feita do código serial com o cProfile é possível ver mais detalhes da execução do mesmo.

![cProfile_serial](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cProfile_serial.png)

## Conclusão 
Conclui-se que este algoritmo, que faz a geração de chaves assimétricas e consequentemente uma busca em uma string, é paralelizável e em um  processador Quadcore pode ter um **ganho** de mais de **3 vezes** em relação à versão não paralela, como pode ser observado no gráfico de SpeedUp. Em relação à análise do algoritmo, que envolve a parte de Profilers, não foi possível fazer uma busca mais profunda sobre o que está acontecendo no código paralelo, assim dificultando que alguns melhoramentos poderiam ser feitos.

## Comandos Utilizados
**Códigos**

    python3 serial_BF_BTC.py 1000
    python3 parallel_BF_BTC.py 1000 8

**cProfile**

    python -m cProfile -o output.stats parallel_BF_BTC.py 1000 8
    python -m pstats output.stats
    sort cumtime
    stats 30

**Gprof2ot**

    gprof2dot -f pstats output.stats | dot -Tpng -o out.png

**PyInstrument**

    pyinstrument process_BF.py 1000 8

## Referências

[Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock). Acessado em 5/08/2022

[Mastering Bitcoin, 2nd Edition by Andreas M. Antonopoulos](https://www.oreilly.com/library/view/mastering-bitcoin-2nd/9781491954379/ch04.html). Acessado em 5/08/2022
