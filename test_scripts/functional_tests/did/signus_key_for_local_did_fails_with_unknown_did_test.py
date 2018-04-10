"""
Created on Jan 13, 2018

@author: nhan.nguyen

Verify that user cannot get verkey in local of an unknown did.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestGetKeyForLocalDidWithUnknownDid(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
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
                                               did.key_for_local_did,
                                               self.wallet_handle,
                                               constant.did_my1,
                                               expected_code=err_code)
