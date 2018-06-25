"""
Created on Dec 11, 2017

@author: khoi.ngo

Implementing test case SubmitRequest with valid value.
"""

import json

from indy import did, ledger, pool
import pytest

from utilities import common
from utilities.constant import message, json_template
from utilities.constant import seed_default_trustee, submit_request,\
    submit_response, JSON_INCORRECT
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class TestSubmitRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.wallet_credentials,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create submitter")
        (submitter_did, _) = \
            await perform(self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": seed_default_trustee}))

        # 3. Create and store target did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create target")
        (target_did, target_verkey) = await perform(
                                        self.steps,
                                        did.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 4. Prepare the request.
        self.steps.add_step("sign the message")
        message_op = message.format("1", target_did, target_verkey)
        message_request = json_template(submitter_did, message_op, False)
        response = await perform(self.steps, ledger.sign_request,
                                 self.wallet_handle, submitter_did,
                                 message_request)

        # get signature
        signed_msg = json.loads(response)
        signature = signed_msg['signature']
        type_request = "105"
        request_json = submit_request.format(1491566332010860,
                                             submitter_did, type_request,
                                             target_did, signature, 2)

        # 5. Submit request
        response = json.loads(
            await perform(self.steps, ledger.submit_request, self.pool_handle,
                          request_json))

        # 6. Verify json response is correct.
        self.steps.add_step("verify json response is correct.")
        expected_response = json.loads(submit_response.format(
                                            submitter_did, target_did,
                                            "", type_request, "REPLY"))
        r1 = response["op"] == expected_response["op"]
        r2 = response["result"]["identifier"] == expected_response["result"][
            "identifier"]
        r3 = response["result"]["dest"] == expected_response["result"]["dest"]
        r4 = response["result"]["type"] == expected_response["result"]["type"]
        if (r1 and r2 and r3 and r4) is True:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            message_fail = JSON_INCORRECT.format("")
            self.steps.get_last_step().set_status(Status.FAILED, message_fail)
