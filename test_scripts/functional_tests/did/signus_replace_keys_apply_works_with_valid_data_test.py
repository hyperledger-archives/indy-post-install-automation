"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that user can apply a replacing key process with valid data.
"""

import pytest
from indy import did
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestReplaceKeysApplyWithValidData(DidTestBase):
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

        # 4. Prepare new verkey with empty json.
        self.steps.add_step("Prepare new verkey with empty json")
        new_verkey = await utils.perform(self.steps, did.replace_keys_start,
                                         self.wallet_handle, my_did, "{}")

        # 5. Replace old verkey.
        self.steps.add_step("Replace old verkey")
        await utils.perform(self.steps, did.replace_keys_apply,
                            self.wallet_handle, my_did)

        # 6. Get verkey of 'my_did'.
        self.steps.add_step("Get verkey of 'my_did'")
        updated_verkey = await utils.perform(self.steps, did.key_for_did,
                                             -1, self.wallet_handle, my_did)

        # 7. Check updated verkey.
        self.steps.add_step("Check updated verkey")
        error_msg = "Updated verkey is different from verkey " \
                    "that returned by 'did.replace_keys_start'"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: new_verkey == updated_verkey)
