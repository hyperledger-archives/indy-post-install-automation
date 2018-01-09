"""
Created on Dec 22, 2017

@author: nhan.nguyen
"""
import json

from indy import signus
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base\
    import SignusTestBase


class TestReplaceKeysStartWithValidSeed(SignusTestBase):
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

        # 4. Prepare new verkey with valid seed.
        self.steps.add_step("Prepare new verkey with valid seed")
        new_verkey = await utils.perform(
            self.steps, signus.replace_keys_start, self.wallet_handle, my_did,
            json.dumps({"seed": constant.seed_my1}))

        # 5. Check new verkey.
        self.steps.add_step("Verify that new verkey is correspond with seed")
        error_msg = "New verkey is no correspond with seed"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: new_verkey == constant.verkey_my1)


if __name__ == "__main__":
    TestReplaceKeysStartWithValidSeed().execute_scenario()
