"""
Created on Dec 11, 2017

@author: khoi.ngo

Implementing test case SignAndSubmitRequest with valid value.
"""
import json

from indy import signus, ledger

from utilities import common, constant
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class SignAndSubmitRequest(TestScenarioBase):
    async def execute_test_steps(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DID")
        (submitter_did, _) = \
            await perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": constant.seed_default_trustee}))

        # 3. Create and store target did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create target")
        (target_did, _) = await perform(
                                        self.steps,
                                        signus.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 4. build nym request
        # 5. sign and submit request
        self.steps.add_step("Prepare and send NYM transaction")
        await perform(self.steps, common.build_and_send_nym_request,
                      self.pool_handle,
                      self.wallet_handle, submitter_did, target_did, None,
                      None, None)

        # 6. build get nym request
        # 7. submit request
        self.steps.add_step("Prepare and send GET_NYM request")
        get_nym_req = await perform(self.steps, ledger.build_get_nym_request,
                                    submitter_did, target_did)
        nym_response = await perform(self.steps, ledger.submit_request,
                                     self.pool_handle, get_nym_req)

        # 8. Verify GET_NYM request
        self.steps.add_step("Verify GET_NYM request")
        response = json.loads(nym_response)
        did_response = response["result"]["dest"]
        if did_response == target_did:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            message = ("Failed. Expected did is [%s] but actual did is [%s]"
                       % (target_did, did_response))
            self.steps.get_last_step().set_status(Status.FAILED, message)


if __name__ == '__main__':
    SignAndSubmitRequest().execute_scenario()
