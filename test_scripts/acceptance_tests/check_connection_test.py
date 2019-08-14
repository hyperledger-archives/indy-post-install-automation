"""
Created on Nov 10, 2017

@author: nhan.nguyen

Containing test script of test scenario 03: check connection.

Verify that user can connect to the pool ledger.
"""

import pytest
import json

from indy import did, wallet, pool

from utilities.constant import *
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class TestCheckConnection(TestScenarioBase):
    seed_steward01 = "000000000000000000000000Steward1"

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        pool_config = json.dumps(
            {"genesis_txn": str(pool_genesis_txn_file)})
        # 1. Create pool ledger
        self.steps.add_step("Create pool ledger")
        await perform(self.steps, pool.create_pool_ledger_config,
                      self.pool_name, pool_config, ignore_exception=False)

        # 2. Create wallet
        self.steps.add_step("Create wallet")
        await perform(self.steps, wallet.create_wallet, self.pool_name,
                      self.wallet_name, None, None, wallet_credentials)
        self.wallet_handle = await perform(self.steps, wallet.open_wallet,
                                           self.wallet_name, None, wallet_credentials)

        # 3. Create DID
        self.steps.add_step("Create DID")
        await perform(self.steps, did.create_and_store_my_did,
                      self.wallet_handle,
                      json.dumps({"seed": self.seed_steward01}))

        # 4. Connect to pool.
        # Verify that the default wallet move to Test from NoEnv?
        # Cannot verify because ".indy/wallet" do'nt include any folder
        # that name no-env and test, and default wallet cannot be created
        # via indy-sdk
        self.steps.add_step("Connect to pool")
        self.pool_handle = await perform(self.steps, pool.open_pool_ledger,
                                         self.pool_name, None)

        # 5. Disconnect from pool.
        self.steps.add_step("Disconnect form pool")
        await perform(self.steps, pool.close_pool_ledger, self.pool_handle)

        # 6. Reconnect to pool.
        self.steps.add_step("Reconnect to pool")
        self.pool_handle = await perform(self.steps, pool.open_pool_ledger,
                                         self.pool_name, None)
