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

def getTokenTxs(address):
    url=f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&sort=asc&apikey={scanKey}'
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
