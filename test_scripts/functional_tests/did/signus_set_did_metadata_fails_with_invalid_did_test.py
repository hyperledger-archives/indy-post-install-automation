"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot set metadata for invalid did.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestSetMetadataWithInvalidDid(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Set metadata for invalid did and
        # verify that metadata cannot be set.
        self.steps.add_step("Set metadata for invalid did and "
                            "verify that metadata cannot be set")
        metadata = "Test did"
        invalid_did = "invalidDid"
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(self.steps,
                                               did.set_did_metadata,
                                               self.wallet_handle, invalid_did,
                                               metadata,
                                               expected_code=error_code)
