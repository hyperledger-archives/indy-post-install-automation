"""
Created on Dec 28, 2017

@author: khoi.ngo

Verify that user cannot encrypt message by an unknown verkey.
"""

import pytest
from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoBoxWithUnknownVerkey(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. VP: Create a crypto box with Expected error = 113
        self.steps.add_step("Create a crypto box with Expected error = 113")
        first_key = "UNKNOWN"
        second_key = "UNKNOWN"
        msg = "Test crypto".encode("UTF-8")
        await utils.perform_with_expected_code(
                                     self.steps, crypto.auth_crypt,
                                     self.wallet_handle, first_key, second_key,
                                     msg, expected_code=113)
