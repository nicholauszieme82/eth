from app import SessionLocal
from app.models import Block, Transaction, Log
from sqlalchemy.orm import joinedload

def get_block_by_number(number):
    with SessionLocal() as session:
        return session.query(Block).options(joinedload(Block.transactions)).filter_by(number=number).first()

def get_transaction_by_hash(tx_hash):
    with SessionLocal() as session:
        return session.query(Transaction).options(joinedload(Transaction.logs)).filter_by(hash=tx_hash).first()

def get_transactions_by_address(address, limit=10):
    with SessionLocal() as session:
        return session.query(Transaction).filter(
            (Transaction.from_address == address) | (Transaction.to_address == address)
        ).order_by(Transaction.block_number.desc()).limit(limit).all()

def get_logs_by_contract(address, limit=10):
    with SessionLocal() as session:
        return session.query(Log).filter_by(address=address).order_by(Log.id.desc()).limit(limit).all()

def get_latest_blocks(limit=10):
    with SessionLocal() as session:
        return session.query(Block).order_by(Block.number.desc()).limit(limit).all()
def get_block_by_hash(block_hash):
    with SessionLocal() as session:
        return session.query(Block).filter_by(hash=block_hash).first()

def get_transactions_in_block(block_number):
    with SessionLocal() as session:
        return session.query(Transaction).filter_by(block_number=block_number).all()

def get_blocks_in_range(start, end):
    with SessionLocal() as session:
        return session.query(Block).filter(Block.number >= start, Block.number <= end).order_by(Block.number).all()

def get_logs_by_address(address):
    with SessionLocal() as session:
        return session.query(Log).filter_by(address=address).order_by(Log.id.desc()).all()

def get_address_summary(address):
    with SessionLocal() as session:
        txs = session.query(Transaction).filter(
            (Transaction.from_address == address) | (Transaction.to_address == address)
        ).all()

        if not txs:
            return None

        block_numbers = [tx.block_number for tx in txs]
        summary = {
            "total_transactions": len(txs),
            "first_seen_block": min(block_numbers),
            "last_seen_block": max(block_numbers),
        }
        return summary

