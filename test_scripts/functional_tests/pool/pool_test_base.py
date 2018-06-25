"""
Created on Dec 8, 2017

@author: nhan.nguyen

Containing a base class for pool testing.
"""

from utilities import common
from utilities.test_scenario_base import TestScenarioBase
from indy import pool


class PoolTestBase(TestScenarioBase):

    async def setup_steps(self):
        await  pool.set_protocol_version(2)
        common.delete_pool_folder(self.pool_name)

    async def teardown_steps(self):
        await common.close_and_delete_pool(self.pool_name, self.pool_handle)
