'''
Created on Jan 17, 2018

@author: khoi.ngo
Implementing test case IssuerCreateClaimDefs with 2 DIDs and the same schema.
'''
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateClaimDefsWith2DIDsAndTheSameSchema(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create and open pool.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, self.pool_genesis_txn_file)

        # 2. Create and open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)
        # 3. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 4. Create 'issuer1_did'.
        self.steps.add_step("Create 'issuer1_did'")
        (issuer1_did, issuer1_vk) = await utils.perform(self.steps,
                                                        did.create_and_store_my_did,
                                                        self.wallet_handle, "{}")

        # 5. Add issuer 1 to the ledger.
        self.steps.add_step("Add issuer 1 to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer1_did, issuer1_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 6. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer2_did'")
        (issuer2_did, issuer2_vk) = await utils.perform(self.steps,
                                                        did.create_and_store_my_did,
                                                        self.wallet_handle, "{}")

        # 7. Add issuer 2 to the ledger.
        self.steps.add_step("Add issuer 2 to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer2_did, issuer2_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 8. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, prover_vk) = await utils.perform(self.steps,
                                                      did.create_and_store_my_did,
                                                      self.wallet_handle, '{}')

        # 9. Add prover to the ledger.
        self.steps.add_step("Add prover to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, prover_did, prover_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 10. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 11. Create and store claim definition 1.
        self.steps.add_step("Create and store claim definition for issuer1")

        schema1_id, schema1_json = await anoncreds.issuer_create_schema(
            issuer1_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema1_request = await ledger.build_schema_request(issuer1_did, schema1_json)
        schema1_result = await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer1_did, schema1_request)
        schema1_json = json.loads(schema1_json)
        schema1_json['seqNo'] = json.loads(schema1_result)['result']['txnMetadata']['seqNo']
        schema1_json = json.dumps(schema1_json)

        cred_def_id1, cred_def_json1 = await utils.perform(
                                                self.steps,
                                                anoncreds.issuer_create_and_store_credential_def,
                                                self.wallet_handle, issuer1_did,
                                                schema1_json, constant.tag,
                                                constant.signature_type, constant.config_false)

        # 12. Create and store claim definition 2.
        self.steps.add_step("Create and store claim definition for issuer2")

        schema2_id, schema2_json = await anoncreds.issuer_create_schema(
            issuer2_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema2_request = await ledger.build_schema_request(issuer2_did, schema2_json)
        schema2_result = await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer2_did, schema2_request)
        schema2_json = json.loads(schema2_json)
        schema2_json['seqNo'] = json.loads(schema2_result)['result']['txnMetadata']['seqNo']
        schema2_json = json.dumps(schema2_json)

        cred_def_id2, cred_def_json2 = await utils.perform(
                                                self.steps,
                                                anoncreds.issuer_create_and_store_credential_def,
                                                self.wallet_handle, issuer2_did,
                                                schema2_json, constant.tag,
                                                constant.signature_type, constant.config_false)

        # 13. Create claim1 request with issuer1.
        self.steps.add_step("Create claim request with issuer1")
        cred_offer1 = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id1)

        cred_req1, cred_req_meta1 = await utils.perform(
                                                self.steps,
                                                anoncreds.prover_create_credential_req,
                                                self.wallet_handle, prover_did,
                                                cred_offer1, cred_def_json1,
                                                constant.secret_name)

        # 14. Check gvt_claim_req1['prover_did'].
        self.steps.add_step("gvt_claim_req1['prover_did']")
        err_msg = "gvt_claim_req1['prover_did'] isn't equal prover_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_req1)['prover_did'] == prover_did)

        # 15. Check cred_def_id.
        self.steps.add_step("Check cred_def_id")
        err_msg = "cred_def_ids isn't equal"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_req1)['cred_def_id'] == cred_def_id1)

        # 16. Create claim request with issuer2.
        self.steps.add_step("Create claim request with issuer2")
        cred_offer2 = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id2)

        cred_req2, cred_req_meta2 = await utils.perform(
                                                self.steps,
                                                anoncreds.prover_create_credential_req,
                                                self.wallet_handle, prover_did,
                                                cred_offer2, cred_def_json2,
                                                constant.secret_name)

        # 17. Check gvt_claim_req2['prover_did'].
        self.steps.add_step("gvt_claim_req2['prover_did']")
        err_msg = "gvt_claim_req2['prover_did'] isn't equal prover_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_req2)['prover_did'] == prover_did)

        # 18. Check cred_def_id.
        self.steps.add_step("Check cred_def_id")
        err_msg = "cred_def_ids isn't equal"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: json.loads(cred_req2)['cred_def_id'] == cred_def_id2)
