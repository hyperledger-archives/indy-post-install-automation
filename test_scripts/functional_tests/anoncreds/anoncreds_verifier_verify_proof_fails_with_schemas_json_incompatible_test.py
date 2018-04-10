"""
Created on Jan 16, 2018

@author: nhan.nguyen
Verify that 'anoncreds.verifier_verify_proof' return false if argument
'schemas_json' is incompatiple.
"""
import json

from indy import anoncreds
from indy.error import ErrorCode
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestVerifierVerifyProofFailsWithIncompatibleSchemasJson\
            (AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'issuer_did'.
        # 4. Create 'prover_did'.
        ((issuer_did, _),
         (prover_did, _)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=2,
            step_descriptions=["Create 'issuer_did'", "Create 'prover_did'"])

        # 5. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 6. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        gvt_claim_def = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer_did, json.dumps(constant.gvt_schema),
            constant.signature_type, False)

        # 7. Create claim request.
        # 8. Create claim.
        # 9. Store claims into wallet.
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer_did, prover_did)

        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            claim_offer, gvt_claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1)

        # 10. Get stored claims with proof and
        # store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request "
            "and store result into 'returned_claims'")
        proof_req = utils.create_proof_req(
            "1", "proof_req_1", "1.0",
            requested_attrs={'attr1_referent': {'name': 'name'}},
            requested_predicates={})
        returned_claims = await utils.perform(
            self.steps, anoncreds.prover_get_claims_for_proof_req,
            self.wallet_handle, proof_req)

        returned_claims = json.loads(returned_claims)

        # 11. Create proof for proof request and
        # store result as "created_proof".
        self.steps.add_step("Create proof for proof request and "
                            "store result as 'created_proof'")
        referent = returned_claims["attrs"]["attr1_referent"][0][
            constant.claim_uuid_key]
        requested_claims_json = json.dumps({
            'self_attested_attributes': {},
            'requested_attrs': {'attr1_referent': [referent, True]},
            'requested_predicates': {}})
        schemas_json = json.dumps({referent: constant.gvt_schema})
        claims_defs_json = json.dumps({referent: json.loads(gvt_claim_def)})
        created_proof = await utils.perform(
            self.steps, anoncreds.prover_create_proof, self.wallet_handle,
            proof_req, requested_claims_json, schemas_json,
            constant.secret_name, claims_defs_json, '{}')

        # 12. Verify created proof with incompatible schemas json and
        # verify that user cannot verify proof.
        self.steps.add_step("Verify created proof with incompatible schemas "
                            "json and verify that user cannot verify proof")
        incompatible_schemas_json = json.dumps({referent: constant.xyz_schema})
        err_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(
            self.steps, anoncreds.verifier_verify_proof, proof_req,
            created_proof, incompatible_schemas_json, claims_defs_json, '{}',
            expected_code=err_code)
