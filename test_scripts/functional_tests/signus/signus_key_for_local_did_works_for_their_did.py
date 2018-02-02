"""
Created on Jan 13, 2018

@author: nhan.nguyen
"""

import json
from indy import signus
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetKeyForLocalDidForTheirDid(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Store 'their_did' and 'their_verkey' into wallet.
        self.steps.add_step("Store 'their_did' and 'their_verkey' into wallet")
        their_did, their_verkey = constant.did_my2, constant.verkey_my2
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did,
                                        "verkey": their_verkey}))

        # 4. Get local verkey of 'their_did' from wallet
        # and store it into 'returned_verkey'.
        self.steps.add_step("Get local verkey of 'my_did' from wallet and "
                            "store it into 'returned_verkey'")
        returned_verkey = await utils.perform(self.steps,
                                              signus.key_for_local_did,
                                              self.wallet_handle,
                                              their_did)

        # 5. Check 'returned_verkey'.
        self.steps.add_step("Check 'returned_verkey'")
        err_msd = "Returned verkey mismatches with stored verkey"
        utils.check(self.steps, error_message=err_msd,
                    condition=lambda: returned_verkey == their_verkey)


if __name__ == "__main__":
    TestGetKeyForLocalDidForTheirDid().execute_scenario()
