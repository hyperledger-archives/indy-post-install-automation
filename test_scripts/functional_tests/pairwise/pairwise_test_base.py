"""
Created on Dec 20, 2017

@author: nhan.nguyen

Containing a base class for pairwise testing.
"""

from utilities import common
from utilities.test_scenario_base import TestScenarioBase


class PairwiseTestBase(TestScenarioBase):
    async def setup_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def teardown_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle)
