"""
Created on Dec 27, 2017

@author: nhan.nguyen

Verify that user cannot sign with invalid wallet handle.
"""

import pytest
from indy import crypto
from indy.error import ErrorCode
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoSignWithInvalidWalletHandle(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey.
        self.steps.add_step("Create verkey")
        my_verkey = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Use 'crypto.crypto_sign' to sign with invalid wallet handle
        # and verify that user cannot sign.
        self.steps.add_step("Use 'crypto.crypto_sign' to sign with invalid "
                            "wallet handle and verify that user cannot sign")
        message = "Test crypto".encode()
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps, crypto.crypto_sign,
                                               self.wallet_handle + 1,
                                               my_verkey, message,
                                               expected_code=error_code)
