from getDataBsc import *
from web3 import Web3
import matplotlib.pyplot as plt
import time

def getPairs(fromBlock, toBlock): 

    pancakeFactory2="0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
    contract,hexToName=getContract(pancakeFactory2)
    print(hexToName)
    logs=contract.events.PairCreated.getLogs(fromBlock=fromBlock, toBlock=toBlock)
    pairs=[]
    for log in logs:
        pairs.append(log['pair'])

def getAddLiquidity(fromBlock, toBlock):
    print(12)
    pancakeFactory2="0x10ED43C718714eb63d5aA57B78B54704E256024E"
    contract,hexToName=getContract(pancakeFactory2)
    print(contract.events)
    logs=contract.functions.addLiquidity.getLogs(fromBlock=fromBlock, toBlock=toBlock)
    pairs=[]
    for log in logs:
        pairs.append(log['pair'])
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
getAddLiquidity(-10, 28448421+10)