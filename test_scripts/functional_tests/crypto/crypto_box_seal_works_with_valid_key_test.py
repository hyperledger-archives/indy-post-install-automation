"""
Created on Jan 2, 2018

@author: nhan.nguyen

Verify that user can encrypt anonymous message with valid data.
"""

import pytest
from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoBoxSealWithValidKey(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create verkey.
        self.steps.add_step("Create verkey")
        my_verkey = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Create sealed crypto box and verify that
        # there is no exception raised.
        self.steps.add_step("Create sealed crypto box and verify that "
                            "there is no exception raised")
        msg = "Test crypto".encode()
        encrypted_msg = await utils.perform(self.steps,
                                            crypto.anon_crypt,
                                            my_verkey, msg,
                                            ignore_exception=False)

        # 5. Open sealed crypto box.
        self.steps.add_step("Open sealed crypto box")
        decrypted_msg = await utils.perform(self.steps,
                                            crypto.anon_decrypt,
                                            self.wallet_handle,
                                            my_verkey, encrypted_msg)

        # 6. Check decrypted message.
        self.steps.add_step("Check encrypted message")
        error_msg = "Decrypted message mismatches"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: decrypted_msg == msg)
