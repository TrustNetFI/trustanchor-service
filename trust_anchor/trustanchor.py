#!/usr/bin/env python3.6

import asyncio
import json

from indy import ledger, pool, signus, wallet
from indy.error import ErrorCode, IndyError

class TrustAnchor(object):
    @classmethod
    async def create(cls):
        self = TrustAnchor()
        settings = {
            'pool_name': "my-test-network",
            'pool_genesis_txn_path': "my-test-network.txn",
            'wallet_name': "ta-wallet",
            'ta_seed': "424242424242MyTestTrustAnchor424",
        }
        pool_name = settings['pool_name']
        try:
            self.pool_config = json.dumps({ "genesis_txn": settings['pool_genesis_txn_path'] })
            await pool.create_pool_ledger_config(pool_name, self.pool_config)
        except IndyError as error:
            if error.error_code != ErrorCode.PoolLedgerConfigAlreadyExistsError:
                raise error

        self.pool_handle = await pool.open_pool_ledger(pool_name, None)

        wallet_name = settings['wallet_name']
        try:
            await wallet.create_wallet(pool_name, wallet_name, None, None, None)
        except IndyError as error:
            if error.error_code != ErrorCode.WalletAlreadyExistsError:
                raise error

        self.wallet_handle = await wallet.open_wallet(wallet_name, None, None)

        (self.trustanchor_did, ver_key, pub_key) = await signus.create_and_store_my_did(self.wallet_handle, json.dumps({ "seed": settings['ta_seed'] }))
        print("TRUST ANCHOR initialised", self.trustanchor_did, ver_key, pub_key)
        return self

    async def register_did(self, did, verkey):
        nym_txn_req = await ledger.build_nym_request(self.trustanchor_did, did, verkey, None, None)
        try:
            await ledger.sign_and_submit_request(self.pool_handle, self.wallet_handle, self.trustanchor_did, nym_txn_req)
        except IndyError as error:
            return {'error': str(error)}

        get_nym_txn_req = await ledger.build_get_nym_request(self.trustanchor_did, did)
        get_nym_txn_resp = await ledger.submit_request(self.pool_handle, get_nym_txn_req)

        get_nym_txn_resp = json.loads(get_nym_txn_resp)
        
        return {'result': get_nym_txn_resp['result']}

    async def destroy(self):
        await wallet.close_wallet(self.wallet_handle)
        await pool.close_pool_ledger(self.pool_handle)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(register_did(parser.did))
    # loop.close()
