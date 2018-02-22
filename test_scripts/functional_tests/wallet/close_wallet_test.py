"""
Created on Dec 8, 2017

@author: khoi.ngo

Implementing test case CloseWallet with valid value.
"""
from indy import wallet, signus
from indy.error import ErrorCode
import pytest

from utilities import common
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, perform_with_expected_code


class TestCloseWallet(TestScenarioBase):
    async def teardown_steps(self):
        await perform(self.steps, wallet.delete_wallet, self.wallet_name, None)
        common.clean_up_pool_and_wallet_folder(self.pool_name,
                                               self.wallet_name)

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create and open a pool
        self.steps.add_step("Create pool Ledger")
        self.pool_handle = await perform(self.steps,
                                         common.create_and_open_pool,
                                         self.pool_name,
                                         self.pool_genesis_txn_file)

        # 2. Create and open a wallet
        self.steps.add_step("Create and open wallet")
        self.wallet_handle = await perform(self.steps,
                                           common.create_and_open_wallet,
                                           self.pool_name, self.wallet_name)

        # 3. Close wallet
        self.steps.add_step("Close wallet.")
        await perform(self.steps, wallet.close_wallet, self.wallet_handle)

        # 4. Verify close wallet successfully by
        # creating and storing did in that wallet
        # expected code is WalletInvalidHandle.
        self.steps.add_step("Verify close wallet successfully by "
                            "creating and storing did in that wallet.")
        assert await perform_with_expected_code(
            self.steps, signus.create_and_store_my_did,
            self.wallet_handle, "{}",
            expected_code=ErrorCode.WalletInvalidHandle)
