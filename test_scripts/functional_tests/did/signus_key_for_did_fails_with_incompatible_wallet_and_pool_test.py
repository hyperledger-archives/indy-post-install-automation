"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get verkey for did with
incompatible wallet handle and pool handle.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common, constant
from utilities.test_scenario_base import TestScenarioBase


class TestKeyForDidWithIncompatiblePoolAndWallet(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        other_pool_name = "other_" + self.pool_name
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    other_pool_name,
                                                    credentials=self.wallet_credentials)

        # 5. Get verkey with incompatible wallet and pool and
        # verify that user cannot get verkey.
        self.steps.add_step("Get verkey with incompatible wallet and pool and "
                            "verify that user cannot get verkey")
        error_code = ErrorCode.WalletIncompatiblePoolError
        await utils.perform_with_expected_code(self.steps, did.key_for_did,
                                               self.pool_handle,
                                               self.wallet_handle,
                                               constant.did_my1,
                                               expected_code=error_code)
