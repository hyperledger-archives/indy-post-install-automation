"""
Created on Jan 8, 2018

@author: nhan.nguyen
Verify that 'anoncreds.prover_get_claims' returns a list of stored claims
with correct format.
"""
import json

from indy import anoncreds, did, ledger
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetClaimReturnCorrectFormat(AnoncredsTestBase):

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
        # 11. Create claim.
        # 12. Store claim into wallet.
        cred_offer = await anoncreds.issuer_create_credential_offer(self.wallet_handle, cred_def_id)

        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            cred_offer, cred_def_json, constant.secret_name, json.dumps(constant.gvt_schema_attr_values))

        # 13. Get claims store in wallet.
        self.steps.add_step("Get claims store in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_credentials,
                                         self.wallet_handle, "{}")

        lst_claims = json.loads(lst_claims)

        # 14. Check returned claims.
        self.steps.add_step("Check returned claims")
        err_msg = "Returned claims is not a list"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: isinstance(lst_claims, list))

        # 15. Check lst_claims[0].
        self.steps.add_step("Check lst_claims[0]")
        err_msg = "Length of lst_claim[0] is incorrect"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims[0]) == 6)

        # 16. Check lst_claims[0]['claim_uuid'].
        # 17. Check lst_claims[0]['attrs'].
        # 18. Check lst_claims[0]['issuer_did'].
        # 19. Check lst_claims[0]['schema_seq_no'].
        utils.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            cred_def_id, schema_id)
