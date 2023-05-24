from getDataBsc import *
from web3 import Web3
import matplotlib.pyplot as plt
import time

def getPairs(fromBlock, toBlock): 
    pancakeFactory2="0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
    contract,hexToName=getContract(pancakeFactory2)
    logs=contract.events.PairCreated.getLogs(fromBlock=fromBlock, toBlock=toBlock)
    pairs=[]
    for log in logs:
        pairs.append(log['args']['pair'])
    return pairs

def getPooled(pairAddress):
    contract,hexToName=getContract(pairAddress)
    stable,token=recognizeStable(contract)
    txs=getTokenTxs(pairAddress)

    fromBlock=int(txs[0]['blockNumber'])
    logs=contract.events.Mint.getLogs(fromBlock=fromBlock-20, toBlock=fromBlock+20)
    for log in logs:
        print(log)
        amountStable=log['args'][f'amount{stable}']
        amountToken=log['args'][f'amount{token}']
        print(amountStable,amountToken)

def getPrices(pairAddress):
    contract,hexToName=getContract(pairAddress)
    stable,token=recognizeStable(contract)
    txs=getTokenTxs(pairAddress)

    fromBlock=int(txs[0]['blockNumber'])
    lastTxBlock=int(txs[-1]['blockNumber'])
    toBlock=fromBlock

    buyPrices=[]
    while fromBlock<lastTxBlock:
        if fromBlock+2000<=lastTxBlock:
            toBlock+=2000
        else:
            toBlock+=(lastTxBlock-toBlock)
        print(toBlock/lastTxBlock)
        logs=contract.events.Swap.getLogs(fromBlock=fromBlock, toBlock=toBlock)


        for log in logs:
            stableIn=log['args'][f'amount{stable}In']
            stableOut=log['args'][f'amount{stable}Out']
            tokenIn=log['args'][f'amount{token}In']
            tokenOut=log['args'][f'amount{token}Out']
            if stableIn!=0:
                buyPrices.append(stableIn/tokenOut)
        
        fromBlock=toBlock
    print(buyPrices[-1])
    plt.plot(buyPrices)
    plt.show()
#getPrices("0xeA8DE07b2129870cB382E48de95423bb66A616ec")
#getAddLiquidity(28448421-10, 28448421+10)
pairs=getPairs(28483284-50,28483284+50)
for pair in pairs:
    print(pair)
    getPooled(pair)