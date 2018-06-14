"""
Created on Dec 15, 2017

@author: nhan.nguyen
Verify that user can use an issuer to create and store a claim definition
with valid data.
"""

import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateAndStoreClaimDefWithValidData(AnoncredsTestBase):

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
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did, issuer_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 6. Create and store claim definition and store
        # returned result as 'claim_def'.
        self.steps.add_step("Create and store claim definition and "
                            "store returned result as 'claim_def'")

        schema_id, schema_json = await anoncreds.issuer_create_schema(
            issuer_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema_request = await ledger.build_schema_request(issuer_did, schema_json)
        schema_result = await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer_did, schema_request)
        schema_json = json.loads(schema_json)
        schema_json['seqNo'] = json.loads(schema_result)['result']['txnMetadata']['seqNo']
        schema_json = json.dumps(schema_json)

        cred_def_id, cred_def_json = await utils.perform(
                                                self.steps,
                                                anoncreds.issuer_create_and_store_credential_def,
                                                self.wallet_handle, issuer_did,
                                                schema_json, constant.tag,
                                                constant.signature_type, constant.config_true)

        claim_def_primary = json.loads(cred_def_json)['value']['primary']

        # 5. Check len(claim_def['data']['primary']['r']).
        self.steps.add_step("Check len(claim_def['data']['primary']['r'])")
        error_message = "Length of claim_def['data']['primary']['r'] " \
                        "is not equal with 4"
        utils.check(self.steps, error_message,
                    condition=lambda: len(claim_def_primary['r']) == 4)

        # 6. Check claim_def['data']['primary']['n'].
        self.__check_a_field_is_not_empty(claim_def_primary, 'n')

        # 7. Check claim_def['data']['primary']['s'].
        self.__check_a_field_is_not_empty(claim_def_primary, 's')

        # 8. Check claim_def['data']['primary']['rms'].
        self.__check_a_field_is_not_empty(claim_def_primary, 'rms')

        # 9. Check claim_def['data']['primary']['z'].
        self.__check_a_field_is_not_empty(claim_def_primary, "z")

        # 10. Check claim_def['data']['primary']['rctxt'].
        self.__check_a_field_is_not_empty(claim_def_primary, "rctxt")

    def __check_a_field_is_not_empty(self, claim_json_def_primary, key: str):
        self.steps.add_step(
            "Check claim_def['data']['primary']['{}']".format(key))

        error_message = "Claim_def['data']['primary']['{}'] " \
                        "is empty".format(key)

        utils.check(self.steps, error_message,
                    condition=lambda: len(claim_json_def_primary[key]) > 0)
