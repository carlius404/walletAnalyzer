from dotenv import load_dotenv
import os
import requests
import json
from web3 import Web3

load_dotenv()
scanKey = os.getenv('BSCSCAN_KEY')


def getTxs(address):
    url=f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apiKey={scanKey}'
    res=requests.get(url)
    res=json.loads(res.text)
    res=res['result']
    return res

def getTokenTxs(address):
    url=f'https://api.bscscan.com/api?module=account&action=tokentx&address={address}&sort=asc&apikey={scanKey}'
    res=requests.get(url)
    res=json.loads(res.text)
    res=res['result']
    return res

def getLogs(txHash):
    url=f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionReceipt&txhash={txHash}&apiKey={scanKey}"
    res=requests.get(url)
    res=json.loads(res.text)
    res=res['result']['logs']
    return res

def getAbi(address):
    url=f'https://api.bscscan.com/api?module=contract&action=getsourcecode&address={address}&apikey={scanKey}'
    res=requests.get(url)
    res=json.loads(res.text)
    if len(res)>1:
        print(f"WARNING: more than one contract was returned from {address} ({len(res)})")
    res=res['result']
    return res