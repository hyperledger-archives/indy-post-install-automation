"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestSetMetadataForDidWithnInvalidWalletHandle(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, _) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Set metadata for 'my_did' with invalid wallet handle and
        # verify that metadata cannot be set
        self.steps.add_step("Set metadata for 'my_did' with invalid "
                            "wallet handle and verify that "
                            "metadata cannot be set")
        metadata = "Test signus"
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               signus.set_did_metadata,
                                               self.wallet_handle + 1, my_did,
                                               metadata,
                                               expected_code=error_code)


if __name__ == "__main__":
    TestSetMetadataForDidWithnInvalidWalletHandle().execute_scenario()
