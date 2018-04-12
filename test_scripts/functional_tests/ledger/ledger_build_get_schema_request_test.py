"""
Created on Dec 12, 2017

@author: khoi.ngo

Implementing test case GetSchemaRequest with valid value.
"""
import json

from indy import did, ledger
import pytest

from utilities import common
from utilities.constant import json_template, schema_response, \
    seed_default_trustee
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json, generate_random_string


class TestGetSchemaRequest(TestScenarioBase):
    @pytest.mark.asyncio
    async def test_valid_data(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create DID")
        (submitter_did, _) = \
            await perform(self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": seed_default_trustee}))
        (target_did, _) = await perform(self.steps,
                                        did.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 3. Prepare data to check and build get schema request
        self.steps.add_step("build get schema request")
        name = generate_random_string(size=4)
        version = "1.1.1"
        data = ('{"name":"%s", "version":"%s"}' % (name, version))
        get_schema_req = json.loads(
            await perform(self.steps, ledger.build_get_schema_request,
                          submitter_did,
                          target_did, data))

        # 4. Verify json get schema request is correct.
        self.steps.add_step("Verify json get schema request is correct.")
        schema_operation = schema_response.format("107", target_did,
                                                  data)
        expected_response = json_template(submitter_did, schema_operation)
        verify_json(self.steps, expected_response, get_schema_req)
