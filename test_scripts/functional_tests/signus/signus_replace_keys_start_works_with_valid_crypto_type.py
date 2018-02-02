"""
Created on Dec 22, 2017

@author: nhan.nguyen
"""
import base58
import json

from indy import signus
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base\
    import SignusTestBase


class TestReplaceKeysStartWithValidCryptoType(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Prepare new verkey with valid crypto type.
        self.steps.add_step("Prepare new verkey with valid crypto type")
        new_verkey = await utils.perform(
            self.steps, signus.replace_keys_start, self.wallet_handle, my_did,
            json.dumps({"crypto_type": constant.crypto_type}))

        # 5. Check format of new verkey.
        self.steps.add_step("Check format of new verkey")
        error_msg = "Format of new verkey is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(base58.b58decode(new_verkey)) ==
                    constant.decoded_verkey_length)

        # 6. Verify that new verkey is different from old verkey.
        self.steps.add_step("Verify that new verkey is "
                            "different form old verkey")
        error_msg = "New verkey is the same with old verkey"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: new_verkey != my_verkey)


if __name__ == "__main__":
    TestReplaceKeysStartWithValidCryptoType().execute_scenario()
