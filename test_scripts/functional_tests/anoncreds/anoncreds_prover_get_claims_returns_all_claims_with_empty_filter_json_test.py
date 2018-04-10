"""
Created on Jan 8, 2018

@author: nhan.nguyen
Verify that user can get all stored claims with empty filter json.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetAllClaimsWithEmptyFilterJson(AnoncredsTestBase):

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
        self.steps.add_step("Create claim request")
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer_did, prover_did)

        claim_req = await utils.perform(
            self.steps, anoncreds.prover_create_and_store_claim_req,
            self.wallet_handle, prover_did, claim_offer,
            claim_def, constant.secret_name)

        # 8. Create claim.
        self.steps.add_step("Create claim")
        (_, created_claim1) = await utils.perform(
            self.steps, anoncreds.issuer_create_claim, self.wallet_handle,
            claim_req, json.dumps(constant.gvt_claim), -1)

        # 9. Create other claim.
        self.steps.add_step("Create other claim")
        (_, created_claim2) = await utils.perform(
            self.steps, anoncreds.issuer_create_claim, self.wallet_handle,
            claim_req, json.dumps(constant.gvt_other_claim), -1)

        # 10. Store claims into wallet.
        self.steps.add_step("Store claims into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_claim1, 0)
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_claim2, 0)

        # 11. Get claims store in wallet.
        self.steps.add_step("Get claims store in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, "{}")

        lst_claims = json.loads(lst_claims)

        # 12. Check returned claims.
        self.steps.add_step("Check returned claims")
        err_msg = "Returned claims is not a list with two elements"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: isinstance(lst_claims, list) and
                    len(lst_claims) == 2)
