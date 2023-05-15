from getDataBsc import *

def swapValues(logs):
    for log in logs:
        for k in log:
            print(1)   
def getPrices(pairAddress):
    abi=getAbi(pairAddress)
    print(abi[0])
    print(abi[1])
    print(abi[2])
    txs=getTokenTxs(pairAddress)
    for tx in txs:
        logs=getLogs(tx['hash'])
        

getPrices("0xa70fC90D49e326dabF4eF63C1a77de063C5ab4d0")
