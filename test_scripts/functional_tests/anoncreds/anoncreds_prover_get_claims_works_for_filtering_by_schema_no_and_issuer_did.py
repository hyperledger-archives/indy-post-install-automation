"""
Created on Jan 8, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverGetClaimByFilteringWithSchemaNoAndIssuerDid(AnoncredsTestBase):
    async def execute_test_steps(self):
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

        # 7. Create and store claim definition
        # with 'issuer1_did' and 'gvt_schema'.
        self.steps.add_step("Create and store claim definition "
                            "with 'issuer1_did' and 'gvt_schema'")
        gvt_claim_def1 = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer1_did, json.dumps(constant.gvt_schema),
            constant.signature_type, False)

        # 8. Create and store other claim definition
        # with 'issuer2_did' with 'xyz_schema'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did' with 'xyz_schema'")
        xyz_claim_def = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer2_did, json.dumps(constant.xyz_schema),
            constant.signature_type, False)

        # 9. Create and store other claim definition
        # with 'issuer2_did' and 'gvt_schema'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did' and 'gvt_schema'")
        gvt_claim_def2 = await utils.perform(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle, issuer2_did, json.dumps(constant.gvt_schema),
            constant.signature_type, False)

        # 10. Create claim request with 'issuer1_did' and 'gvt_schema'.
        # 11. Create claim with 'gvt_schema'.
        # 12. Store created claim into wallet.
        claim_offer = utils.create_claim_offer(issuer1_did,
                                               constant.gvt_schema_seq)
        step_descriptions = ["Create claim request with "
                             "'issuer1_did' and 'gvt_schema'",
                             "Create claim with 'gvt_schema'",
                             "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle,
            prover_did, json.dumps(claim_offer),
            gvt_claim_def1, constant.secret_name,
            json.dumps(constant.gvt_claim), -1,
            step_descriptions=step_descriptions)

        # 13. Create other claim request with 'issuer2_did' and 'xyz_schema'.
        # 14. Create other claim with 'xyz_schema'.
        # 15. Store created claim into wallet.
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.xyz_schema_seq)
        step_descriptions = ["Create other claim request with "
                             "'issuer2_did' and 'xyz_schema'",
                             "Create other claim with 'xyz_schema'",
                             "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle,
            prover_did, json.dumps(claim_offer),
            xyz_claim_def, constant.secret_name,
            json.dumps(constant.xyz_claim), -1,
            step_descriptions=step_descriptions
        )

        # 16. Create another claim request with 'issuer2_did' and 'gvt_schema'.
        # 17. Create claim with 'gvt_schema'.
        # 18. Store created claim into wallet.
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.gvt_schema_seq)
        step_descriptions = ["Create another claim request with "
                             "'issuer2_did' and 'gvt_schema'",
                             "Create other claim with 'gvt_schema'",
                             "Store created claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle,
            prover_did, json.dumps(claim_offer),
            gvt_claim_def2, constant.secret_name,
            json.dumps(constant.gvt_other_claim), -1,
            step_descriptions=step_descriptions
        )

        # 19. Get stored claims by filtering with
        # 'issuer2_did and gvt_schema_no.
        self.steps.add_step("Get stored claims by "
                            "filtering with 'issuer2_did' and gvt_schema_no")
        filter_json = json.dumps({"schema_seq_no": constant.gvt_schema_seq,
                                  "issuer_did": issuer2_did})
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
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
            self.steps, lst_claims[0], constant.gvt_other_claim,
            issuer2_did, constant.gvt_schema_seq)


if __name__ == '__main__':
    TestProverGetClaimByFilteringWithSchemaNoAndIssuerDid().execute_scenario()
