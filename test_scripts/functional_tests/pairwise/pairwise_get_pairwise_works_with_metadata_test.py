"""
Created on Dec 26, 2017

@author: nhan.nguyen

Verify that user can get pairwise with metadata.
"""

import json
import pytest
from indy import did, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestGetPairwiseWithMetadata(PairwiseTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          did.create_and_store_my_did,
                                          self.wallet_handle, "{}")

        # 4. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             did.create_and_store_my_did,
                                             self.wallet_handle, '{}')

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 6. Create pairwise with metadata.
        self.steps.add_step("Create pairwise with metadata")
        metadata = "Test pairwise"
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, metadata)

        # 7 Get created pairwise.
        self.steps.add_step("Get created pairwise")
        pairwise_with_metadata = await utils.perform(self.steps,
                                                     pairwise.get_pairwise,
                                                     self.wallet_handle,
                                                     their_did)

        # 8. Check returned pairwise.
        self.steps.add_step("Check returned pairwise")
        utils.check(self.steps, error_message="Gotten pairwise mismatches",
                    condition=lambda:
                    json.loads(pairwise_with_metadata) ==
                    {"my_did": my_did, "metadata": metadata})
