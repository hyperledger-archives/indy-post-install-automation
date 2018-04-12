"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that user cannot get endpoint of an unknown did.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common, constant
from utilities.test_scenario_base import TestScenarioBase


class TestGetEndPointForDidWithUnknownDid(TestScenarioBase):
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

        # 5. Get endpoint of an unknown did and
        # verify that endpoint cannot be gotten.
        self.steps.add_step("Get endpoint of an unknown did and "
                            "verify that endpoint cannot be gotten")
        error_code = ErrorCode.CommonInvalidState
        await utils.perform_with_expected_code(self.steps,
                                               did.get_endpoint_for_did,
                                               self.wallet_handle,
                                               self.pool_handle,
                                               constant.did_my1,
                                               expected_code=error_code)
