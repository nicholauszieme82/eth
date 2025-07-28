from datetime import datetime, timezone
from utils.web3provider import web3
from utils.formatter import clean_hex
from utils.signatures import (
    load_signatures,
    decode_function_signature,
)
from core.logs import process_logs

import os

# Load function signatures once
FUNCTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "functions.txt")
function_signatures = load_signatures(FUNCTIONS_FILE)

def process_transfer(tx):
    print(f"  [TRANSFER] From: {tx['from']} -> To: {tx['to']}, Value: {web3.from_wei(tx['value'], 'ether')} ETH")

def process_deployment(tx, receipt):
    print(f"  [DEPLOYMENT] From: {tx['from']} -> New Contract: {receipt.contractAddress}")

def process_contract_call(tx):
    print(f"  [CALL] From: {tx['from']} -> To: {tx['to']} | Input Length: {len(tx['input'])} chars")

def process_empty_call(tx):
    print(f"  [EMPTY CALL] From: {tx['from']} -> To: {tx['to']} | No Input | No Value")

def get_method_name(input_data):
    if not input_data or len(input_data) < 10:
        return "Unknown Method"
    selector = input_data[2:10].lower()
    return function_signatures.get(selector, f"0x{selector}")

def process_transaction(tx_hash):
    tx = web3.eth.get_transaction(tx_hash)
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    block = web3.eth.get_block(tx.blockNumber)

    status_str = "Success" if receipt.status == 1 else "Failed"
    confirmations = web3.eth.block_number - tx.blockNumber + 1
    ago_seconds = int(datetime.now(timezone.utc).timestamp() - block.timestamp)

    gas_used = receipt.gasUsed
    gas_limit = tx.gas
    gas_pct = (gas_used / gas_limit) * 100 if gas_limit else 0

    gas_price = getattr(receipt, "effectiveGasPrice", tx.gasPrice)
    txn_fee = gas_used * gas_price

    print(f"[tx] Hash: {tx.hash.hex()}")
    print(f"     Status: {status_str}")
    print(f"     Block Number: {tx.blockNumber} (Confirmations: {confirmations})")
    print(f"     Timestamp (ago): {ago_seconds} seconds")
    print(f"     From: {tx['from']}")
    print(f"     To: {tx.to}")
    print(f"     Value: {web3.from_wei(tx.value, 'ether')} ETH")
    print(f"     Txn Fee: {web3.from_wei(txn_fee, 'ether')} ETH")
    print(f"     Gas Price (wei): {gas_price}")
    print(f"     Gas Limit: {gas_limit}")
    print(f"     Gas Used: {gas_used} ({gas_pct:.2f}%)")
    print(f"     Nonce: {tx.nonce}")
    print(f"     Position in Block: {receipt.transactionIndex}")
    print(f"Input Data: {clean_hex(tx.input)}")

    if tx.input and tx.input != "0x":
        # Ensure tx.input is hex string for decode_function_signature
        input_hex = tx.input.hex() if isinstance(tx.input, bytes) else tx.input
        if not input_hex.startswith("0x"):
            input_hex = "0x" + input_hex
        method_name = decode_function_signature(input_hex, function_signatures)
        print(f"Method: {method_name}")

    if isinstance(tx.input, bytes):
        tx_input_str = tx.input.hex()
    else:
        tx_input_str = tx.input

    if tx.to is None:
        process_deployment(tx, receipt)
    elif (tx_input_str == "0x" or tx_input_str == "") and tx.value > 0:
        process_transfer(tx)
    elif (tx_input_str == "0x" or tx_input_str == "") and tx.value == 0:
        process_empty_call(tx)
    else:
        process_contract_call(tx)

    process_logs(receipt)

