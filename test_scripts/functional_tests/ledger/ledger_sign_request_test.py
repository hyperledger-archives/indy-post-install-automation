"""
Created on Dec 11, 2017

@author: khoi.ngo

Implementing test case SignRequest with valid value.
"""
import json

from indy import did, ledger, pool
import pytest

from utilities import common, constant
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class TestSignRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # Prepare data to test.
        message = json.dumps(
            {
                "reqId": 1496822211362017764,
                "identifier": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
                "operation":
                    {
                        "type": "1",
                        "dest": "VsKV7grR1BUE29mG2Fm2kX",
                        "verkey": "GjZWsBLgZCR18aL468JAT7"
                                  "w9CZRiBnpxUPPgyQxh4voa"
                    }
            })
        expected_signature = "65hzs4nsdQsTUqLCLy2qisbKLfwYKZSWoyh1C6CU59" \
                             "p5pfG3EHQXGAsjW4Qw4QdwkrvjSgQuyv8qyABcXRBznFKW"

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name, self.wallet_credentials,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DID")
        (_did, _) = \
            await perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": constant.seed_default_trustee}))

        # 3. sign request
        self.steps.add_step("sign the request")
        sign_txn = await perform(self.steps, ledger.sign_request,
                                 self.wallet_handle, _did, message)

        # 4. verify the signature is correct.
        self.steps.add_step("verify the signature is correct.")
        signed_msg = json.loads(sign_txn)
        actual_signature = signed_msg['signature']
        if actual_signature == expected_signature:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            message = ("Failed. Expected signature is [%s] "
                       "but actual signature is [%s]"
                       % (expected_signature, actual_signature))
            self.steps.get_last_step().set_status(Status.FAILED, message)
