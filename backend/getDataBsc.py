from dotenv import load_dotenv
import os
import requests
import json
from web3 import Web3

load_dotenv()
scanKey = os.getenv('BSCSCAN_KEY')
web3 = Web3(Web3.HTTPProvider('https://bscrpc.com'))
stableCoins=["0x55d398326f99059ff775485246999027b3197955","0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c","0xe9e7cea3dedca5984780bafc599bd69add087d56"]

def getTxs(address,fromBlock,ToBlock):
    txs = web3.eth.getTransactionsByAddress(address=address,startBlock=fromBlock,endBlock=ToBlock)
    return txs


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
    res=res['result']
    if len(res)>1:
        print(f"WARNING: more than one contract was returned from {address} ({len(res)})")
    return res[0]['ABI']

def getContract(address):
    abi=getAbi(address)
    contract=web3.eth.contract(address, abi=abi)
    hexToName={}
    for abi in contract.abi:
        if abi["type"] == "event":
            name = abi["name"]
            inputs = [param["type"] for param in abi["inputs"]]
            inputs = ",".join(inputs)
            
            signatureText=f"{name}({inputs})"
            signatureHex=web3.toHex(web3.keccak(text=signatureText))
            hexToName[signatureHex[:10]]=name
    return contract, hexToName

def recognizeStable(contract):
    token0=contract.functions.token0().call()
    token1=contract.functions.token1().call()
    
    if token0.lower() in stableCoins:
        stable=0
        token=1
    if token1.lower() in stableCoins:
        stable=1
        token=0
    return stable,token
        