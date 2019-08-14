"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that user can start a replacing key process with valid seed.
"""

import pytest
import json

from indy import did
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base\
    import DidTestBase


class TestReplaceKeysStartWithValidSeed(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Prepare new verkey with valid seed.
        self.steps.add_step("Prepare new verkey with valid seed")
        new_verkey = await utils.perform(
            self.steps, did.replace_keys_start, self.wallet_handle, my_did,
            json.dumps({"seed": constant.seed_my1}))

        # 5. Check new verkey.
        self.steps.add_step("Verify that new verkey is correspond with seed")
        error_msg = "New verkey is no correspond with seed"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: new_verkey == constant.verkey_my1)
