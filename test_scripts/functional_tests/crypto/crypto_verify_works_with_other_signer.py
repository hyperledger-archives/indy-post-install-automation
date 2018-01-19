"""
Created on Jan 6, 2018

@author: khoi.ngo
"""

import json

from indy import crypto

from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase
from utilities import common, utils, constant


class CryptoSignWithOtherSigner(CryptoTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey with seed my1.
        self.steps.add_step("Create verkey with seed my1")
        my_verkey = await utils.perform(
                                     self.steps, crypto.create_key,
                                     self.wallet_handle,
                                     json.dumps({"seed": constant.seed_my1}))

        # 4. Create the other verkey with empty json.
        self.steps.add_step("Create the other verkey")
        other_verkey = await utils.perform(self.steps, crypto.create_key,
                                           self.wallet_handle, "{}")

        # 5. Crypto sign the message.
        self.steps.add_step("Crypto sign the message")
        message = "Test crypto".encode()
        signature = await utils.perform(self.steps, crypto.crypto_sign,
                                        self.wallet_handle, my_verkey,
                                        message)

        # 5. Verify signed signature with other signer.
        self.steps.add_step("Verify signed signature with other signer")
        result = await utils.perform(self.steps, crypto.crypto_verify,
                                     other_verkey, message,
                                     signature)

        error_msg = "Return True although we use other verkey"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: result is False)


if __name__ == "__main__":
    CryptoSignWithOtherSigner().execute_scenario()
