"""
Created on Dec 13, 2017

@author: khoi.ngo

Implementing test case BuildAttribRequest with valid value.
"""
import json

from indy import did, ledger, pool
import pytest

from utilities import common, utils
from utilities.constant import json_template, attrib_response, \
    seed_default_trustee
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestBuildAttribRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await \
            perform(self.steps, common.prepare_pool_and_wallet, self.pool_name,
                    self.wallet_name, self.wallet_credentials, self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            json.dumps({"seed": seed_default_trustee}))

        # 3. build attrib request
        self.steps.add_step("Create DIDs")
        raw = '{"endpoint":{"ha":"127.0.0.1:5555"}}'
        attrib_req = json.loads(await perform(self.steps,
                                              ledger.build_attrib_request,
                                              submitter_did, submitter_did,
                                              None, raw, None))

        # 4. Verifying build_attrib_request json.
        self.steps.add_step("Verifying get_nym_request json")
        err_msg = "Invalid request type"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: attrib_req['operation']['type'] == '100')
