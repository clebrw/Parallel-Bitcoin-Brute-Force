# Brute Force in Bitcoin Wallets

## Abstract

Assuming that you are curious and intend to take the real proof of how difficult it is to find an address with a non-zero balance, an algorithm was developed that generates a new bitcoin address and tests if it is in a list of bitcoin addresses with non-zero balance. If so, which is rare, the address and your private key will be saved in a text file.

Taking advantage of the parallelization knowledge acquired during the Parallel Programming Course (ELC139), two algorithms were developed in Python, one using Processes and the other Threads for comparison purposes, whose SpeedUp and Profilers data will be shown later.

## Introduction

The generation of Bitcoin wallets is done through asymmetric cryptography, where from a private key, a public key is generated and from it, the address of the wallet that is used to receive coins. Due to the Elliptic Curves and Hash algorithm used in key generation encryption, it is only possible to make a one-way path as seen in the image below, that is, from the generation of the private key to the wallet address.

![Geração de chaves de Bitcoin - Fonte: Oreilly](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/private-public-address-oreilly.png)

In terms of security, we have 256 bits of possibilities for generating wallets, this represents a number of 78 digits, that is, it is just not greater than the number of atoms in the observable universe.

|Object |Numbers |
|---------------------|---------------------------|
| Galaxies            | 10<sup>11</sup> à 10<sup>12</sup> galaxies |
| Starts            | 10<sup>22</sup> à 10<sup>24</sup> stars |
| A person          | 7*10<sup>27</sup> atoms |
| World population   | 5*10<sup>37</sup> atoms |
| Bitcoin Addresses  | 1,15*10<sup>77</sup> addresses |
| Observable Universe | 10<sup>82</sup> atoms |
 
Based on this data, it is possible to note that it is quite unlikely to generate the same Bitcoin address twice if using secure randomization methods in generating the keys. Therefore, **it is practically impossible to get the private key of some address with a non-zero balance using brute force**, as it would take thousands of years to find one with the available hardware that we have today.

## Development
The generation of keys is done using the *Key()* function of the **bit** library that generates addresses of type *Pay for Public Key Hash* **(P2PKH)**. In this case, we use *Key.from_int()* so that the performance test is as controlled as possible, so all tests will generate the same addresses and test them.

    def test_wallet(start, end):
        for i in range(start, end+1):
            pk = Key.from_int(i)
            if pk.address in wallets:
                with open('found.txt', 'a') as result:
                    result.write(f'ADDR:{pk.address} - PK:{pk.to_wif()}\n')
                print(f'\n *** Added address to found.txt ***')

