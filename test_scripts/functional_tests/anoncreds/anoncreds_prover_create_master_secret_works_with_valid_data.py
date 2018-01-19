"""
Created on Dec 18, 2017

@author: nhan.nguyen
"""

from indy import anoncreds
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverCreateMasterSecret(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 4. Create another master secret with the same secret name and verify
        # that master secret cannot be created because of duplicating name.
        self.steps.add_step("Create another master secret with the same secret"
                            " name and verify that master secret cannot be "
                            "created because of duplicating name")
        error_code = ErrorCode.AnoncredsMasterSecretDuplicateNameError
        await utils.perform_with_expected_code(
            self.steps, anoncreds.prover_create_master_secret,
            self.wallet_handle, constant.secret_name, expected_code=error_code)


if __name__ == '__main__':
    TestProverCreateMasterSecret().execute_scenario()
