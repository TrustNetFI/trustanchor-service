#!/usr/bin/env python3.6

import argparse
import asyncio
import json

from indy import pool, signus, wallet
from indy.error import ErrorCode, IndyError

async def register_did():
    pool_name = "my-test-network"
    pool_genesis_txn_path = "my-test-network.txn"
    
    wallet_name = "ta-wallet"
    ta_seed = "424242424242MyTestTrustAnchor424"

    try:
        pool_config = json.dumps({ "genesis_txn": pool_genesis_txn_path})
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError as error:
        if error.error_code != ErrorCode.PoolLedgerConfigAlreadyExistsError:
            raise error
        
    pool_handle = await pool.open_pool_ledger(pool_name, None)

    try:
        await wallet.create_wallet(pool_name, wallet_name, None, None, None)
    except IndyError as error:
        if error.error_code != ErrorCode.WalletAlreadyExistsError:
            raise error

    wallet_handle = await wallet.open_wallet(wallet_name, None, None)

    (did, ver_key, pub_key) = await signus.create_and_store_my_did(wallet_handle, json.dumps({ "seed": ta_seed }))

    print(did, ver_key, pub_key)




    

    await wallet.close_wallet(wallet_handle)

    await pool.close_pool_ledger(pool_handle)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('did', type=str)
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register_did(parser.did))
    loop.close()
