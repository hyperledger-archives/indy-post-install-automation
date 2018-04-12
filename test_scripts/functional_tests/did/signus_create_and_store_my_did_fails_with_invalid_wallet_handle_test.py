"""
Created on Dec 13, 2017

@author: nhan.nguyen

Verify that user cannot create and store 'my_did' with invalid wallet handle.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import common
from utilities import utils
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestCreateDidWithInvalidWalletHandle(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verify that cannot create did
        # with invalid wallet handle.
        self.steps.add_step("Create did and verify that cannot create "
                            "did with invalid wallet handle")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               did.create_and_store_my_did,
                                               self.wallet_handle + 1, "{}",
                                               expected_code=error_code)
