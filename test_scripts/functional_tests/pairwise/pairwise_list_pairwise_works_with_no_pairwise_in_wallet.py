"""
Created on Dec 26, 2017

@author: nhan.nguyen
"""

import json
from indy import pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestListPairwiseWithNoPairwiseInWallet(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Get list of pairwise from wallet.
        self.steps.add_step("Get list of pairwise from wallet")
        list_pairwise = await utils.perform(self.steps, pairwise.list_pairwise,
                                            self.wallet_handle)

        list_pairwise = json.loads(list_pairwise)

        # 4. Check size of list pairwise.
        self.steps.add_step("Check size of list pairwise")
        error_msg = "List pairwise is not empty"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(list_pairwise) == 0)


if __name__ == "__main__":
    TestListPairwiseWithNoPairwiseInWallet().execute_scenario()
