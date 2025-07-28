from flask import jsonify, request
from app.queries import (
    get_block_by_number,
    get_transaction_by_hash,
    get_transactions_by_address,
    get_logs_by_contract,
    get_latest_blocks,
    get_block_by_hash,
    get_transactions_in_block,
    get_blocks_in_range,
    get_logs_by_address,
    get_address_summary,
)

def init_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Ethereum Explorer API (Flask)"})

    @app.route("/blocks/<int:number>")
    def block(number):
        block = get_block_by_number(number)
        if not block:
            return jsonify({"error": "Block not found"}), 404
        return jsonify({
            "number": block.number,
            "hash": block.hash,
            "miner": block.miner,
            "timestamp": block.timestamp,
            "gas_limit": block.gas_limit,
            "txs": [tx.hash for tx in block.transactions]
        })

    @app.route("/txs/<string:tx_hash>")
    def transaction(tx_hash):
        tx = get_transaction_by_hash(tx_hash)
        if not tx:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify({
            "hash": tx.hash,
            "from": tx.from_address,
            "to": tx.to_address,
            "value": tx.value,
            "status": tx.status,
            "block_number": tx.block_number,
        })

    @app.route("/txs/by-address")
    def tx_by_address():
        address = request.args.get("address")
        if not address:
            return jsonify({"error": "Missing address param"}), 400
        txs = get_transactions_by_address(address)
        return jsonify([{
            "hash": tx.hash,
            "from": tx.from_address,
            "to": tx.to_address,
            "block": tx.block_number
        } for tx in txs])

    @app.route("/logs/by-contract")
    def logs_by_contract():
        address = request.args.get("address")
        if not address:
            return jsonify({"error": "Missing address param"}), 400
        logs = get_logs_by_contract(address)
        return jsonify([{
            "tx_hash": log.tx_hash,
            "data": log.data,
            "topics": [log.topic0, log.topic1, log.topic2, log.topic3]
        } for log in logs])

    @app.route("/blocks/latest")
    def latest_blocks():
        blocks = get_latest_blocks(10)
        return jsonify([{
            "number": b.number,
            "hash": b.hash,
            "miner": b.miner,
            "timestamp": b.timestamp,
            "gas_used": b.gas_used
        } for b in blocks])

    @app.route("/blocks/hash/<string:block_hash>")
    def block_by_hash(block_hash):
        block = get_block_by_hash(block_hash)
        if not block:
            return jsonify({"error": "Block not found"}), 404
        return jsonify({
            "number": block.number,
            "hash": block.hash,
            "miner": block.miner,
            "timestamp": block.timestamp,
            "gas_limit": block.gas_limit,
            "txs": [tx.hash for tx in block.transactions]
        })

    @app.route("/txs/in-block/<int:block_number>")
    def txs_in_block(block_number):
        txs = get_transactions_in_block(block_number)
        return jsonify([{
            "hash": tx.hash,
            "from": tx.from_address,
            "to": tx.to_address,
            "value": tx.value,
            "gas": tx.gas,
            "gas_price": tx.gas_price
        } for tx in txs])

    @app.route("/blocks/range")
    def blocks_range():
        try:
            start = int(request.args.get("from"))
            end = int(request.args.get("to"))
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid or missing 'from' or 'to' params"}), 400

        blocks = get_blocks_in_range(start, end)
        return jsonify([{
            "number": b.number,
            "hash": b.hash,
            "miner": b.miner,
            "timestamp": b.timestamp
        } for b in blocks])

    @app.route("/address/<string:address>/txs")
    def address_txs(address):
        txs = get_transactions_by_address(address)
        return jsonify([{
            "hash": tx.hash,
            "from": tx.from_address,
            "to": tx.to_address,
            "value": tx.value,
            "block": tx.block_number
        } for tx in txs])

    @app.route("/address/<string:address>/logs")
    def address_logs(address):
        logs = get_logs_by_address(address)
        return jsonify([{
            "tx_hash": log.tx_hash,
            "data": log.data,
            "topics": [log.topic0, log.topic1, log.topic2, log.topic3]
        } for log in logs])

    @app.route("/address/<string:address>/summary")
    def address_summary(address):
        summary = get_address_summary(address)
        if not summary:
            return jsonify({"error": "No transactions found"}), 404
        return jsonify(summary)

