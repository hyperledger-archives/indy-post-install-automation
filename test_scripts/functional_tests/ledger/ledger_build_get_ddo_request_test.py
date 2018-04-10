"""
Created on Dec 27, 2017

@author: khoi.ngo

Implementing test case BuildDDORequest with valid value.
"""
import json

from indy import did, ledger
import pytest

from utilities import common
from utilities.constant import json_template, operation_fields, \
    seed_default_trustee
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestBuildDDORequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store submitter did
        self.steps.add_step("Create Submitter")
        (submitter_did, _) = await perform(
                          self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": seed_default_trustee}))

        # 3. Create and store target did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create target")
        (target_did, target_verkey) = await perform(
                                        self.steps,
                                        did.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 4. build and send nym request
        self.steps.add_step("Prepare and send NYM transaction")
        await perform(self.steps, common.build_and_send_nym_request,
                      self.pool_handle, self.wallet_handle,
                      submitter_did, target_did,
                      target_verkey, None, None)

        # 5. build GET_DDO request
        self.steps.add_step("Build ddo request")
        get_ddo_req = json.loads(await perform(
                                self.steps, ledger.build_get_ddo_request,
                                submitter_did, target_did))

        # 6. Verifying get_nym_request json correctly.
        self.steps.add_step("Verifying get_ddo_request json")
        ddo_operation = operation_fields.format("120", target_did)
        expected_response = json_template(submitter_did, ddo_operation)

        verify_json(self.steps, expected_response, get_ddo_req)
