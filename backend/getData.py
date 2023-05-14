from dotenv import load_dotenv
import os
import requests
import json
from web3 import Web3

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
    fromAddress=res['from']
    
    if 'operations' not in res:
        return
    operations=res['operations']
    
    for operation in operations:
        if operation['type']=='transfer':
            color='\u001b[0m'
            
            if fromAddress==operation['from']:
                color=colors.FAIL
            if fromAddress==operation['to']:
                color=colors.GREEN
            print(color+operation['value']+" "+operation['tokenInfo']['symbol'])

def getTrades(address):
    txs=getTxs(address)
    for tx in txs:
        print(colors.BLUE+tx['hash'])
        logs=getValues(tx['hash'])
        print()

    
#0xF9a5844AC0b81Bc45f448F864D484E0EF5927D5f
getTrades("0xF9a5844AC0b81Bc45f448F864D484E0EF5927D5f")
