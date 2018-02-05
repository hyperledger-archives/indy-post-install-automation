"""
Created on Dec 27, 2017

@author: nhan.nguyen

Verify that user can sign with valid verkey.
"""

import pytest
import json
from indy import crypto
from utilities import common, utils, constant
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoSignWithValidData(CryptoTestBase):
    def setup_method(self):
        super().setup_method()
        self.expected_signature = bytes(
            [169, 215, 8, 225, 7, 107, 110, 9, 193, 162, 202, 214, 162, 66,
             238, 211, 63, 209, 12, 196, 8, 211, 55, 27, 120,
             94, 204, 147, 53, 104, 103, 61, 60, 249, 237, 127, 103, 46, 220,
             223, 10, 95, 75, 53, 245, 210, 241, 151, 191,
             41, 48, 30, 9, 16, 78, 252, 157, 206, 210, 145, 125, 133, 109,
             11])

        self.message = '{"reqId":1496822211362017764}'.encode('utf-8')

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey with seed my1.
        self.steps.add_step("Create verkey with seed my1")
        my_verkey = await utils.perform(
            self.steps, crypto.create_key, self.wallet_handle,
            json.dumps({"seed": constant.seed_my1}))

        # 4. Use 'crypto.crypto_sign' to sign.
        self.steps.add_step("Use 'crypto.crypto_sign' to sign")
        signature = await utils.perform(self.steps, crypto.crypto_sign,
                                        self.wallet_handle, my_verkey,
                                        self.message)

        # 5. Check created signature.
        self.steps.add_step("Check created signature")
        error_msg = "Created signature is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: self.expected_signature == signature)
