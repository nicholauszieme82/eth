from datetime import datetime, timezone
from utils.formatter import format_time_ago
from utils.formatter import clean_hex
from core.reward import get_block_reward

def process_block(block):
    timestamp = block.timestamp
    timestamp_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    time_ago_str = format_time_ago(datetime.now(timezone.utc).timestamp() - timestamp)

    gas_used = block.gasUsed
    gas_limit = block.gasLimit
    gas_pct = (gas_used / gas_limit * 100) if gas_limit else 0

    print("========== blc info ==========")
    print(f"[Blc Number]       {block.number}")
    print(f"[Blc Height]       {block.number}")
    print(f"[Timestamp]        {timestamp_dt} UTC ({time_ago_str} ago)")
    print(f"[Transactions]     {len(block.transactions)}")
    print(f"[Validated By]     {block.miner}")
    print(f"[Blc Reward]       {get_block_reward(block)} ETH")
    print(f"[Difficulty]       {block.difficulty}")
    print(f"[Total Difficulty] {block.totalDifficulty}")
    print(f"[Size]             {block.size} bytes")
    print(f"[Gas Used]         {gas_used:,} ({gas_pct:.2f}%)")
    print(f"[Gas Limit]        {gas_limit:,}")
    print(f"[Extra Data]       {clean_hex(block.extraData)}")
    print(f"[Hash]             {block.hash.hex()}")
    print(f"[Parent Hash]      {block.parentHash.hex()}")
    print(f"[SHA3 Uncles]      {block.sha3Uncles.hex()}")
    print("================================")

