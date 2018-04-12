"""
Created on Dec 19, 2017

@author: khoi.ngo

Implementing test case ClaimRequest with valid value.
"""
import json

from indy import did, ledger
import pytest

from utilities import common
from utilities.constant import seed_default_trustee, signature_type,\
    claim_response, json_template
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestClaimRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await \
            perform(self.steps, common.prepare_pool_and_wallet, self.pool_name,
                    self.wallet_name, self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            json.dumps({"seed": seed_default_trustee}))

        # 3. prepare data to build claim request
        self.steps.add_step("build claim request")
        schema_seq_no = 1
        data = '"primary":{"n":"1","s":"2","rms":"3",' \
               '"r":{"name":"1"}, "rctxt":"1","z":"1"}'
        data_request = '{' + data + '}'
        response = json.loads(await perform(
                                self.steps, ledger.build_claim_def_txn,
                                submitter_did, schema_seq_no,
                                signature_type, data_request))

        # 4. Verify json claim request is correct.
        self.steps.add_step("Verify json claim request is correct.")
        data_response = '{"revocation": {},' + data + '}'
        claim_op = claim_response.format(data_response, "102", signature_type)
        expected_response = json_template(submitter_did, claim_op)
        verify_json(self.steps, expected_response, response)
