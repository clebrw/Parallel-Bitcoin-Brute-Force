import sys
from bit import Key
from timeit import default_timer

print(f' - Starting - Bitcoin Brute Force') 
print(f'> Reading Wallets') 

wallets = open('wallets_bitcoin.txt', 'r').read()

lines = wallets.count('\n')
print(f'> {lines:,} Wallets Loaded\n')

if len(sys.argv) != 2:
        print(f' - Parameters : n_tests ') 
        exit()

iterations = int(sys.argv[1])

print('>>> Starting Brute Force <<<\n')

get_time = default_timer() # get time now

for i in range(iterations):
        pk = Key()
        if pk.address in wallets:
            with open('found.txt', 'a') as result:
                result.write(f'ADDR:{pk.address} - PK:{pk.to_wif()}\n')
            print(f'\n *** FOUND! ***\n> Added Address to found.txt\n')

print(f'> {round(iterations/(default_timer() - get_time),2)} Wallets/seg ')

print('\n>>> End Brute Force <<<')       