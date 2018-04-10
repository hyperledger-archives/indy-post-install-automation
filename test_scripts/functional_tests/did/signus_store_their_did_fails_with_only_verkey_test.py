"""
Created on Dec 12, 2017

@author: nhan.nguyen

Verify that user cannot store 'their_did' with only verkey (without did).
"""

import pytest
import json

from indy import did
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestStoreOnlyVerkeyIntoWallet(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (_, their_verkey) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Store only "their_verkey" into wallet and
        # verify that use cannot store only verkey into wallet.
        self.steps.add_step("Store only 'their_verkey' into wallet and verify "
                            "that use cannot store only verkey into wallet")
        key_did = json.dumps({"verkey": their_verkey})
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(self.steps,
                                               did.store_their_did,
                                               self.wallet_handle,
                                               key_did,
                                               expected_code=error_code)
