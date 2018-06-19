"""
Created on Dec 28, 2017

@author: khoi.ngo

Verify that user cannot create verkey with invalid seed.
"""

import pytest
import json

from indy import crypto

from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase
from utilities import common, utils


class TestCryptoCreateKeyWithInvalidSeed(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create verkey with invalid seed. Expected error = 113
        self.steps.add_step("Create verkey with invalid seed")
        invalid_seed = "INVALID_SEED"
        await utils.perform_with_expected_code(
                                         self.steps, crypto.create_key,
                                         self.wallet_handle,
                                         json.dumps({"seed": invalid_seed}),
                                         expected_code=113)
