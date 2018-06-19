"""
Created on Dec 28, 2017

@author: khoi.ngo

Verify that an encrypted message cannot be
decrypted with verkey that does not exist in wallet.
"""

import pytest
from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestOpenCryptoBoxWithUnknownVerkey(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create the first verkey with empty json.
        self.steps.add_step("Create the first key")
        first_key = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Create the second verkey with empty json.
        self.steps.add_step("Create the second key")
        second_key = await utils.perform(self.steps, crypto.create_key,
                                         self.wallet_handle, "{}")

        # 5. Create a crypto box".
        self.steps.add_step("Create a crypto box")
        msg = "Test crypto".encode("UTF-8")
        encrypted_msg = await utils.perform(
                                                self.steps, crypto.auth_crypt,
                                                self.wallet_handle, first_key,
                                                second_key, msg)

        # 6. Open crypto box with unknown verkey. Expected error = 113
        self.steps.add_step("Open a crypto box")
        unknown_verkey = "UNKNOWN_VERKEY"
        await utils.perform_with_expected_code(
                                         self.steps, crypto.auth_decrypt,
                                         self.wallet_handle, unknown_verkey,
                                         encrypted_msg,
                                         expected_code=113)
