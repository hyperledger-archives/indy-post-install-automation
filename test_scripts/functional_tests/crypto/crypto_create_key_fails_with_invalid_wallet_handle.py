"""
Created on Dec 28, 2017

@author: khoi.ngo

Implementing test case CryptoCreateKey with invalid handle.
"""

from indy import crypto

from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase
from utilities import common, utils


class CryptoCreateKeyWithInvalidWalletHandle(CryptoTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create verkey with invalid wallet handle. Expected error = 200
        self.steps.add_step("Create verkey with invalid wallet handle")
        await utils.perform_with_expected_code(
                                         self.steps, crypto.create_key,
                                         self.wallet_handle + 9999, "{}",
                                         expected_code=200)


if __name__ == '__main__':
    CryptoCreateKeyWithInvalidWalletHandle().execute_scenario()
