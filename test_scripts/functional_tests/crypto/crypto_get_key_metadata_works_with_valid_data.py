"""
Created on Dec 28, 2017

@author: nhan.nguyen
"""

from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class CryptoGetKeyMetadataWithValidData(CryptoTestBase):
    async def execute_test_steps(self):
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

        # 5. Get metadata of created verkey.
        self.steps.add_step("Get metadata of created verkey")
        returned_metadata = await utils.perform(self.steps,
                                                crypto.get_key_metadata,
                                                self.wallet_handle, my_verkey)

        # 6. Check returned metadata.
        self.steps.add_step("Check returned metadata")
        error_msg = "Returned metadata mismatches with " \
                    "metadata that is used to set before"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_metadata == metadata)


if __name__ == "__main__":
    CryptoGetKeyMetadataWithValidData().execute_scenario()
