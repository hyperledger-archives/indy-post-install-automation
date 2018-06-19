"""
Created on Dec 15, 2017

@author: nhan.nguyen
Verify that user cannot create and store a claim definition with invalid
wallet handle.
"""

import json

from indy import anoncreds, did, ledger
from indy.error import ErrorCode
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateAndStoreClaimDefWithInvalidWalletHandle\
            (AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create and open pool.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, self.pool_genesis_txn_file)

        # 2. Create and open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name, credentials=self.wallet_credentials)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, issuer_vk) = await utils.perform(self.steps,
                                                      did.create_and_store_my_did,
                                                      self.wallet_handle, "{}")

        # 4. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 5. Add issuer to the ledger.
        # self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did, issuer_vk, alias=None, role='TRUSTEE')
        await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 6. Create and store claim definition with invalid wallet handle
        # and verify that a claim definition cannot be created.
        self.steps.add_step("Create and store claim definition with invalid "
                            "wallet handle and verify that a "
                            "claim definition cannot be created.")
        error_code = ErrorCode.WalletInvalidHandle

        schema_id, schema_json = await anoncreds.issuer_create_schema(
            issuer_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema_request = await ledger.build_schema_request(issuer_did, schema_json)
        schema_result = await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer_did, schema_request)
        schema_json = json.loads(schema_json)
        schema_json['seqNo'] = json.loads(schema_result)['result']['txnMetadata']['seqNo']
        schema_json = json.dumps(schema_json)

        await utils.perform_with_expected_code(
            self.steps, anoncreds.issuer_create_and_store_credential_def,
            self.wallet_handle + 1, issuer_did,
            schema_json, constant.tag,
            constant.signature_type, constant.config_false, expected_code=error_code)
