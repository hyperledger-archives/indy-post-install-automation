"""
Created on Dec 18, 2017

@author: nhan.nguyen
Verify that user can create claim with valid data.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateClaim(AnoncredsTestBase):

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
        created_claim = json.loads(created_claim)

        # 9. Check created_claim['issuer_did'].
        self.steps.add_step("Check created_claim['issuer_did']")
        error_msg = "'issuer_did' mismatches"
        utils.check(self.steps, error_msg,
                    condition=lambda:
                    created_claim['issuer_did'] == issuer_did)

        # 10. Check created_claim['schema_seq_no'].
        self.steps.add_step("Check created_claim['schema_seq_no']")
        error_msg = "'schema_seq_no' mismatches"
        utils.check(self.steps, error_msg,
                    condition=lambda: utils.compare_json(created_claim['schema_key'], constant.gvt_schema_key))

        # 11. Check created_claim['claim'].
        self.steps.add_step("Check created_claim['claim']")
        error_msg = "'claim' mismatches"
        utils.check(self.steps, error_msg,
                    condition=lambda:
                    created_claim['values'] == constant.gvt_claim)
