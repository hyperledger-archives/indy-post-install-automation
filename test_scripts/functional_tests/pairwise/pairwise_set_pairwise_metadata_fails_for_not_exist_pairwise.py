"""
Created on Dec 26, 2017

@author: nhan.nguyen
"""

import json
from indy import signus, pairwise
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestSetPairwiseMetadataForNotExistPairwise(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             signus.create_and_store_my_did,
                                             self.wallet_handle, "{}")

        # 4. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 5. Set metadata for not exist pairwise and
        # verify that metadata cannot be set.
        self.steps.add_step("Set metadata for not exist pairwise and "
                            "verify that metadata cannot be set")
        metadata = "Test pairwise"
        error_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               pairwise.set_pairwise_metadata,
                                               self.wallet_handle, their_did,
                                               metadata,
                                               expected_code=error_code)


if __name__ == "__main__":
    TestSetPairwiseMetadataForNotExistPairwise().execute_scenario()
