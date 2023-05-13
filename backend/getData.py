from dotenv import load_dotenv
import os
import requests
import json
from web3 import Web3



load_dotenv()
scanKey = os.getenv('ETHERSCAN_KEY')
plorerKey = os.getenv('ETHPLORER_KEY')
def getTxs(address):
    url=f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apiKey={scanKey}'
    res=requests.get(url)
    res=json.loads(res.text)
    res=res['result']
    return res

def getLogs(txHash):
    url=f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={txHash}&apiKey={scanKey}"
    res=requests.get(url)
    res=json.loads(res.text)
    res=res['result']['logs']
    return res

def getValues(txHash):
    url=f'https://api.ethplorer.io/getTxInfo/{txHash}?apiKey={plorerKey}'
    res=requests.get(url)
    res=json.loads(res.text)
    print(res)
    operations=res['operations']

    for operation in operations:
        print(operation)

def getTrades(address):
    txs=getTxs(address)
    for tx in txs:
        logs=getValues(tx)

    
#0xF9a5844AC0b81Bc45f448F864D484E0EF5927D5f
getValues("0xc1005cbf96fc4415f216eadf4551cb3552abbfa732400d001dfa0b7056c1b7d7")