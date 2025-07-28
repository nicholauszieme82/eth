import time
from app import web3, SessionLocal
from app.models import Block, Transaction, Log
from sqlalchemy.exc import IntegrityError

def store_block(block_number):
    session = SessionLocal()
    try:
        if session.query(Block).get(block_number):
            print(f"⏭️ Block #{block_number} already exists.")
            return

        block = web3.eth.get_block(block_number, full_transactions=True)

        b = Block(
            number=block.number,
            hash=block.hash.hex(),
            parent_hash=block.parentHash.hex(),
            miner=block.miner,
            timestamp=block.timestamp,
            gas_limit=block.gasLimit,
            gas_used=block.gasUsed,
        )
        session.add(b)

        for tx in block.transactions:
            receipt = web3.eth.get_transaction_receipt(tx.hash)
            t = Transaction(
                hash=tx.hash.hex(),
                block_number=tx.blockNumber,
                from_address=tx["from"],
                to_address=tx.to,
                value=tx.value,
                gas=tx.gas,
                gas_price=tx.gasPrice,
                nonce=tx.nonce,
                status=str(receipt.status),
                gas_used=receipt.gasUsed,
                contract_address=receipt.contractAddress,
            )
            session.add(t)

            for log in receipt.logs:
                l = Log(
                    tx_hash=tx.hash.hex(),
                    address=log.address,
                    data=log.data,
                    topic0=log.topics[0].hex() if len(log.topics) > 0 else None,
                    topic1=log.topics[1].hex() if len(log.topics) > 1 else None,
                    topic2=log.topics[2].hex() if len(log.topics) > 2 else None,
                    topic3=log.topics[3].hex() if len(log.topics) > 3 else None,
                )
                session.add(l)

        session.commit()
        print(f"✅ Stored block #{block_number}")
    except IntegrityError:
        session.rollback()
        print(f"⚠️ Duplicate entry for block #{block_number}")
    except Exception as e:
        session.rollback()
        print(f"❌ Error storing block #{block_number}: {e}")
    finally:
        session.close()

def get_latest_stored_block():
    session = SessionLocal()
    try:
        last = session.query(Block).order_by(Block.number.desc()).first()
        return last.number if last else -1
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 Starting full sync from genesis...")

    while True:
        chain_latest = web3.eth.block_number
        db_latest = get_latest_stored_block()

        if db_latest < chain_latest:
            for block_num in range(db_latest + 1, chain_latest + 1):
                store_block(block_num)
        else:
            print(f"🟢 Up to date at block #{chain_latest}, waiting...")
            time.sleep(2)  # wait and poll again

