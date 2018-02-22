"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user can replace old endpoint with another endpoint for did.
"""

import pytest
from indy import signus
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestReplaceEndPointForDidInWallet(SignusTestBase):
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
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Set endpoint for 'my_did' and
        # verify that there is no exception raised.
        self.steps.add_step("Set endpoint for 'my_did' and verify that "
                            "there is no exception raised")
        await utils.perform(self.steps, signus.set_endpoint_for_did,
                            self.wallet_handle, my_did, constant.endpoint,
                            my_verkey)

        # 5. Get endpoint of 'my_did'.
        self.steps.add_step("Get end point of 'my_did'")
        (old_endpoint, old_verkey) = await utils.perform(
            self.steps, signus.get_endpoint_for_did, self.wallet_handle,
            -1, my_did)

        # 6. Check old verkey.
        self.steps.add_step("Check old verkey")
        error_msg = "Old verkey mismatches with verkey that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: old_verkey == my_verkey)

        # 7. Check old endpoint.
        self.steps.add_step("Check old endpoint")
        error_msg = "Old endpoint mismatches with endpoint that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: old_endpoint == constant.endpoint)

        # 8. Set endpoint for 'my_did' to replace old endpoint and
        # verify that there is no exception raised.
        self.steps.add_step("Set endpoint for 'my_did' to replace old endpoint"
                            " and verify that there is no exception raised.")
        new_endpoint = "100.0.0.0:9700"
        new_verkey = constant.verkey_my1
        await utils.perform(self.steps, signus.set_endpoint_for_did,
                            self.wallet_handle, my_did, new_endpoint,
                            new_verkey, ignore_exception=False)

        # 9. Get endpoint of 'my_did'.
        self.steps.add_step("Get end point of 'my_did'")
        (updated_endpoint, updated_verkey) = await utils.perform(
            self.steps, signus.get_endpoint_for_did, self.wallet_handle,
            -1, my_did)

        # 10. Check updated verkey.
        self.steps.add_step("Check updated verkey")
        error_msg = "Updated verkey mismatches with new verkey that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: updated_verkey == new_verkey)

        # 11. Check updated endpoint.
        self.steps.add_step("Check updated endpoint")
        error_msg = "Updated endpoint mismatches with new endpoint that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: updated_endpoint == new_endpoint)
