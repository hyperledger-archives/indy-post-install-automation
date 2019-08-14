"""
Created on Jan 17, 2018

@author: khoi.ngo

Implementing test case ProverGetsClaim with request predicate and
request attributes.
"""
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetsClaimWithReqPredicateAndReqAttrs(AnoncredsTestBase):

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

        # 8. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 9. Create and store claim definition.
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

        # 10. Create claim request.
        self.steps.add_step("Create claim request")
        cred_offer = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id)
        cred_req, cred_req_meta = await utils.perform(
            self.steps,
            anoncreds.prover_create_credential_req,
            self.wallet_handle, prover_did,
            cred_offer, cred_def_json,
            constant.secret_name)

        # 11. Create claim.
        self.steps.add_step("Create claim")
        cred_json, cred_revoc_id, revoc_reg_delta_json = await utils.perform(self.steps,
                                                                             anoncreds.issuer_create_credential,
                                                                             self.wallet_handle, cred_offer, cred_req,
                                                                             json.dumps(constant.gvt_schema_attr_values),
                                                                             None, None)

        # 12. Store claims into wallet.
        self.steps.add_step("Store claims into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_credential,
                            self.wallet_handle, None, cred_req_meta, cred_json, cred_def_json, None)

        # 13. Get stored claims with proof request that
        # contains empty requested attrs and
        # store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request that contains "
            "empty requested attrs and store result into 'returned_claims'")
        attrs_req = {"attr1_referent": {"name": "name"}}
        predicates_js = {"predicate1_referent":
                         {"name": "age", "p_type": ">=", "p_value": 25}}
        proof_req = utils.create_proof_req("1", "proof_req_1", "1.0",
                                           attrs_req, predicates_js)
        returned_claims = json.loads(await utils.perform(
            self.steps, anoncreds.prover_get_credentials_for_proof_req,
            self.wallet_handle, proof_req))

        # 14. Get claim
        self.steps.add_step("Get claims")
        lst_claims = json.loads(await utils.perform(
                                                self.steps,
                                                anoncreds.prover_get_credentials,
                                                self.wallet_handle, "{}"))

        # 15. Check returned_claims['attrs'].
        self.steps.add_step("Check returned_claims['attrs'] is correct")
        err_msg = "returned_claims['attrs'] is incorrect"
        utils.check(
            self.steps, error_message=err_msg, condition=lambda:
            returned_claims['attrs']['attr1_referent'][0]['cred_info'] == lst_claims[0])

        # 16. Check returned_claims['predicates'].
        self.steps.add_step("Check returned_claims['predicates'] is correct")
        err_msg = "returned_claims['predicates'] is incorrect"
        utils.check(
            self.steps, error_message=err_msg, condition=lambda:
            returned_claims['predicates']['predicate1_referent'][0]['cred_info'] == lst_claims[0])
