from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app import Base

class Block(Base):
    __tablename__ = "blocks"
    number = Column(Integer, primary_key=True)
    hash = Column(String, unique=True)
    parent_hash = Column(String)
    miner = Column(String)
    timestamp = Column(BigInteger)
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    transactions = relationship("Transaction", back_populates="block")

class Transaction(Base):
    __tablename__ = "transactions"
    hash = Column(String, primary_key=True)
    block_number = Column(Integer, ForeignKey("blocks.number"))
    from_address = Column(String)
    to_address = Column(String)
    value = Column(BigInteger)
    gas = Column(BigInteger)
    gas_price = Column(BigInteger)
    nonce = Column(Integer)
    status = Column(String)
    gas_used = Column(BigInteger)
    contract_address = Column(String, nullable=True)
    block = relationship("Block", back_populates="transactions")
    logs = relationship("Log", back_populates="transaction")

class Log(Base):
    __tablename__ = "logs"
    __table_args__ = (UniqueConstraint('tx_hash', 'address', 'data', name='uq_log'),)
    id = Column(Integer, primary_key=True)
    tx_hash = Column(String, ForeignKey("transactions.hash"))
    address = Column(String)
    data = Column(String)
    topic0 = Column(String)
    topic1 = Column(String, nullable=True)
    topic2 = Column(String, nullable=True)
    topic3 = Column(String, nullable=True)
    transaction = relationship("Transaction", back_populates="logs")

