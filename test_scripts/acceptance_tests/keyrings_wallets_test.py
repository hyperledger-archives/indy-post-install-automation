"""
Created on Nov 8, 2017

@author: khoi.ngo

Containing test script of test scenario 04: keyrings wallets.

Verify that the wallet is created at the correct place and work well.
"""

import pytest
import json
import os.path

from indy import did, pool

from utilities import common
from utilities.constant import seed_default_trustee, work_dir
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class TestKeyringsWallets(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Create and open pool Ledger
        self.steps.add_step("Create and open pool Ledger")
        self.pool_handle, self.wallet_handle = await perform(
                                               self.steps,
                                               common.prepare_pool_and_wallet,
                                               self.pool_name,
                                               self.wallet_name,
                                               self.wallet_credentials,
                                               self.pool_genesis_txn_file)

        # 2. verify wallet was created in .indy/wallet
        self.steps.add_step("Verify wallet was created in .indy/wallet")
        wallet_path = work_dir + "/wallet/" + self.wallet_name
        result = os.path.exists(wallet_path)
        if result:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            message_2 = "Cannot find %s directory." % wallet_path
            self.steps.get_last_step().set_status(Status.PASSED, message_2)

        # 3. create DID to check the new wallet work well.
        self.steps.add_step("Create DID to check the new wallet work well")
        await perform(self.steps, did.create_and_store_my_did,
                      self.wallet_handle,
                      json.dumps({"seed": seed_default_trustee}))
