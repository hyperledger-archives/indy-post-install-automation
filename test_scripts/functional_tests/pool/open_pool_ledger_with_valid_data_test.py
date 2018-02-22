"""
Created on Dec 8, 2017

@author: nhan.nguyen
Verify that user can open a pool ledger with valid data.
"""

from indy import pool

from utilities import utils
from utilities import common, constant
from test_scripts.functional_tests.pool.pool_test_base import PoolTestBase
import pytest


class TestOpenPoolLedgerConfig(PoolTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger configuration.
        self.steps.add_step("Create pool ledger config")
        await utils.perform(self.steps, common.create_pool_ledger_config,
                            self.pool_name, constant.pool_genesis_txn_file)
        # 2. Open pool ledger.
        self.steps.add_step("Open pool ledger")
        self.pool_handle = await \
            utils.perform(self.steps, pool.open_pool_ledger,
                          self.pool_name, None, ignore_exception=True)

        # 3. Verify that returned pool_handle is a positive integer.
        self.steps.add_step("Verify that returned pool_"
                            "handle is a positive integer")
        utils.check(self.steps, error_message="Cannot open pool ledger",
                    condition=lambda: isinstance(self.pool_handle, int) and
                    self.pool_handle >= 0)
