"""
Created on Jan 13, 2018

@author: nhan.nguyen
"""

from indy import signus
from utilities import utils
from utilities import common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetKeyForLocalDidForMyDid(SignusTestBase):
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

        # 4. Get local verkey of 'my_did' from wallet
        # and store it into 'returned_verkey'.
        self.steps.add_step("Get local verkey of 'my_did' from wallet and "
                            "store it into 'returned_verkey'")
        returned_verkey = await utils.perform(self.steps,
                                              signus.key_for_local_did,
                                              self.wallet_handle,
                                              my_did)

        # 5. Check 'returned_verkey'.
        self.steps.add_step("Check 'returned_verkey'")
        err_msd = "Returned verkey mismatches with stored verkey"
        utils.check(self.steps, error_message=err_msd,
                    condition=lambda: returned_verkey == my_verkey)


if __name__ == "__main__":
    TestGetKeyForLocalDidForMyDid().execute_scenario()
