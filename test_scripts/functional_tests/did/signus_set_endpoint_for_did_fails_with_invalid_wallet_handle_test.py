"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot set endpoint for did with invalid wallet handle.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestSetEndPointForDidInWalletWithInvalidWalletHandle(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)
        # 3. Create did with empty json.
        self.steps.add_step("Create did with empty json")
        (_did, ver_key) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Set endpoint with invalid wallet handle and
        # verify that endpoint cannot be set.
        self.steps.add_step("Set endpoint with invalid wallet handle and "
                            "verify that endpoint cannot be set")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               did.set_endpoint_for_did,
                                               self.wallet_handle + 1,
                                               _did, constant.endpoint, ver_key,
                                               expected_code=error_code)
