from utils.web3provider import web3

def get_block_reward(block):
    base_fee = block.get("baseFeePerGas", 0)
    gas_used = block.gasUsed

    reward = base_fee * gas_used if base_fee else 0
    return web3.from_wei(reward, "ether")

