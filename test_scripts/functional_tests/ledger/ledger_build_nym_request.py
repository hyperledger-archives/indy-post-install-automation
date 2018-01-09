"""
Created on Dec 12, 2017

@author: khoi.ngo

Implementing test case BuildNymRequest with valid value.
"""
import json

from indy import signus, ledger

from utilities import common, constant
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json
from utilities.constant import message, json_template


class BuildNymRequest(TestScenarioBase):
    async def execute_test_steps(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create submitter")
        (submitter_did, _) = \
            await perform(self.steps,
                          signus.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": constant.seed_default_trustee}))

        # 3. Create and store target did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create target")
        (target_did, target_verkey) = await perform(
                                        self.steps,
                                        signus.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 4. build nym request
        self.steps.add_step("build NYM request")
        nym_req_txn = json.loads(
            await perform(self.steps, ledger.build_nym_request, submitter_did,
                          target_did,
                          target_verkey, None, None))

        # 5. Verifying json nym request response correctly.
        self.steps.add_step("Verifying nym request")
        message_op = message.format("1", target_did, target_verkey)
        expected_response = json_template(submitter_did, message_op)
        verify_json(self.steps, expected_response, nym_req_txn)


if __name__ == '__main__':
    BuildNymRequest().execute_scenario()
