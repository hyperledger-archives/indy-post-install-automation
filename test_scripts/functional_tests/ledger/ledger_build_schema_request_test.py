"""
Created on Dec 12, 2017

@author: khoi.ngo

Implementing test case SchemaRequest with valid value.
"""
import json

from indy import did, ledger, pool, anoncreds
import pytest

from utilities import common, constant, utils
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class TestSchemaRequest(TestScenarioBase):

    @pytest.mark.asyncio
    async def test(self):
        await  pool.set_protocol_version(2)

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps, common.prepare_pool_and_wallet,
                          self.pool_name, self.wallet_name, self.wallet_credentials,
                          self.pool_genesis_txn_file)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        issuer_did, issuer_vk = await utils.perform(self.steps,
                                                    did.create_and_store_my_did,
                                                    self.wallet_handle, "{}")

        # 4. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 5. Add issuer to the ledger.
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did, issuer_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 7. Build and send SCHEMA request.
        self.steps.add_step("Build SCHEMA")
        schema_id, schema_json = await anoncreds.issuer_create_schema(
            issuer_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema_request = json.loads(await utils.perform(self.steps, ledger.build_schema_request,
                                                        issuer_did, schema_json))

        # 4. Verifying build schema successfully by checking data response
        self.steps.add_step(
            "Verifying build schema successfully by checking data response")
        err_msg = "Invalid request type"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: schema_request['operation']['type'] == '101')
