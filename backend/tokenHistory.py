from getDataBsc import *
from web3 import Web3
import matplotlib.pyplot as plt

def swapValues(logs):
    for log in logs:
        for k in log:
            print(1)   
def getPrices(pairAddress):
    txs=getTokenTxs(pairAddress)
    buyPrices=[]
    sellPrices=[]
    doneTxs=[]
    for tx in txs:
        if tx['hash'] not in doneTxs:
            doneTxs.append(tx['hash'])
            print(len(buyPrices))
            buy,sell=getPrice(pairAddress,tx['hash'])
            buyPrices+=buy
            sellPrices+=sell
            if len(buyPrices)>100:
                plt.plot(buyPrices)
                plt.show()
getPrices("0xb7365f296b71094B57662bd357a2cd29282Bb133")
