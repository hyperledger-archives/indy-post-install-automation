"""
Created on Jan 12, 2018

@author: nhan.nguyen
Verify that system returns no claim when getting claim with proof request
that contains empty requested predicates and empty requested attrs.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetClaimsForProofReqWithEmptyReqPredicateAndReqAttrs \
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
        claim_def = await utils.perform(
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
            claim_offer, claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1)

        # 10. Get stored claims with proof request that
        # contains empty requested predicates and empty
        # requested attrs and store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request that contains "
            "empty requested predicates and empty requested attrs "
            "and store result into 'returned_claims'")
        proof_req = utils.create_proof_req("1", "proof_req_1", "1.0",
                                           requested_attrs={},
                                           requested_predicates={})
        returned_claims = await utils.perform(
            self.steps, anoncreds.prover_get_claims_for_proof_req,
            self.wallet_handle, proof_req)

        returned_claims = json.loads(returned_claims)

        # 11. Check returned_claims['attrs'].
        self.steps.add_step("Check returned_claims['attrs']")
        err_msg = "returned_claims['attrs'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not returned_claims['attrs'])

        # 12. Check returned_claims['predicates'].
        self.steps.add_step("Check returned_claims['predicates']")
        err_msg = "returned_claims['predicates'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not returned_claims['predicates'])
