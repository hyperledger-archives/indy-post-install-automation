"""
Created on Dec 8, 2017

@author: nhan.nguyen
Verify that user can delete an existing pool config.
"""

from indy import pool
from utilities import utils
from utilities import common, constant
from test_scripts.functional_tests.pool.pool_test_base import PoolTestBase
import pytest


class TestDeletePoolLedgerConfig(PoolTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        self.steps.add_step("Create pool ledger config")
        await utils.perform(self.steps, common.create_pool_ledger_config,
                            self.pool_name, constant.pool_genesis_txn_file)

        # 2. Delete created pool ledger config.
        self.steps.add_step("Delete created pool ledger config")
        result = await \
            utils.perform(self.steps, pool.delete_pool_ledger_config,
                          self.pool_name, ignore_exception=True)

        # 3. Verify that pool ledger config is deleted.
        self.steps.add_step("Verify that pool ledger config is deleted")
        error_message = "Cannot delete a pool ledger config"
        if utils.check(self.steps, error_message,
                       condition=lambda: not isinstance(result, Exception) and
                       not utils.check_pool_exist(self.pool_name)):
            # prevent post-condition clean up the pool again.
            self.pool_name = None
