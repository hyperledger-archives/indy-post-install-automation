"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.signus.signus_test_base\
    import SignusTestBase


class TestKeyForDidWithInvalidWalletHandle(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (did, _) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Get verkey with invalid wallet handle and
        # verify that user cannot get verkey.
        self.steps.add_step("Get verkey with invalid wallet handle and "
                            "verify that user cannot get verkey")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps, signus.key_for_did,
                                               -1, self.wallet_handle + 1,
                                               did, expected_code=error_code)


if __name__ == "__main__":
    TestKeyForDidWithInvalidWalletHandle().execute_scenario()
