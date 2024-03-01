from algosdk.v2client import algod
from algosdk import encoding
from algosdk.abi import ABIType
import time

algod_token = 'INSERT YOUR NODE TOKEN HERE'
algod_port = 'INSERT YOUR NODE PORT HERE'

algod_client = algod.AlgodClient(algod_token, algod_port)

def decode_vote_weights(vote_weights_encoded):
    vote_weights_type = ABIType.from_string("uint64[]")
    vote_weights_bytes = encoding.base64.b64decode(vote_weights_encoded)
    vote_weights = vote_weights_type.decode(vote_weights_bytes)
    return vote_weights

#THESE PROPOSAL NUMBERS ARE VALID FOR PERIOD 3, REPLACE WITH RESPECTIVE PERIOD'S PROPOSAL NUMBERS
proposal_nums = [
    "92", "95", "96", "98", "99", "100", "104", "107", "108", "109", "110", "112",
    "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123",
    "130", "141", "142", "143", "144", "145", "148", "149", "150", "152", "153",
    "154", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165",
    "167", "168", "170", "01"
]

#THIS APPLICATION ID IS VALID FOR PERIOD 3, REPLACE WITH RESPECTIVE PERIOD'S APP ID
APP_ID = 1484325878
last_block_tracked = 0

while True:
    algod_client = algod.AlgodClient(algod_token, algod_port)
    last_block = algod_client.status()['last-round']
    if last_block > last_block_tracked:
        last_block_tracked = last_block
        block_tx_ids = algod_client.get_block_txids(last_block)['blockTxids']
        for tx_id in block_tx_ids:
            tx_info = algod_client.pending_transaction_info(tx_id)['txn']['txn']
            if tx_info['type'] == 'appl' and 'apid' in tx_info:

                if tx_info['apid'] == APP_ID:
                    args = tx_info['apaa']
                     
                    if args[0] == 'xA/9qg==':
                        vote_weights_encoded = args[-2]  
                        vote_weights = decode_vote_weights(vote_weights_encoded)
                        address = tx_info['snd']
                        vote_weights_mapped = {proposal_nums[i]: "{:,}".format(weight) for i, weight in enumerate(vote_weights) if weight > 0}
                        print(f"Address {address} voted for proposals with weights: {vote_weights_mapped}")
    time.sleep(2)
