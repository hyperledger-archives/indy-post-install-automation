"""
Created on Dec 21, 2017

@author: khoi.ngo

Implementing test case GetClaimRequest with valid value.
"""
import json

from indy import did, ledger
import pytest

from utilities import common
from utilities.constant import seed_default_trustee, signature_type, \
    get_claim_response, json_template
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestGetClaimRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await perform(
                                    self.steps, common.prepare_pool_and_wallet,
                                    self.pool_name, self.wallet_name,
                                    self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(
                                    self.steps,
                                    did.create_and_store_my_did,
                                    self.wallet_handle,
                                    json.dumps({"seed": seed_default_trustee}))

        # 3. prepare data to build claim request
        self.steps.add_step("build claim request")
        ref = 1
        data = '"primary":{"n":"1","s":"2","rms":"3",' \
               '"r":{"name":"1"}, "rctxt":"1","z":"1"}'
        data_request = '{' + data + '}'
        claim_req = await perform(
                                self.steps, ledger.build_claim_def_txn,
                                submitter_did, ref,
                                signature_type, data_request)

        # 4. send claim request
        self.steps.add_step("send claim request")
        await perform(self.steps, ledger.sign_and_submit_request,
                      self.pool_handle, self.wallet_handle,
                      submitter_did, claim_req)

        # 5. build GET_CLAIM request
        self.steps.add_step("build get_claim request")
        # origin = "origin"
        claim_req = json.loads(await perform(
                                self.steps, ledger.build_get_claim_def_txn,
                                submitter_did, ref,
                                signature_type, submitter_did))

        # 6. Verify json get_claim request is correct.
        self.steps.add_step("Verify json get_claim request is correct.")
        get_claim_op = get_claim_response.format("108", ref,
                                                 signature_type, submitter_did)
        expected_response = json_template(submitter_did, get_claim_op)
        verify_json(self.steps, expected_response, claim_req)
