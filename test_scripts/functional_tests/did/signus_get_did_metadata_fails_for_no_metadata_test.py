"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get metadata of did
if this did does not contain any metadata.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestGetMetadataForNoMetadata(DidTestBase):
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
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Get metadata of "my_did" and
        # verify that metadata cannot be gotten.
        self.steps.add_step("Get metadata of 'my_did' and "
                            "verify that metadata cannot be gotten")
        error_code = ErrorCode.WalletNotFoundError
        await utils.perform_with_expected_code(self.steps,
                                               did.get_did_metadata,
                                               self.wallet_handle, my_did,
                                               expected_code=error_code)
