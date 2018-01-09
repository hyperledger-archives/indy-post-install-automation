"""
Created on Dec 26, 2017

@author: nhan.nguyen
"""

import json
from indy import signus, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestListPairwise(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          signus.create_and_store_my_did,
                                          self.wallet_handle, "{}")

        # 4. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             signus.create_and_store_my_did,
                                             self.wallet_handle, "{}")

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 6. Create pairwise.
        self.steps.add_step("Create pairwise")
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, None)

        # 7. Get list of pairwise from wallet.
        self.steps.add_step("Get list of pairwise from wallet")
        list_pairwise = await utils.perform(self.steps, pairwise.list_pairwise,
                                            self.wallet_handle)

        list_pairwise = json.loads(list_pairwise)

        # 8. Check size of list pairwise.
        self.steps.add_step("Check size of list pairwise")
        error_msg = "Size of list pairwise is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(list_pairwise) == 1)

        # 9. Check the first element in list pairwise.
        self.steps.add_step("Check the first element in list pairwise")
        error_msg = "The first element in list pairwise mismatches"
        expected_pairwise = {"my_did": my_did, "their_did": their_did}
        print(type(list_pairwise[0]))
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: json.loads(list_pairwise[0]) ==
                    expected_pairwise)


if __name__ == "__main__":
    TestListPairwise().execute_scenario()
