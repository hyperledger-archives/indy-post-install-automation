"""
Created on Dec 19, 2017

@author: nhan.nguyen
Verify that user cannot create a master secret with invalid wallet handle.
"""

from indy import anoncreds
from indy.error import ErrorCode
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverCreateMasterSecretWithInvalidWalletHandle(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Create master secret with invalid wallet handle and
        # verify that master secret cannot be created.
        self.steps.add_step("Create master secret with invalid wallet handle"
                            " and verify that master secret cannot be created")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(
            self.steps, anoncreds.prover_create_master_secret,
            self.wallet_handle + 1, constant.secret_name,
            expected_code=error_code)
