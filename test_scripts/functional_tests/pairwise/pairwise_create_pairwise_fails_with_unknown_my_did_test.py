"""
Created on Dec 26, 2017

@author: nhan.nguyen

Verify that user cannot create pairwise with unknown 'my_did'
"""

import json
import pytest
from indy import did, pairwise
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestCreatePairwiseWithUnknownMyDid(PairwiseTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             did.create_and_store_my_did,
                                             self.wallet_handle, "{}")

        # 4. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 5. Create pairwise with unknown 'my_did' and
        # verify that pairwise cannot be created.
        error_code = ErrorCode.WalletItemNotFound
        self.steps.add_step("Create pairwise with unknown 'my_did' and "
                            "verify that pairwise cannot be created")
        await utils.perform_with_expected_code(self.steps,
                                               pairwise.create_pairwise,
                                               self.wallet_handle, their_did,
                                               constant.verkey_my1, None,
                                               expected_code=error_code)
