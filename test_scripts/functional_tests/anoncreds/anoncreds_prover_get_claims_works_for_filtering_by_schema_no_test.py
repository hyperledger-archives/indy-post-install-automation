"""
Created on Jan 8, 2018

@author: nhan.nguyen
Verify that user can get stored claims by filtering by schema sequence no.
"""
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetClaimByFilteringWithSchemaNo(AnoncredsTestBase):

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

        # 3. Create 'issuer1_did'.
        # 4. Create 'issuer2_did'.
        # 5. Create 'prover_did'.
        ((issuer1_did, issuer1_vk),
         (issuer2_did, issuer2_vk),
         (prover_did, prover_vk)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=3,
            step_descriptions=["Create 'issuer1_did'",
                               "Create 'issuer2_did'",
                               "Create 'prover_did'"])

        # 6. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 7. Add issuer 1 to the ledger.
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer1_did, issuer1_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 8. Add issuer 2 to the ledger.
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer2_did, issuer2_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

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

        # 11. Create and store claim definition with 'issuer1_did'.
        self.steps.add_step("Create and store claim definition "
                            "with 'issuer1_did'")
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

        # 12. Create and store other claim definition with 'issuer2_did'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did'")
        schema2_id, schema2_json = await anoncreds.issuer_create_schema(
            issuer2_did, constant.xyz_schema_name, "1.0", constant.xyz_schema_attr_names)
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

        # 13. Create claim request with 'issuer1_did'.
        # 14. Create claim.
        # 15. Store created claim into wallet.
        cred_offer1 = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id1)

        step_descriptions = ["Create claim request with 'issuer1_did'",
                             "Create claim", "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            cred_offer1, cred_def_json1, constant.secret_name, json.dumps(constant.gvt_schema_attr_values),
            step_descriptions=step_descriptions)

        # 16. Create other claim request with 'issuer2_did'.
        # 17. Create other claim.
        # 18. Store created claim into wallet.
        cred_offer2 = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id2)

        step_descriptions = ["Create other claim request with 'issuer2_did'",
                             "Create other claim",
                             "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            cred_offer2, cred_def_json2, constant.secret_name, json.dumps(constant.xyz_schema_attr_values),
            step_descriptions=step_descriptions)

        # 19. Get stored claims by filtering with gvt_schema_no.
        self.steps.add_step("Get stored claims by "
                            "filtering with gvt_schema_no")
        filter_json = json.dumps({"schema_id": schema1_id})
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_credentials,
                                         self.wallet_handle, filter_json)

        lst_claims = json.loads(lst_claims)

        # 20. Check returned list claims.
        self.steps.add_step("Check returned list claims")
        err_msg = "Cannot get claims from wallet"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims) == 1)

        # 21. Check lst_claims[0]['claim_uuid'].
        # 22. Check lst_claims[0]['attrs'].
        # 23. Check lst_claims[0]['issuer_did'].
        # 24. Check lst_claims[0]['schema_seq_no'].
        utils.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            cred_def_id1, schema1_id)
