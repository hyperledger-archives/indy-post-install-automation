"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot set endpoint for an invalid did.
"""

import pytest
from indy import signus
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestSetEndPointForDidInWalletWithInvalidDid(SignusTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Set endpoint with invalid did and
        # verify that endpoint cannot be set.
        self.steps.add_step("Set endpoint with invalid did and "
                            "verify that endpoint cannot be set")
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(self.steps,
                                               signus.set_endpoint_for_did,
                                               self.wallet_handle,
                                               "invalidDid",
                                               constant.endpoint,
                                               constant.verkey_my1,
                                               expected_code=error_code)
