from dotenv import load_dotenv
load_dotenv()
from web3 import Web3
from pymongo import MongoClient
import json
from time import time
from datetime import datetime
import sys, os
from pprint import pprint
lib_dir = os.getenv('lib_dir')
if not lib_dir:
    sys.exit('no lib_dir in .env')
sys.path.append(os.getenv('lib_dir'))
from josienlib import db
import gate_api
from gate_api.exceptions import ApiException, GateApiException

db = db()

def get_omi_usdt():
    configuration = gate_api.Configuration(host="https://api.gateio.ws/api/v4")
    api_client = gate_api.ApiClient(configuration)
    api_instance = gate_api.SpotApi(api_client)
    currency_pair = 'OMI_USDT'

    try:
        api_response = api_instance.list_tickers(currency_pair=currency_pair)
        return float(api_response[0].last)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_tickers: %s\n" % e)

    return False


def update_db():
    w3 = Web3(Web3.HTTPProvider('https://rpc.gochain.io/'))
    #pprint(w3.isConnected())
    
    reserve_address = '0xd9494D749eD554B2D2faAB1a8e20d2b566410F00'
    vault_address = '0x17656848E63cb846D93E629C710f6B0cc30A89dc'
    burn_address = '0xbBDA162f1E3EC2D4D9D99cafd0c14B03EC4E78d3'
    contract_address = '0x5347FDeA6AA4d7770B31734408Da6d34a8a07BdF'
    
    with open('/prod/apps/josien.net/app/abi') as f:
      abi = json.load(f)
    
    contract = w3.eth.contract(contract_address, abi=abi)
    
    reserve_balance = contract.functions.balanceOf(reserve_address).call()
    reserve = w3.fromWei(reserve_balance, 'ether')
    
    vault_balance = contract.functions.balanceOf(vault_address).call()
    vault = w3.fromWei(vault_balance, 'ether')
    
    burn_balance = contract.functions.balanceOf(burn_address).call()
    burn = w3.fromWei(burn_balance, 'ether')

    t = round(time() * 1000)
    
    reserve_d = {} 
    reserve_d['x'] = t
    reserve_d['y'] = round(reserve)
    
    burn_d = {}
    burn_d['x'] = t
    burn_d['y'] = round(burn)
    
    vault_d = {}
    vault_d['x'] = t
    vault_d['y'] = round(vault)
    
    omi_usdt_d = {}
    omi_usdt_d['x'] = t
    omi_usdt_d['y'] = get_omi_usdt() 
    
    if not db.list_collection_names():
        db.omi_wallet.update_one( { }, { "$set": { "reserve": [],
                                                   "vault": [],
                                                   "omiusdt": [],
                                                   "burn": [] } }, upsert=True )
    
    
    db.omi_wallet.update_one( { }, { "$push": { 'reserve': { "$each": [ reserve_d ] },
                                                'vault': { "$each": [ vault_d ] },
                                                'burn': { "$each": [ burn_d ] },
                                                'omiusdt': { "$each": [ omi_usdt_d ] } } } )


def fix_db():
    docs = db.omi_wallet.find()
    for doc in docs:
        for i in doc['omiusdt']:
            if not i['y']:
                u = db.omi_wallet.update_one({}, { "$pull": { "omiusdt": { "x": i['x'] } }})
                pprint(u)
                pprint(i)

def dev():
    w3 = Web3(Web3.HTTPProvider('https://rpc.gochain.io/'))
    #pprint(w3.isConnected())

    reserve_address = '0xd9494D749eD554B2D2faAB1a8e20d2b566410F00'
    vault_address = '0x17656848E63cb846D93E629C710f6B0cc30A89dc'
    burn_address = '0xbBDA162f1E3EC2D4D9D99cafd0c14B03EC4E78d3'
    contract_address = '0x5347FDeA6AA4d7770B31734408Da6d34a8a07BdF'

    with open('/prod/apps/josien.net/app/abi') as f:
      abi = json.load(f)

    contract = w3.eth.contract(contract_address, abi=abi)

    #pprint(vars(contract))
    #pprint(dir(contract))
    #pprint(contract.web3.eth.getBlock('latest'))
    #pprint(vars(contract.functions))
    #pprint(vars(contract.functions.symbol))
    #pprint(contract.functions.events)
    #pprint(dict(contract.web3.eth.getBlock('latest')))
    pprint(contract.web3.eth.block_number)
    pprint(contract.web3.eth.get_block_transaction_count(19333793))
    #pprint(contract.web3.eth.getTransactionByBlock(19332868))
    # >>> web3.eth.get_transaction_by_block(46147, 0)

    #contract.events.Transfer(
    #  {fromBlock: 0, toBlock: 'latest'},
    #  (err, data) => !err && acc.push(data)
    #)



if __name__ == '__main__':
    update_db()
    fix_db()
    #dev()
