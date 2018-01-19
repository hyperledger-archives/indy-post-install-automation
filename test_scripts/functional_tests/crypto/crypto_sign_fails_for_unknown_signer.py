"""
Created on Dec 27, 2017

@author: nhan.nguyen
"""

from indy import crypto
from indy.error import ErrorCode
from utilities import common, utils, constant
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class CryptoSignWithUnknownVerkey(CryptoTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Use 'crypto.crypto_sign' to sign with unknown verkey and
        # verify that user cannot sign.
        self.steps.add_step("Use 'crypto.crypto_sign' to sign with "
                            "unknown verkey and verify that user cannot sign")
        error_code = ErrorCode.WalletNotFoundError
        message = "Test crypto".encode()
        await utils.perform_with_expected_code(self.steps, crypto.crypto_sign,
                                               self.wallet_handle,
                                               constant.verkey_my1, message,
                                               expected_code=error_code)


if __name__ == "__main__":
    CryptoSignWithUnknownVerkey().execute_scenario()
