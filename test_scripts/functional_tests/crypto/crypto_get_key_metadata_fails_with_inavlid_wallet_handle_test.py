"""
Created on Jan 2, 2018

@author: nhan.nguyen

Verify that user cannot get metadata of verkey with invalid wallet handle.
"""

import pytest
from indy import crypto
from indy.error import ErrorCode
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoGetKeyMetadataWithInvalidWalletHandle(CryptoTestBase):
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

        # 4. Set metadata for created verkey.
        self.steps.add_step("Set metadata for created verkey")
        metadata = "Test crypto"
        await utils.perform(self.steps, crypto.set_key_metadata,
                            self.wallet_handle, my_verkey, metadata)

        # 5. Get metadata of created verkey with invalid wallet handle and
        # verify that metadata cannot be gotten.
        self.steps.add_step("Get metadata of created verkey with "
                            "invalid wallet handle and verify that "
                            "metadata cannot be gotten")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               crypto.get_key_metadata,
                                               self.wallet_handle + 1,
                                               my_verkey,
                                               expected_code=error_code)
