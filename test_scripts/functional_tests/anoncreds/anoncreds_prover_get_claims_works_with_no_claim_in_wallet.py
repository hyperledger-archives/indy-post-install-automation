"""
Created on Jan 10, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds
from utilities import utils, common
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverGetClaimWithNoClaimInWallet(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Get stored claims in wallet.
        self.steps.add_step("Get stored claims in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, '{}')

        lst_claims = json.loads(lst_claims)

        # 4. Check returned list claims.
        self.steps.add_step("Check returned list claims")
        err_msg = "Returned list claims is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not lst_claims)


if __name__ == '__main__':
    TestProverGetClaimWithNoClaimInWallet().execute_scenario()
