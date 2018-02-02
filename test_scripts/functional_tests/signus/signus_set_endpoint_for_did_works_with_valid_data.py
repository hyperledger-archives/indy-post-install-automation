"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestSetEndPointForDidInWallet(SignusTestBase):
    async def execute_test_steps(self):
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
                            my_verkey, ignore_exception=False)

        # 5. Get end point of 'my_did'.
        self.steps.add_step("Get end point of 'my_did'")
        (returned_endpoint, returned_verkey) = await utils.perform(
            self.steps, signus.get_endpoint_for_did, self.wallet_handle,
            -1, my_did)

        # 6. Check returned verkey.
        self.steps.add_step("Check returned verkey")
        error_msg = "Returned verkey mismatches with verkey that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_verkey == my_verkey)

        # 7. Check returned endpoint.
        self.steps.add_step("Check returned endpoint")
        error_msg = "Returned endpoint mismatches with endpoint that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_endpoint == constant.endpoint)


if __name__ == "__main__":
    TestSetEndPointForDidInWallet().execute_scenario()
