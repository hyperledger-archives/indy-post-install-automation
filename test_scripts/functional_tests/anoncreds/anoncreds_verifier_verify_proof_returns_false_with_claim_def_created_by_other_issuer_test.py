"""
Created on Jan 16, 2018

@author: nhan.nguyen
Verify that 'anoncreds.verifier_verify_proof' return false
if argument 'claim_defs_json' is incompatiple.
"""
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestVerifierVerifyProofWithClaimDefCreatedByOtherIssuer\
            (AnoncredsTestBase):

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

        # 3. Create 'issuer_did'.
        # 4. Create 'prover_did'.
        ((issuer_did, issuer_vk),
         (prover_did, prover_vk)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=2,
            step_descriptions=["Create 'issuer_did'", "Create 'prover_did'"])

        # 5. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 5. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 6. Add issuer to the ledger.
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did, issuer_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 7. Add prover to the ledger.
        self.steps.add_step("Add prover to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, prover_did, prover_vk, alias=None, role='TRUSTEE')
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
                                                constant.signature_type, constant.config_false)

        # 7. Create claim request.
        # 8. Create claim.
        # 9. Store claims into wallet.
        cred_offer = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id)

        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            cred_offer, cred_def_json, constant.secret_name, json.dumps(constant.gvt_schema_attr_values))

        # 10. Get stored claims with proof and
        # store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request "
            "and store result into 'returned_claims'")
        proof_req = utils.create_proof_req(
            "1", "proof_req_1", "1.0",
            requested_attributes={'attr1_referent': {'name': 'name'}},
            requested_predicates={})
        returned_claims = await utils.perform(
            self.steps, anoncreds.prover_get_credentials_for_proof_req,
            self.wallet_handle, proof_req)

        returned_claims = json.loads(returned_claims)

        # 11. Create proof for proof request and
        # store result as "created_proof".
        self.steps.add_step("Create proof for proof request and "
                            "store result as 'created_proof'")
        referent = returned_claims["attrs"]["attr1_referent"][0]["cred_info"][constant.claim_uuid_key]
        requested_claims_json = json.dumps({
            'self_attested_attributes': {},
            'requested_attributes': {'attr1_referent': {"cred_id": referent, "revealed": True}},
            'requested_predicates': {}})
        schemas_json = json.dumps({schema_id: json.loads(schema_json)})
        claims_defs_json = json.dumps({cred_def_id: json.loads(cred_def_json)})
        created_proof = await utils.perform(
            self.steps, anoncreds.prover_create_proof, self.wallet_handle,
            proof_req, requested_claims_json,
            constant.secret_name,  schemas_json, claims_defs_json, '{}')

        # 12. Create 'issuer_did2'.
        self.steps.add_step("Create 'issuer_did2'")
        issuer_did2, issuer_vk2 = await  utils.perform(self.steps,
                                                       did.create_and_store_my_did,
                                                       self.wallet_handle, '{}')

        # 13. Add issuer 2 to the ledger.
        self.steps.add_step("Add issuer 2 to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did2, issuer_vk2, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 13. Create and store other claim definition with 'issuer_did2'
        # and store returned result as 'gvt_claim_def2'.
        self.steps.add_step("Create and store other claim definition with "
                            "'issuer_did2' and store returned result as"
                            " 'gvt_claim_def2'")
        self.steps.add_step("Create and store claim definition")
        schema_id2, schema_json2 = await anoncreds.issuer_create_schema(
            issuer_did2, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema_request2 = await ledger.build_schema_request(issuer_did2, schema_json2)
        schema_result2 = await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer_did2, schema_request2)
        schema_json2 = json.loads(schema_json2)
        schema_json2['seqNo'] = json.loads(schema_result2)['result']['txnMetadata']['seqNo']
        schema_json2 = json.dumps(schema_json2)

        cred_def_id2, cred_def_json2 = await utils.perform(
                                                self.steps,
                                                anoncreds.issuer_create_and_store_credential_def,
                                                self.wallet_handle, issuer_did2,
                                                schema_json2, constant.tag,
                                                constant.signature_type, constant.config_false)

        # 14. Verify created proof with incompatible claim defs json.
        self.steps.add_step("Verify created proof with "
                            "incompatible claim defs json")
        claims_defs_json2 = json.dumps({cred_def_id: json.loads(cred_def_json2)})
        result = await utils.perform(
            self.steps, anoncreds.verifier_verify_proof, proof_req,
            created_proof, schemas_json, claims_defs_json2, '{}', '{}')
        err_msg = "True is returned instead"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not result)
