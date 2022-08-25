from bit import Key
from timeit import default_timer 
from multiprocessing import cpu_count, Process
import sys
wallets = []

def BF_random(iterations):
    for _ in range(iterations):
        pk = Key()
        if pk.address in wallets:
            with open('found.txt', 'a') as result:
                result.write(f'ADDR:{pk.address} - PK:{pk.to_wif()}\n')
            print(f'\n *** Added address to found.txt ***')

if __name__ == '__main__':
   
    if len(sys.argv) != 3:
        print(f' - Parameters : n_tests, n_jobs ') 
        exit()

    print(f'> Starting - Bitcoin Brute Force') 
    print(f'> CPU count: {cpu_count()}')
    
    iterations = int(sys.argv[1])
    n_jobs = int(sys.argv[2])
    
    print(f'> Reading Wallets') 
    wallets = open('wallets_bitcoin.txt', 'r').read()
    lines = wallets.count('\n')
    print(f'> {lines:,} Wallets Loaded\n')
    
    print('>>> Starting Brute Force <<<')
    cpu_iteration = round(iterations/n_jobs)
    
    get_time = default_timer() # get time now
    process = [Process(target=BF_random, args=(cpu_iteration,)) for _ in range(n_jobs)] 
     
    for p in process:
        p.start()
    for p in process:
        p.join()
    
    print(f'> {round(iterations/(default_timer() - get_time),2)} Wallets/seg ')
    print('\n>>> End Brute Force <<<')       