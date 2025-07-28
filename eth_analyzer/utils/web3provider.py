import os
from web3 import Web3
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Read Web3 provider URL from .env
provider_uri = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
web3 = Web3(Web3.HTTPProvider(provider_uri))

# Check connection
if not web3.is_connected():
    raise ConnectionError(f"Failed to connect to Ethereum node at {provider_uri}")

