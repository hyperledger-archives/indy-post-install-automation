"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get metadata of did with invalid wallet handle.
"""

import pytest
from indy import signus
from indy.error import ErrorCode
from utilities import common, utils
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetMetadataWithInvalidWalletHandle(SignusTestBase):
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
        (my_did, _) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Set metadata for 'my_did'.
        self.steps.add_step("Set metadata for 'my_did'")
        metadata = "Test signus"
        await utils.perform(self.steps, signus.set_did_metadata,
                            self.wallet_handle, my_did, metadata,
                            ignore_exception=False)

        # 5. Get metadata with invalid wallet handle and
        # verify that metadata cannot be gotten.
        self.steps.add_step("Get metadata with invalid wallet handle and "
                            "verify that metadata cannot be gotten.")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               signus.get_did_metadata,
                                               self.wallet_handle + 1, my_did,
                                               expected_code=error_code)
