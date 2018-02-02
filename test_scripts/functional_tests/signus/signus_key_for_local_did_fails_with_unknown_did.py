"""
Created on Jan 13, 2018

@author: nhan.nguyen
"""
from indy import signus
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetKeyForLocalDidWithUnknownDid(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Get local verkey with unknown did and
        # verify that verkey cannot be gotten.
        self.steps.add_step("Get local verkey with unknown did and "
                            "verify that verkey cannot be gotten")
        err_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               signus.key_for_local_did,
                                               self.wallet_handle,
                                               constant.did_my1,
                                               expected_code=err_code)


if __name__ == "__main__":
    TestGetKeyForLocalDidWithUnknownDid().execute_scenario()
