"""
Created on Jan 2, 2018

@author: nhan.nguyen

Verify that an anonymous encrypted message
cannot be decrypted with verkey does not exist in wallet.
"""

import pytest
from indy import crypto
from indy.error import ErrorCode
from utilities import common, utils, constant
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoBoxSealOpenWithUnknownVerkey(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create sealed crypto box.
        self.steps.add_step("Create sealed crypto box")
        msg = "Test crypto".encode()
        encrypted_msg = await utils.perform(self.steps,
                                            crypto.crypto_box_seal,
                                            constant.verkey_my1, msg)

        # 4. Open sealed crypto box with unknown verkey and
        # verify that sealed crypto box cannot be opened.
        self.steps.add_step("Open sealed crypto box with unknown verkey and "
                            "verify that sealed crypto box cannot be opened")
        error_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               crypto.crypto_box_seal_open,
                                               self.wallet_handle,
                                               constant.verkey_my1,
                                               encrypted_msg,
                                               expected_code=error_code)
