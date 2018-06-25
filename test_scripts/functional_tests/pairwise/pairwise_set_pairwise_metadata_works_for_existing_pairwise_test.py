"""
Created on Dec 20, 2017

@author: nhan.nguyen

Verify that user can set metadata for an existing pairwise.
"""

import json
import pytest
from indy import did, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestSetPairwiseMetadata(PairwiseTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          did.create_and_store_my_did,
                                          self.wallet_handle, "{}")

        # 4. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             did.create_and_store_my_did,
                                             self.wallet_handle, "{}")

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}),
                            ignore_exception=False)

        # 6. Create pairwise.
        self.steps.add_step("Create pairwise between 'my_did' and 'their_did'")
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, None)

        # 7. Get created pairwise without metadata.
        self.steps.add_step("Get created pairwise without metadata")
        pairwise_without_metadata = await utils.perform(self.steps,
                                                        pairwise.get_pairwise,
                                                        self.wallet_handle,
                                                        their_did)

        # 8. Set metadata for pairwise.
        self.steps.add_step("Set metadata for pairwise")
        metadata = "Test pairwise"
        await utils.perform(self.steps, pairwise.set_pairwise_metadata,
                            self.wallet_handle, their_did, metadata)

        # 9. Get created pairwise with metadata.
        self.steps.add_step("Get created pairwise with metadata")
        pairwise_with_metadata = await utils.perform(self.steps,
                                                     pairwise.get_pairwise,
                                                     self.wallet_handle,
                                                     their_did)

        # 10. Verify that pairwise before and after setting metadata are
        # different from each other.
        self.steps.add_step("Verify that pairwise before and after "
                            "setting metadata are different from each other")
        error_msg = "Pairwise before and after setting " \
                    "metadata are equal each other"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: pairwise_with_metadata !=
                    pairwise_without_metadata)

        # 11. Verify the metadata is set successfully.
        self.steps.add_step("Verify the metadata is set successfully")
        error_msg = "Cannot set metadata for pairwise"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: json.loads(pairwise_with_metadata) ==
                    {"my_did": my_did, "metadata": metadata})
