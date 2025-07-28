import os
import sys
from dotenv import load_dotenv

from utils.web3provider import web3
from core.block import process_block
from core.transaction import process_transaction

# Load .env variables
load_dotenv()

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <block_number>")
        return

    block_number = int(sys.argv[1])

    # Fetch block with full transactions
    block = web3.eth.get_block(block_number, full_transactions=True)

    # Process block summary
    process_block(block)

    # Process each transaction in the block
    for tx in block.transactions:
        process_transaction(tx.hash)

if __name__ == "__main__":
    main()

