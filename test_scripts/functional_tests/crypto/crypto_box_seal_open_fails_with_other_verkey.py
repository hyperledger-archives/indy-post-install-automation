"""
Created on Jan 2, 2018

@author: nhan.nguyen
"""

from indy import crypto
from indy.error import ErrorCode
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class CryptoBoxSealOpenWithOtherKey(CryptoTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'my_verkey'.
        self.steps.add_step("Create 'my_verkey'")
        my_verkey = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Create other verkey.
        self.steps.add_step("Create other verkey")
        other_verkey = await utils.perform(self.steps, crypto.create_key,
                                           self.wallet_handle, "{}")

        # 4. Create sealed crypto box with 'my_verkey'.
        self.steps.add_step("Create sealed crypto box with 'my_verkey'")
        msg = "Test crypto".encode()
        encrypted_msg = await utils.perform(self.steps,
                                            crypto.crypto_box_seal,
                                            my_verkey, msg)

        # 5. Open sealed crypto box with other verkey and verify
        # that sealed crypto box cannot be opened.
        self.steps.add_step("Open sealed crypto box with other verkey and "
                            "verify that sealed crypto box cannot be opened")
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(self.steps,
                                               crypto.crypto_box_seal_open,
                                               self.wallet_handle,
                                               other_verkey, encrypted_msg,
                                               expected_code=error_code)


if __name__ == "__main__":
    CryptoBoxSealOpenWithOtherKey().execute_scenario()
