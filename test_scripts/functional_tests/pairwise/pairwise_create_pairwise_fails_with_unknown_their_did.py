"""
Created on Dec 26, 2017

@author: nhan.nguyen
"""

from indy import signus, pairwise
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestCreatePairwiseWithUnknownTheirDid(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          signus.create_and_store_my_did,
                                          self.wallet_handle, "{}")

        # 4. Create pairwise with unknown 'their_did' and
        # verify that pairwise cannot be created.
        self.steps.add_step("Create pairwise with unknown 'their_did' and "
                            "verify that pairwise cannot be created")
        error_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               pairwise.create_pairwise,
                                               self.wallet_handle,
                                               constant.verkey_my1, my_did,
                                               None, expected_code=error_code)


if __name__ == "__main__":
    TestCreatePairwiseWithUnknownTheirDid().execute_scenario()
