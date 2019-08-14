"""
Created on Dec 14, 2017

@author: nhan.nguyen

Verify that user cannot sign with invalid wallet handle.
"""

import pytest
import json

from indy import did, crypto
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestSignWithValidData(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Create did and verkey with valid seed.
        self.steps.add_step("Create did and verkey with valid seed")
        did_json = json.dumps({"seed": constant.seed_my1})
        (my_did, my_verkey) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, did_json)

        # 4. Use "did.sign" to sign with invalid wallet handle
        # and verify thay user cannot sign successfully.
        self.steps.add_step("Use 'did.sign' to sign with invalid "
                            "wallet handle and verify thay user "
                            "cannot sign successfully")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps, crypto.crypto_sign,
                                               self.wallet_handle + 1, my_verkey,
                                               "Test did".encode("UTF-8"),
                                               expected_code=error_code)
