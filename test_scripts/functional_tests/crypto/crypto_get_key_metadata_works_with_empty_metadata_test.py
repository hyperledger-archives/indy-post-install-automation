"""
Created on Dec 28, 2017

@author: nhan.nguyen

Verify that user can get empty metadata of verkey.
"""

import pytest
from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestCryptoGetKeyMetadataWithEmptyMetadata(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create verkey.
        self.steps.add_step("Create verkey")
        my_verkey = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Set empty metadata for created verkey.
        self.steps.add_step("Set emtpy metadata for created verkey")
        metadata = ""
        await utils.perform(self.steps, crypto.set_key_metadata,
                            self.wallet_handle, my_verkey, metadata)

        # 5. Get metadata of created verkey.
        self.steps.add_step("Get metadata of created verkey")
        returned_metadata = await utils.perform(self.steps,
                                                crypto.get_key_metadata,
                                                self.wallet_handle, my_verkey)

        # 6. Check returned metadata.
        self.steps.add_step("Check returned metadata")
        error_msg = "Returned metadata mismatches with " \
                    "metadata that is used to set before"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_metadata == metadata)
