"""
Created on Dec 08, 2017

@author: khoi.ngo
Implementing test case open_wallet with valid value.
"""
from indy.error import IndyError
import pytest

from utilities import common
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform
from indy import pool


class TestOpenWallet(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Create and open a pool
        self.steps.add_step("Create and open a pool")
        self.pool_handle = await perform(self.steps,
                                         common.create_and_open_pool,
                                         self.pool_name,
                                         self.pool_genesis_txn_file)

        # 2. Create and open a wallet
        self.steps.add_step("Create and open a wallet")
        returned_code = await perform(self.steps,
                                      common.create_and_open_wallet,
                                      self.pool_name, self.wallet_name, self.wallet_credentials)

        # 3. Verify that user is able to open a new wallet
        self.steps.add_step("Verify the response code of open_wallet API.")
        if not isinstance(returned_code, IndyError):
            self.wallet_handle = returned_code  # using for post-condition
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            self.steps.get_last_step().set_message(
                "Failed. Cannot open the wallet which was created.")
