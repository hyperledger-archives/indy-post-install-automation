"""
Created on Dec 26, 2017

@author: nhan.nguyen
"""

import json
from indy import signus, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestResetPairwiseMetadata(PairwiseTestBase):
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
                            json.dumps({"did": their_did}),
                            ignore_exception=False)

        # 6. Create pairwise.
        self.steps.add_step("Create pairwise between 'my_did' and 'their_did'")
        metadata = "Test pairwise"
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, metadata)

        # 7. Get created pairwise with metadata.
        self.steps.add_step("Get created pairwise without metadata")
        pairwise_with_metadata = await utils.perform(self.steps,
                                                     pairwise.get_pairwise,
                                                     self.wallet_handle,
                                                     their_did)

        # 8. Verify that gotten pairwise contains metadata.
        self.steps.add_step("Verify that gotten pairwise contains metadata")
        error_msg = "Gotten pairwise mismatches"
        expected_pairwise = utils.create_gotten_pairwise_json(my_did, metadata)
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: json.loads(pairwise_with_metadata) ==
                    expected_pairwise)

        # 9. Set metadata for pairwise to reset metadata.
        self.steps.add_step("Set metadata for pairwise to reset metadata")
        metadata = None
        await utils.perform(self.steps, pairwise.set_pairwise_metadata,
                            self.wallet_handle, their_did, metadata)

        # 10. Get pairwise of which metadata is reset.
        self.steps.add_step("Get pairwise of which metadata is reset")
        pairwise_without_metadata = await utils.perform(self.steps,
                                                        pairwise.get_pairwise,
                                                        self.wallet_handle,
                                                        their_did)

        # 11. Verify that pairwise before and after
        # setting metadata is different from each other.
        self.steps.add_step("Verify that pairwise before and after "
                            "setting metadata is different from each other")
        error_msg = "Pairwise before and after setting " \
                    "metadata are equal each other"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: pairwise_with_metadata !=
                    pairwise_without_metadata)

        # 12. Verify the metadata is reset successfully.
        self.steps.add_step("Verify the metadata is reset successfully")
        error_msg = "Cannot reset metadata for pairwise"
        expected_pairwise = utils.create_gotten_pairwise_json(my_did)
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: json.loads(pairwise_without_metadata) ==
                    expected_pairwise)


if __name__ == "__main__":
    TestResetPairwiseMetadata().execute_scenario()
