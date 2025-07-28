import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from web3 import Web3

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")

# DB Setup
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Web3
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

