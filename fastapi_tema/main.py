# """ main app """

# from fastapi import FastAPI
# from pydantic import BaseModel
# from .settings import settings


# app = FastAPI()

# class Status(BaseModel):
#     """_summary_

#     Args:
#         BaseModel (_type_): _description_
#     """
#     status:str = "ok"
    
# @app.get(settings.main_url)
# async def status():
#     """_summary_

#     Returns:
#         _type_: _description_
#     """
#     return Status()


""" main app """
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
# from .config import web3, token_contract
# import requests
# from dotenv import load_dotenv
# import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .settings import settings

# load_dotenv()

app = FastAPI()

# POLYGONSCAN_API_KEY = os.getenv("POLYGONSCAN_API_KEY")
# POLYGONSCAN_API_URL = "https://api.polygonscan.com/api"

class AddressRequest(BaseModel):
    addresses: List[str]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get(settings.main_url, response_class=FileResponse)
async def read_root():
    return "static/index.html"


















# @app.get("/get_balance")
# async def get_balance(address: str = Query(..., description="The Ethereum address to get the balance for")):
#     try:
#         checksum_address = web3.to_checksum_address(address)
#         balance = token_contract.functions.balanceOf(checksum_address).call()
#         decimals = token_contract.functions.decimals().call()
#         formatted_balance = balance / (10 ** decimals)
#         return {"balance": formatted_balance}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/get_balance_batch")
# async def get_balance_batch(request: AddressRequest):
#     try:
#         balances = []
#         decimals = token_contract.functions.decimals().call()
#         for address in request.addresses:
#             checksum_address = web3.to_checksum_address(address)
#             balance = token_contract.functions.balanceOf(checksum_address).call()
#             formatted_balance = balance / (10 ** decimals)
#             balances.append(formatted_balance)
#         return {"balances": balances}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/get_token_info")
# async def get_token_info():
#     try:
#         name = token_contract.functions.name().call()
#         symbol = token_contract.functions.symbol().call()
#         total_supply = token_contract.functions.totalSupply().call()
#         decimals = token_contract.functions.decimals().call()
#         formatted_total_supply = total_supply / (10 ** decimals)
#         return {
#             "name": name,
#             "symbol": symbol,
#             "totalSupply": formatted_total_supply
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/get_top")
# async def get_top(n: int):
#     try:
#         params = {
#             "module": "account",
#             "action": "tokentx",
#             "contractaddress": "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0",
#             "sort": "desc",
#             "apikey": POLYGONSCAN_API_KEY
#         }
#         response = requests.get(POLYGONSCAN_API_URL, params=params)
#         data = response.json()

#         if data["status"] != "1":
#             raise HTTPException(status_code=500, detail="Error fetching data from Polygonscan")

#         transactions = data["result"]
#         balances = {}

#         for tx in transactions:
#             to_address = tx["to"]
#             value = int(tx["value"])

#             if to_address not in balances:
#                 balances[to_address] = value
#             else:
#                 balances[to_address] += value

#         sorted_addresses = sorted(balances.items(), key=lambda item: item[1], reverse=True)
#         top_addresses = sorted_addresses[:n]

#         decimals = token_contract.functions.decimals().call()
#         top_addresses = [(addr, balance / (10 ** decimals)) for addr, balance in top_addresses]

#         return {"top_addresses": top_addresses}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/get_top_with_transactions")
# async def get_top_with_transactions(n: int):
#     try:
#         params = {
#             "module": "account",
#             "action": "tokentx",
#             "contractaddress": "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0",
#             "sort": "desc",
#             "apikey": POLYGONSCAN_API_KEY
#         }
#         response = requests.get(POLYGONSCAN_API_URL, params=params)
#         data = response.json()

#         if data["status"] != "1":
#             raise HTTPException(status_code=500, detail="Error fetching data from Polygonscan")

#         transactions = data["result"]
#         balances = {}
#         last_transactions = {}

#         for tx in transactions:
#             to_address = tx["to"]
#             value = int(tx["value"])
#             timestamp = int(tx["timeStamp"])

#             if to_address not in balances:
#                 balances[to_address] = value
#                 last_transactions[to_address] = timestamp
#             else:
#                 balances[to_address] += value
#                 if timestamp > last_transactions[to_address]:
#                     last_transactions[to_address] = timestamp

#         sorted_addresses = sorted(balances.items(), key=lambda item: item[1], reverse=True)
#         top_addresses = sorted_addresses[:n]

#         decimals = token_contract.functions.decimals().call()
#         top_addresses_with_tx = [(addr, balance / (10 ** decimals), last_transactions[addr]) for addr, balance in top_addresses]

#         return {"top_addresses_with_transactions": top_addresses_with_tx}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