One of the ways to find out if a generated wallet has a balance is to check it online on some blockchain explorer websites, but this takes a few seconds and most of the time a limit on IP queries is imposed. Another much faster method that can be used is to download a text file with the wallets that have a non-zero balance, so that all verification is local and does not require online consultations to work. This second approach was used in this work, where more than 42 million addresses of the most varied types were downloaded from the website (http://addresses.loyce.club/), and the text file was extracted * Bitcoin_addresses_LATEST.txt* in the same directory as the Python files. As the *Key()* function works with the P2PKH type, we will filter only these types of addresses to increase the search efficiency. With the version of the date that this report was written (07/2022), there are 1.6GB of addresses and after applying the filter, a file of approximately 800MB was generated.

In the *test_wallet()* function, after generating a wallet, we check if the generated address exists within the wallet file with a non-null balance, if it exists, the address and the private key are recorded in the *found.txt* file, otherwise the next address is tested.

In the repository you can find **serial_BF_BTC.py** which is the non-parallel version of the program and **parallel_BF_BTC.py** which is the parallel version using Process, both generate random keys and are not as controlled as the versions ** process_BF.py** and **thread_BF.py** that were used to do the SpeedUp tests. In addition, we have **select_P2PKH_text.py** that generates a text file with only P2PKH addresses, **wallets_bitcoin.txt** from the file that has the addresses of wallets with updated balances.

### Parallelism
As this algorithm involves more basic operations, such as a search on a string that contains the wallets separated by the characters *\n*, it was not difficult to parallelize its operations.
At first, the *Process()* function from the *multiprocessing* library was used, which had the objective of parallelizing the address tests. In a second moment, the *Thread( )* function of the *threading* library was tested, which did not work as expected because of a block that exists in the Python language when it comes to the thread part.

### Differences between Processes and Threads

![process vs threads_javatpoint](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/process-vs-thread_javatpoint.png)

In Python, when we create a **Process**, a processor core can be assigned to it, so if we have a Quadcore processor, we can create four processes and the performance will be almost four times that of a core. It won't be exactly four times faster, because the system manages the processes and between them we have the operating system processes that are also demanding CPU.

When we are working with **Threads**, we can create several within a process, but they suffer a block, where only one thread is executed at a time. This lock is managed by the Global Interpreter Lock (**GIL**) that works like a *mutex*, causing only one thread to execute while the others are blocked, making the code *thread-safe*. This management is necessary because of the *reference counting*, which is a reference of how many times an object is used in Python, if it is null, the *Garbage Collector* will free this space in memory, excluding this object. If several threads are running, it can be incremented simultaneously and thus generate a *race conditions* problem, erroneously incrementing the number of times, which can cause a deletion by the Garbage Collector before it is really necessary and consequently causing *bugs * in the code.  

![GIL_threads_packtpub](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/GIL_threads.png)

This is proved through the SpeedUp graph generated from a code that was parallelized using threads and processes. It is possible to observe that there is a performance gain when working with processes and the same does not occur when we are using threads in Python.

To generate the SpeedUp graph, 1,000 addresses were tested in quad core processor, managed according to the number of processes or threads that were created and, in addition, each test was repeated three times to then average the values and have a more reliable result of runtime.

![SpeedUp - Threads vs Process ](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/SpeedUp.png)

In order to obtain a performance comparison between processors, the algorithm made with **process_FB.py** processes was used. We tested a third-generation Intel Core i7, a second-generation Intel Core i5, a generic processor that Google Colab makes available to those who use the platform and, finally, a Raspberry pi 4 that has an ARM Cortex-A72.

![comparacao_entre_cpus](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cpus_comparison.png)

A parallelization efficiency graph was also generated for the Intel Core i7 Quad Core processor, where **2.72 SpeedUp** and **68% efficiency** were obtained from this parallelization compared to the serial version of the algorithm. , **serial_BF_BTC.py**. In the parallel version, with processes, we have a longer time to configure the environment, but in the execution part there is no significant difference in performance.

![Eficiência](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/eficiencia.png)

### Profilers
To better understand the data flow, it was decided to analyze the code using the **cProfile** profiler, however, this profiler cannot obtain information from processes that were created. It's as if it can't track what happens after they're started and only detects when processes resume execution by calling *join( )*.

![cProfile](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cProfile.png)

Another way to analyze the data flow is through gprof2dot which generates a graph where warm colors indicate greater execution.

![gprof2dot](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/gprof2dot_output_cProfile.png)

The *pyinstrument* software was also used to collect information about the processes that were created and unfortunately it was not possible to obtain information beyond what the cProfile generated. 

![pyinstrument](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/pyinstrument.png)

A probable way to analyze the processes created would be to run some software that analyzes all the processes that are running in the Operating System, we would probably have a lot of noise from other services, but it would be possible to get more information about this execution. It is also possible to make non-parallel code, in which processes are not created, so it is possible to better analyze the functions that are called and if the time is spent in the search that is performed or in the generation of asymmetric keys.
In this analysis made of the serial code with cProfile it is possible to see more details of its execution.

![cProfile_serial](https://raw.githubusercontent.com/clebrw/Parallel-Bitcoin-Brute-Force/main/img/cProfile_serial.png)

## Conclusion 
It is concluded that this algorithm, which generates asymmetric keys and consequently a search in a string, is parallelizable and in a Quadcore processor it can have a **gain** of more than **3 times** in relation to the previous non-parallel version, as can be seen in the SpeedUp graph. Regarding the analysis of the algorithm, which involves the Profilers part, it was not possible to do a deeper search on what is happening in the parallel code, thus making it difficult for some improvements to be made.

## Commands Used
**Codes**

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

## References

[Mastering Bitcoin, 2nd Edition by Andreas M. Antonopoulos](https://www.oreilly.com/library/view/mastering-bitcoin-2nd/9781491954379/ch04.html). Acessed in 08/2022

[Process Vs. Thread | Difference Between Process and Thread](https://www.javatpoint.com/process-vs-thread). Acessed in 08/2022

[Python Global Interpreter Lock Tutorial](https://www.datacamp.com/tutorial/python-global-interpreter-lock). Acessed in 08/2022

[Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock). Acessed in 08/2022
