"""
Created on Jan 8, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverGetClaimReturnCorrectFormat(AnoncredsTestBase):
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
        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            json.dumps(claim_offer), claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1)

        # 10. Get claims store in wallet.
        self.steps.add_step("Get claims store in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, "{}")

        lst_claims = json.loads(lst_claims)

        # 11. Check returned claims.
        self.steps.add_step("Check returned claims")
        err_msg = "Returned claims is not a list"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: isinstance(lst_claims, list))

        # 12. Check lst_claims[0].
        self.steps.add_step("Check lst_claims[0]")
        err_msg = "Length of lst_claim[0] is incorrect"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims[0]) == 4)

        # 13. Check lst_claims[0]['claim_uuid'].
        # 14. Check lst_claims[0]['attrs'].
        # 15. Check lst_claims[0]['issuer_did'].
        # 16. Check lst_claims[0]['schema_seq_no'].
        utils.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            issuer_did, constant.gvt_schema_seq)


if __name__ == '__main__':
    TestProverGetClaimReturnCorrectFormat().execute_scenario()
