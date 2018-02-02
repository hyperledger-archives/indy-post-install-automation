"""
Created on Jan 10, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverGetClaimsWorksWithNoClaimMatchesWithFilter(AnoncredsTestBase):
    async def execute_test_steps(self):
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
        # 9. Store claim into wallet.
        claim_offer = utils.create_claim_offer(issuer_did,
                                               constant.gvt_schema_seq)
        description = ["Create claim request", "Create claim",
                       "Store claim into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            json.dumps(claim_offer), claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1, step_descriptions=description)

        # 10. Get claims store in wallet.
        self.steps.add_step("Get claims store in wallet")
        filter_json = json.dumps({"schema_seq_no":
                                  constant.gvt_schema_seq + 1})
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, filter_json)

        lst_claims = json.loads(lst_claims)

        # 11. Check returned claims.
        self.steps.add_step("Check returned claims")
        err_msg = "Returned claims is not an empty list"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not lst_claims)


if __name__ == '__main__':
    TestProverGetClaimsWorksWithNoClaimMatchesWithFilter().execute_scenario()
