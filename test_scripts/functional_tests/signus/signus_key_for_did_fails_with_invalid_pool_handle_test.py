"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get verkey if did with invalid pool handle.
"""

import pytest
from indy import signus
from indy.error import ErrorCode
from utilities import utils, common, constant
from utilities.test_scenario_base import TestScenarioBase


class TestKeyForDidWithInvalidPoolHandle(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file
        )

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Get verkey with invalid pool handle and
        # verify that user cannot get verkey.
        self.steps.add_step("Get verkey with invalid pool handle and "
                            "verify that user cannot get verkey")
        error_code = ErrorCode.PoolLedgerInvalidPoolHandle
        await utils.perform_with_expected_code(self.steps, signus.key_for_did,
                                               self.pool_handle + 1,
                                               self.wallet_handle,
                                               constant.did_my1,
                                               expected_code=error_code)
