"""
Created on Dec 12, 2017

@author: nhan.nguyen

Verify that user cannot store 'their_did' with invalid wallet handle.
"""

import pytest
import json

from indy import did
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestStoreDidWithInvalidWalletHandle(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (their_did, _) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Store 'their_did' with invalid wallet handle and
        # verify that created did cannot be stored.
        self.steps.add_step("Store 'their_did' with invalid wallet handle and"
                            " verify that created did cannot be stored")
        did_json = json.dumps({"did": their_did})
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               did.store_their_did,
                                               self.wallet_handle + 1,
                                               did_json,
                                               expected_code=error_code)
