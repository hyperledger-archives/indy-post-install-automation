"""
Created on Dec 27, 2017

@author: nhan.nguyen
"""

from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class CryptoSignWithValidData(CryptoTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey with seed my1.
        self.steps.add_step("Create verkey with seed my1")
        my_verkey = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Use 'crypto.crypto_sign' to sign.
        self.steps.add_step("Use 'crypto.crypto_sign' to sign")
        message = "Test crypto".encode()
        signature = await utils.perform(self.steps, crypto.crypto_sign,
                                        self.wallet_handle, my_verkey,
                                        message)

        # 5. Verify signed signature.
        self.steps.add_step("Verify signed signature")
        result = await utils.perform(self.steps, crypto.crypto_verify,
                                     my_verkey, message, signature)

        error_msg = "'crypto.crypto_verify' return False instead of True"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: result is True)


if __name__ == "__main__":
    CryptoSignWithValidData().execute_scenario()
