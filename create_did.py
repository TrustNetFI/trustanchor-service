#!/usr/bin/env python3.6

import asyncio
import json

from indy import ledger, pool, signus, wallet
from indy.error import ErrorCode, IndyError

async def main():
    settings = {
        'pool_name': "my-test-network",
        'pool_genesis_txn_path': "my-test-network.txn",
    }
    pool_name = settings['pool_name']
    try:
        pool_config = json.dumps({ "genesis_txn": settings['pool_genesis_txn_path'] })
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError as error:
        if error.error_code != ErrorCode.PoolLedgerConfigAlreadyExistsError:
            raise error

    pool_handle = await pool.open_pool_ledger(pool_name, None)

    wallet_name = 'my-wallet'
    try:
        await wallet.create_wallet(pool_name, wallet_name, None, None, None)
    except IndyError as error:
        if error.error_code != ErrorCode.WalletAlreadyExistsError:
            raise error

    wallet_handle = await wallet.open_wallet(wallet_name, None, None)

    (did, ver_key, pub_key) = await signus.create_and_store_my_did(wallet_handle, "{}")


    print()
    print("CREATED DID: {} VERKEY: {} PUBKEY: {}".format(did, ver_key, pub_key))
    print()
    print("http://127.0.0.1:8000/?did={}&verkey={}".format(did, ver_key))
    print()

    await wallet.close_wallet(wallet_handle)
        
    await pool.close_pool_ledger(pool_handle)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
