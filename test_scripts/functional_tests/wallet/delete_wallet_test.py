"""
Created on Dec 8, 2017

@author: khoi.ngo

Implementing test case DeleteWallet with valid value.
"""
from indy import wallet, pool
from indy.error import ErrorCode
import pytest

from utilities import common
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, perform_with_expected_code


class TestDeleteWallet(TestScenarioBase):
    async def teardown_steps(self):
        common.clean_up_pool_and_wallet_folder(self.pool_name,
                                               self.wallet_name)

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Create and open a pool
        self.steps.add_step("Create and open a pool Ledger")
        self.pool_handle = await perform(self.steps,
                                         common.create_and_open_pool,
                                         self.pool_name,
                                         self.pool_genesis_txn_file)

        # 2. Create and open a wallet
        self.steps.add_step("Create and open wallet")
        self.wallet_handle = await perform(self.steps,
                                           common.create_and_open_wallet,
                                           self.pool_name, self.wallet_name, self.wallet_credentials)

        # 3. Close wallet
        self.steps.add_step("Close wallet.")
        await perform(self.steps, wallet.close_wallet, self.wallet_handle)

        # 4. Delete wallet
        self.steps.add_step("Delete wallet.")
        await perform(self.steps, wallet.delete_wallet, self.wallet_name, self.wallet_credentials)

        # 5. Verify that user is able
        # to delete a wallet by opening that wallet.
        # expected code is WalletNotFoundError
        self.steps.add_step("Verify that user is able to "
                            "delete a wallet by opening that wallet.")
        assert await perform_with_expected_code(
            self.steps, wallet.open_wallet, self.wallet_name, None, self.wallet_credentials,
            expected_code=ErrorCode.WalletNotFoundError)
