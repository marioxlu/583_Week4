from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
############################
#Connect to an Ethereum node
api_url = "https://eth-mainnet.g.alchemy.com/v2/af1I02w3ZtSVoGgFEG9UFCMBGCNVHasF" #YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)

contract_address = web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('abi.json', 'r') as f:
    abi = json.load(f) 



# Instantiate the contract object
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
    assert isinstance(apeID,int), f"{apeID} is not an int"
    assert 1 <= apeID, f"{apeID} must be at least 1"

    data = {'owner': "", 'image': "", 'eyes': "" }
    
    # Fetch the owner of the ape by token ID
    try:
        owner = contract.functions.ownerOf(apeID).call()
        data['owner'] = owner
    except Exception as e:
        print(f"Error fetching owner for Ape ID {apeID}: {e}")
        return data

    # Fetch the tokenURI (metadata location)
    try:
        token_uri = contract.functions.tokenURI(apeID).call()
        # Make sure the URI is correct for IPFS retrieval
        if token_uri.startswith("ipfs://"):
            token_uri = token_uri.replace("ipfs://", "https://ipfs.io/ipfs/")
        # Fetch metadata from IPFS
        metadata = requests.get(token_uri).json()
        data['image'] = metadata['image']
        data['eyes'] = metadata['attributes'][0]['value']  # Assuming 'eyes' is the first attribute
    except Exception as e:
        print(f"Error fetching metadata for Ape ID {apeID}: {e}")

    assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
    assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
    return data

