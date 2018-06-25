"""
Created on Dec 20, 2017

@author: nhan.nguyen

Verify that user can create a pairwise without metadata.
"""

import json
import pytest
from indy import did, pairwise
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestCreatePairwiseWithoutMetadata(PairwiseTestBase):
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
        (their_did, _) = await  utils.perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            "{}")

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 6. Create pairwise without metadata and
        # verify that there is no exception raised.
        self.steps.add_step("Create pairwise without metadata and "
                            "verify that there is no exception raised")
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, None,
                            ignore_exception=False)

        # 7. Get created pairwise.
        self.steps.add_step("Get created pairwise")
        pairwise_without_metadata = await utils.perform(self.steps,
                                                        pairwise.get_pairwise,
                                                        self.wallet_handle,
                                                        their_did)

        # 8. Verify 'pairwise_without_metadata'.
        self.steps.add_step("Verify 'pairwise_without_metadata'")
        expected_pairwise = utils.create_gotten_pairwise_json(my_did, None)
        utils.check(self.steps, error_message="Gotten pairwise mismatches",
                    condition=lambda: json.loads(pairwise_without_metadata) ==
                    expected_pairwise)
