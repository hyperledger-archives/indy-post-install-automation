"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get endpoint of did with invalid pool handle.
"""

import pytest
from indy import signus
from indy.error import ErrorCode
from utilities import utils, common, constant
from utilities.test_scenario_base import TestScenarioBase


class TestGetEndPointForDidFromLedger(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 6. Get endpoint with invalid pool handle and
        # verify that endpoint cannot be gotten.
        self.steps.add_step("Get endpoint with invalid pool handle and "
                            "verify that endpoint cannot be gotten")
        error_code = ErrorCode.PoolLedgerInvalidPoolHandle
        await utils.perform_with_expected_code(self.steps,
                                               signus.get_endpoint_for_did,
                                               self.wallet_handle,
                                               self.pool_handle + 1, my_did,
                                               expected_code=error_code)
