"""
Created on Jan 17, 2018

@author: khoi.ngo

Implementing test case ProverGetsClaim with request predicate and
request attributes.
"""
import json

from indy import anoncreds, did
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetsClaimWithReqPredicateAndReqAttrs(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, '{}')

        # 5. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 6. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 7. Create claim request.
        self.steps.add_step("Create claim request")
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer_did, prover_did)

        claim_req = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          claim_offer, claim_def,
                          constant.secret_name)

        # 8. Create claim.
        self.steps.add_step("Create claim")
        (_, created_claim) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, claim_req,
                          json.dumps(constant.gvt_claim), -1)

        # 9. Store claims into wallet.
        self.steps.add_step("Store claims into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_claim, 0)

        # 10. Get stored claims with proof request that
        # contains empty requested attrs and
        # store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request that contains "
            "empty requested attrs and store result into 'returned_claims'")
        attrs_req = {"attr1_referent": {"name": "name"}}
        predicates_js = {"predicate1_referent":
                         {"attr_name": "age", "p_type": ">=", "value": 25}}
        proof_req = utils.create_proof_req("1", "proof_req_1", "1.0",
                                           attrs_req, predicates_js)
        returned_claims = json.loads(await utils.perform(
            self.steps, anoncreds.prover_get_claims_for_proof_req,
            self.wallet_handle, proof_req))

        # 11. Get claim
        self.steps.add_step("Get claims")
        lst_claims = json.loads(await utils.perform(
                                                self.steps,
                                                anoncreds.prover_get_claims,
                                                self.wallet_handle, "{}"))

        # 12. Check returned_claims['attrs'].
        self.steps.add_step("Check returned_claims['attrs'] is correct")
        err_msg = "returned_claims['attrs'] is incorrect"
        utils.check(
            self.steps, error_message=err_msg, condition=lambda:
            returned_claims['attrs']['attr1_referent'] == lst_claims)

        # 13. Check returned_claims['predicates'].
        self.steps.add_step("Check returned_claims['predicates'] is correct")
        err_msg = "returned_claims['predicates'] is incorrect"
        utils.check(
            self.steps, error_message=err_msg, condition=lambda:
            returned_claims['predicates']['predicate1_referent'] == lst_claims)
