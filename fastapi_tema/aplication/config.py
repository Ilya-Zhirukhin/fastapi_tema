# from web3 import Web3

# # URL для подключения к RPC-серверу сети Polygon
# POLYGON_RPC_URL = "https://polygon-rpc.com"

# TOKEN_ADDRESS = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"

# # ABI для взаимодействия с ERC20 контрактом
# ERC20_ABI = [
#     # Сокращенный ABI, содержащий только используемые методы
#     {
#         "constant": True,
#         "inputs": [{"name": "_owner", "type": "address"}],
#         "name": "balanceOf",
#         "outputs": [{"name": "balance", "type": "uint256"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "decimals",
#         "outputs": [{"name": "", "type": "uint8"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "symbol",
#         "outputs": [{"name": "", "type": "string"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "name",
#         "outputs": [{"name": "", "type": "string"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "totalSupply",
#         "outputs": [{"name": "", "type": "uint256"}],
#         "type": "function"
#     }
# ]

# web3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
# checksum_address = Web3.to_checksum_address(TOKEN_ADDRESS) 
# token_contract = web3.eth.contract(address=checksum_address, abi=ERC20_ABI)

