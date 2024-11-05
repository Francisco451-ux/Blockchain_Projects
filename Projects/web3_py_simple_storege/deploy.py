from solcx import compile_standard, install_solc, get_installed_solc_versions
import json
from web3 import Web3
import os
from dotenv import load_dotenv
from eth_utils import decode_hex

load_dotenv()

# Check installed Solc versions
print(get_installed_solc_versions())

# Install Solc version 0.6.0 if not installed
if "0.6.0" not in get_installed_solc_versions():
    install_solc("0.6.0")

with open("./SimpleStorege.sol", "r") as file:
    simple_storage_file = file.read()


# Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorege.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)


with open("compile_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorege.sol"]["SimpleStorege"]["evm"][
    "bytecode"
]["object"]

# get abi

abi = compiled_sol["contracts"]["SimpleStorege.sol"]["SimpleStorege"]["abi"]

# for connecting to ganache/sepolia

w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/efe07e35bbe145e286a49ee49d0b4b48")
)
chain_id = 58008
my_address = "0x0xaEf6C4B06836416C8ab9d92b7aD404988c1dF2E5"
# private_key = "0x0a6bc46f246a8ea62e16ba80b383eaac9553d57319b3d9077250e037253788"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latestest transaction

nonce = w3.eth.get_transaction_count(my_address)
print(nonce)


# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.to_wei(20, "gwei"),
        "gas": 2000000,
    }
)

# Sign the transaction
private_key_bytes = decode_hex(private_key)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key_bytes)
print(signed_txn)

# Send  this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract
# Contract address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return a value
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.to_wei(20, "gwei"),
        "gas": 2000000,
    }
)
# Sign the transaction with the private key
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# Send the transaction to the blockchain

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

# Wait to the Transaction to finish

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())
