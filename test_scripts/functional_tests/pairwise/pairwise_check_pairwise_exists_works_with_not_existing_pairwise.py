"""
Created on Dec 20, 2017

@author: nhan.nguyen
"""

import json
from indy import signus, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestCheckPairwiseNotExist(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             signus.create_and_store_my_did,
                                             self.wallet_handle, '{}')

        # 4. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle, json.dumps({"did": their_did}))

        # 5. Verify that 'is_pairwise_exists' return 'False'.
        self.steps.add_step("Verify that 'is_pairwise_exists' return 'False'")
        pairwise_exists = await utils.perform(self.steps,
                                              pairwise.is_pairwise_exists,
                                              self.wallet_handle,
                                              their_did)
        utils.check(self.steps,
                    error_message="'True' is returned instead of 'False'",
                    condition=lambda: pairwise_exists is False)


if __name__ == "__main__":
    TestCheckPairwiseNotExist().execute_scenario()
