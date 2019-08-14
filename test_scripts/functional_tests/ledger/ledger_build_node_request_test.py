"""
Created on Dec 26, 2017

@author: khoi.ngo

Implementing test case BuildNodeRequest with valid value.
"""
import json

from indy import did, ledger, pool
import pytest

from utilities import common, constant
from utilities.constant import node_request, json_template
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestBuildNodeRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name, self.wallet_credentials,
                          self.pool_genesis_txn_file)

        # 2. Create and store submitter did
        self.steps.add_step("Create Submitter")
        (submitter_did, _) = \
            await perform(self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": constant.seed_default_trustee}))

        # 3. Create and store target did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create target")
        (target_did, _) = \
            await perform(self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": seed_trustee_2}))

        # 4. build node request
        self.steps.add_step("build Node request")
        data_request = '{{"node_ip":"{}","node_port":{},"client_ip":"{}",' \
            '"client_port":{},"alias":"{}","services":["VALIDATOR"],' \
            '"blskey":"CnEDk9HrMnmiHXEV1WFgbVCRteYnPqsJwrTdcZaNhFVW"}}'
        ip = "10.20.30.206"
        port = "9709"
        alias = "test_case_build_node_request"
        data = data_request.format(ip, port, ip, port, alias)
        response = json.loads(await perform(
                                self.steps, ledger.build_node_request,
                                submitter_did, target_did, data))

        # 5. Verifying json response correctly.
        self.steps.add_step("Verifying json response correctly")
        node_op = node_request.format("0", target_did, data)
        expected_response = json_template(submitter_did, node_op)

        verify_json(self.steps, expected_response, response)
