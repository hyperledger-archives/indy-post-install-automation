"""
Created on Dec 21, 2017

@author: khoi.ngo

Implementing test case GetTxnRequest with valid value.
"""
import json

from indy import did, ledger, pool
import pytest

from utilities import common, utils
from utilities.constant import seed_default_trustee, json_template
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestGetTxnRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await perform(
                                    self.steps, common.prepare_pool_and_wallet,
                                    self.pool_name, self.wallet_name, self.wallet_credentials,
                                    self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DID")
        (submitter_did, _) = await perform(
                                    self.steps,
                                    did.create_and_store_my_did,
                                    self.wallet_handle,
                                    json.dumps({"seed": seed_default_trustee}))

        # 3. build get_txn request
        self.steps.add_step("build get_txn request")
        data = 1
        get_txn_req = json.loads(await perform(self.steps,
                                               ledger.build_get_txn_request,
                                               submitter_did, None, data))

        # 4. verify json response
        self.steps.add_step("Verify json get_txn request is correct.")
        err_msg = "Invalid request type"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: get_txn_req['operation']['type'] == '3')
