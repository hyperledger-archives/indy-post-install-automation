"""
Created on Dec 13, 2017

@author: nhan.nguyen

Verify that user cannot create and store 'my_did' with invalid crypto type.
"""

import pytest
import json

from indy import did
from indy.error import ErrorCode
from utilities import utils
from utilities import common, constant
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestCreateDidWithInvalidCryptoType(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did with an invalid crypto type and verify that
        # cannot create did with invalid crypto type.
        self.steps.add_step("Create did with an invalid crypto "
                            "type and verify that cannot create "
                            "did with invalid crypto type.")

        did_json = json.dumps({"seed": constant.seed_my1,
                               "crypto_type": "invalidType"})
        error_code = ErrorCode.UnknownCryptoTypeError
        await utils.perform_with_expected_code(self.steps,
                                               did.create_and_store_my_did,
                                               self.wallet_handle, did_json,
                                               expected_code=error_code)
