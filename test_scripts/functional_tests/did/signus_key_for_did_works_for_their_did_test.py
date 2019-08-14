"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user can get verkey for 'their_did'.
"""

import pytest
import json

from indy import did
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base\
    import DidTestBase


class TestKeyForDidWithTheirDid(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Store 'their_did' and 'their_verkey' into wallet.
        self.steps.add_step("Store 'their_did' and 'their_verkey' into wallet")
        their_did_json = {"did": constant.did_my2,
                          "verkey": constant.verkey_my2}
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle, json.dumps(their_did_json))

        # 4 Get verkey for 'their_did" from wallet.
        self.steps.add_step("Get local verkey of 'their_did' from wallet")
        returned_verkey = await utils.perform(self.steps, did.key_for_did,
                                              -1, self.wallet_handle,
                                              constant.did_my2)

        # 5. Check returned verkey.
        self.steps.add_step("Check returned verkey")
        error_msg = "Returned verkey mismatch with 'their_verkey'"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_verkey == constant.verkey_my2)
