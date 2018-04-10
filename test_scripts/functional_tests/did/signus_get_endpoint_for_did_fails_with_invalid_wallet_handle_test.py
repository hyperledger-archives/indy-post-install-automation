"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get endpoint of did with invalid wallet handle.
"""

import pytest
from indy import did
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
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 6. Set endpoint for created did.
        self.steps.add_step("Set endpoint for created did")
        await utils.perform(self.steps, did.set_endpoint_for_did,
                            self.wallet_handle, my_did, constant.endpoint,
                            my_verkey)

        # 7. Get endpoint with invalid wallet handle and
        # verify that endpoint cannot be gotten.
        self.steps.add_step("Get endpoint with invalid wallet handle and "
                            "verify that endpoint cannot be gotten")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               did.get_endpoint_for_did,
                                               self.wallet_handle + 1,
                                               self.pool_handle, my_did,
                                               expected_code=error_code)
