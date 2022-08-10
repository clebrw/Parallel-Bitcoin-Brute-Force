out_file = open('wallets_bitcoin.txt','w')

with open('Bitcoin_addresses_LATEST.txt') as f:
    for line in f.readlines():
        if line[0] == '1':
            out_file.write(line)

print(f'\nFIM')