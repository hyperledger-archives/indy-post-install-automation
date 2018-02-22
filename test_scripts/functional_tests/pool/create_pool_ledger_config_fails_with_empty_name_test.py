"""
Created on Dec 12, 2017

@author: nhan.nguyen
Verify that user cannot create a pool ledger configuration with
empty "pool_name".
"""

from indy.error import ErrorCode
from utilities import utils
from utilities import common, constant
from test_scripts.functional_tests.pool.pool_test_base import PoolTestBase
import pytest


class TestCreatePoolConfigFailsWithEmptyName(PoolTestBase):

    @pytest.mark.asyncio
    async def test(self):
        self.pool_name = ""
        # 1. Create a pool ledger config and verify that
        # cannot create a pool ledger config with empty pool name.
        self.steps.add_step("Create a pool ledger config and verify that "
                            "cannot create a pool ledger config "
                            "with empty pool name")
        error_code = ErrorCode.CommonInvalidParam2
        await utils.perform_with_expected_code(
            self.steps, common.create_pool_ledger_config, self.pool_name,
            constant.pool_genesis_txn_file, expected_code=error_code)
