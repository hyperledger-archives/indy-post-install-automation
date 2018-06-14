'''
Created on Jan 17, 2018

@author: khoi.ngo
Implementing test case IssuerCreateClaimDefs with create_none_revoc.
'''
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateAndStoreClaimDefsWithCreateNoneRevoc(AnoncredsTestBase):

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

        # 6. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")

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
        print("claim_def: " + str(cred_def_json))
        # 7. Check len(claim_def['value']['primary']['r']).
        self.steps.add_step("len(claim_def['value']['primary']['r'])")
        err_msg = "len(claim_def['value']['primary']['r']) isn't equal 4"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: len(json.loads(cred_def_json)['value']['primary']['r']) == 4)

        # 8. Check claim_def['value']['primary']['n'].
        self.steps.add_step("claim_def['value']['primary']['n']")
        err_msg = "claim_def['value']['primary']['n'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_def_json)['value']['primary']['n'])

        # 9. Check claim_def['value']['primary']['s'].
        self.steps.add_step("claim_def['value']['primary']['s']")
        err_msg = "claim_def['value']['primary']['s'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_def_json)['value']['primary']['s'])

        # 10. Check claim_def['value']['primary']['rms'].
        self.steps.add_step("claim_def['value']['primary']['rms']")
        err_msg = "claim_def['value']['primary']['rms'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_def_json)['value']['primary']['rms'])

        #11. Check claim_def['value']['primary']['z'].
        self.steps.add_step("claim_def['value']['primary']['z']")
        err_msg = "claim_def['value']['primary']['z'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_def_json)['value']['primary']['z'])

        # 12. Check claim_def['value']['primary']['rctxt'].
        self.steps.add_step("claim_def['value']['primary']['rctxt']")
        err_msg = "claim_def['value']['primary']['rctxt'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_def_json)['value']['primary']['rctxt'])

        # 13. Check length of claim_def['value']['revocation'].
        self.steps.add_step("Length of claim_def['value']['revocation']")
        err_msg = "Length of claim_def['value']['revocation'] isn't equal 11"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: len(json.loads(cred_def_json)['value']['revocation']) == 11)

        # 14. Check length of claim_def['data']['revocation'].
        self.steps.add_step("Length of claim_def['value']['revocation']")
        err_msg = "Length of claim_def['data']['revocation'] isn't empty"
        result = True
        for _, value in json.loads(cred_def_json)['value']['revocation'].items():
            if not value:
                result = False
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: result)
