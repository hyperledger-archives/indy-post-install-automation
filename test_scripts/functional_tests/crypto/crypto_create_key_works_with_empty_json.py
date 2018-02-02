"""
Created on Dec 27, 2017

@author: nhan.nguyen
"""

import base58

from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class CryptoCreateVerkeyWithEmptyJson(CryptoTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey with empty json.
        self.steps.add_step("Create verkey with empty json")
        my_verkey = await utils.perform(
            self.steps, crypto.create_key, self.wallet_handle, "{}")

        # 4. Check created verkey.
        self.steps.add_step("Check created verkey")
        error_msg = "Created verkey is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(base58.b58decode(my_verkey)) == 32)


if __name__ == "__main__":
    CryptoCreateVerkeyWithEmptyJson().execute_scenario()
