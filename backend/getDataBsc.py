from dotenv import load_dotenv
import os
import requests
import json
from web3 import Web3

load_dotenv()
scanKey = os.getenv('BSCSCAN_KEY')
web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
stableCoins=["0x55d398326f99059ff775485246999027b3197955","0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c","0xe9e7cea3dedca5984780bafc599bd69add087d56"]
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
    res=res['result']
    if len(res)>1:
        print(f"WARNING: more than one contract was returned from {address} ({len(res)})")
    return res[0]['ABI']

def getPrice(address,txHash):
    logs=web3.eth.get_transaction_receipt(txHash).logs
    abi=getAbi(address)
    contract=web3.eth.contract(address, abi=abi)

    #recognize which one of the two tokens is the stable coin, 
    #so we can determine the price of the token compared to the stable coin

    token0=contract.functions.token0().call()
    token1=contract.functions.token1().call()
    
    if token0.lower() in stableCoins:
        stable=0
        token=1
    if token1.lower() in stableCoins:
        stable=1
        token=0
    
    #create a dict that maps all the events signature to the name of the event

    hexToName={}
    for abi in contract.abi:
        if abi["type"] == "event":
            name = abi["name"]
            inputs = [param["type"] for param in abi["inputs"]]
            inputs = ",".join(inputs)
            
            signatureText=f"{name}({inputs})"
            signatureHex=web3.toHex(web3.keccak(text=signatureText))
            hexToName[signatureHex[:10]]=name
    buyPrices=[]
    sellPrices=[]
    for log in logs:
        if log['address'].lower()==address.lower():
            topic0=log['topics'][0].hex()
            topic0=topic0[:10]
            if topic0=="0xd78ad95f": #if the topic0 has the signature of the swap event
                    decodedLogs=contract.events[hexToName[topic0]]().processLog(log)
                    stableIn=decodedLogs['args'][f'amount{stable}In']
                    stableOut=decodedLogs['args'][f'amount{stable}Out']
                    tokenIn=decodedLogs['args'][f'amount{token}In']
                    tokenOut=decodedLogs['args'][f'amount{token}Out']
                    if stableIn!=0:
                        buyPrices.append(stableIn/tokenOut)
                    else:
                        sellPrices.append(stableOut/tokenIn)
    return buyPrices,sellPrices

                    