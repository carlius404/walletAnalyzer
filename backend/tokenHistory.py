from getDataBsc import *
from web3 import Web3
import matplotlib.pyplot as plt
import time
def swapValues(logs):
    for log in logs:
        for k in log:
            print(1)   
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
    #txs=getTokenTxs(pairAddress)
    #buyPrices=[]
    #sellPrices=[]
    #swapData=[]
    #doneTxs=[]
    #lenn=len(txs)
    #n=0
    #for tx in txs:
    #    n+=1
    #    print(n/lenn)
    #    if tx['hash'] not in doneTxs:
    #        start=time.time()
    #        doneTxs.append(tx['hash'])
    #        data=getSwapLogs(tx['hash'],pairAddress)
    #        swapData+=data
    #        if len(data)>0:
    #            
    #            decodedLogs=contract.events[hexToName["0xd78ad95f"]]().processLog(data[0])
    #        print(time.time()-start)
getPrices("0xeA8DE07b2129870cB382E48de95423bb66A616ec")
