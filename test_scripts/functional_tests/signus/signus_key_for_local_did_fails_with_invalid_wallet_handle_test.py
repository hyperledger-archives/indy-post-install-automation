"""
Created on Jan 13, 2018

@author: nhan.nguyen

Verify that user cannot get verkey in local with invalid wallet handle.
"""

import pytest
from indy import signus
from indy.error import ErrorCode
from utilities import utils
from utilities import common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetKeyForLocalDidWithInvalidWalletHandle(SignusTestBase):
    @pytest.mark.asyncio
    async def test(self):
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

        # 4. Get local verkey with invalid wallet handle and
        # verify that verkey cannot be gotten.
        self.steps.add_step("Get local verkey with invalid wallet handle and "
                            "verify that verkey cannot be gotten")
        err_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               signus.key_for_local_did,
                                               self.wallet_handle + 1,
                                               my_did, expected_code=err_code)
