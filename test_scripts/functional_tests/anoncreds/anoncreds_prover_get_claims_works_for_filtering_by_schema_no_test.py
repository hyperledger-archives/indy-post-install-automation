"""
Created on Jan 8, 2018

@author: nhan.nguyen
Verify that user can get stored claims by filtering by schema sequence no.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverGetClaimByFilteringWithSchemaNo(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)
        # 3. Create 'issuer1_did'.
        # 4. Create 'issuer2_did'.
        # 5. Create 'prover_did'.
        ((issuer1_did, _),
         (issuer2_did, _),
         (prover_did, _)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=3,
            step_descriptions=["Create 'issuer1_did'",
                               "Create 'issuer2_did'",
                               "Create 'prover_did'"])

        # 6. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 7. Create and store claim definition with 'issuer1_did'.
        self.steps.add_step("Create and store claim definition "
                            "with 'issuer1_did'")
        gvt_claim_def = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer1_did, json.dumps(constant.gvt_schema),
            constant.signature_type, False)

        # 8. Create and store other claim definition with 'issuer2_did'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did'")
        xyz_claim_def = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer2_did, json.dumps(constant.xyz_schema),
            constant.signature_type, False)

        # 9. Create claim request with 'issuer1_did'.
        # 10. Create claim.
        # 11. Store created claim into wallet.
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer1_did, prover_did)

        step_descriptions = ["Create claim request with 'issuer1_did'",
                             "Create claim", "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle,
            prover_did, claim_offer,
            gvt_claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1,
            step_descriptions=step_descriptions)

        # 12. Create other claim request with 'issuer2_did'.
        # 13. Create other claim.
        # 14. Store created claim into wallet.
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.xyz_schema),
                                                                issuer2_did, prover_did)

        step_descriptions = ["Create other claim request with 'issuer2_did'",
                             "Create other claim",
                             "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle,
            prover_did, claim_offer,
            xyz_claim_def, constant.secret_name,
            json.dumps(constant.xyz_claim), -1,
            step_descriptions=step_descriptions)

        # 15. Get stored claims by filtering with gvt_schema_no.
        self.steps.add_step("Get stored claims by "
                            "filtering with gvt_schema_no")
        filter_json = json.dumps({"schema_key": constant.gvt_schema_key})
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, filter_json)

        lst_claims = json.loads(lst_claims)

        # 16. Check returned list claims.
        self.steps.add_step("Check returned list claims")
        err_msg = "Cannot get claims from wallet"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims) == 1)

        # 17. Check lst_claims[0]['claim_uuid'].
        # 18. Check lst_claims[0]['attrs'].
        # 19. Check lst_claims[0]['issuer_did'].
        # 20. Check lst_claims[0]['schema_seq_no'].
        utils.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            issuer1_did, constant.gvt_schema_seq)
