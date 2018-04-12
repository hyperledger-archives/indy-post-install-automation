"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user can get verkey for 'my_did'.
"""

import pytest
from indy import did
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base\
    import DidTestBase


class TestKeyForDidWithMyDid(DidTestBase):
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
        (my_did, my_verkey) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Get verkey of 'my_did' from wallet.
        self.steps.add_step("Get local verkey of 'my_did' from wallet")
        returned_verkey = await utils.perform(self.steps, did.key_for_did,
                                              -1, self.wallet_handle, my_did)

        # 5. Check returned verkey.
        self.steps.add_step("Check returned verkey")
        error_msg = "Returned verkey mismatch with 'my_verkey'"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_verkey == my_verkey)
