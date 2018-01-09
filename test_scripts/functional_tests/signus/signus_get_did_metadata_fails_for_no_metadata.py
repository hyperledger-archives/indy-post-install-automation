"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetMetadataForNoMetadata(SignusTestBase):
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

        # 4. Get metadata of "my_did" and
        # verify that metadata cannot be gotten.
        self.steps.add_step("Get metadata of 'my_did' and "
                            "verify that metadata cannot be gotten")
        error_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               signus.get_did_metadata,
                                               self.wallet_handle, my_did,
                                               expected_code=error_code)


if __name__ == "__main__":
    TestGetMetadataForNoMetadata().execute_scenario()
