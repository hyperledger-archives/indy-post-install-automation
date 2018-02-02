"""
Created on Jan 17, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverCreateProofWithValidData(AnoncredsTestBase):
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

        # 7. Create claim request and store result in 'claim_req'.
        # 8. Create claim and store result as 'created_claim'.
        # 9. Store 'created_claim' into wallet.
        claim_offer = utils.create_claim_offer(issuer_did,
                                               constant.gvt_schema_seq)
        description = ["Create claim request and store result in 'claim_req'",
                       "Create claim and store result as 'created_claim'",
                       "Store 'created_claim' into wallet"]
        await common.create_and_store_claim(
            self.steps, self.wallet_handle, prover_did,
            json.dumps(claim_offer), claim_def, constant.secret_name,
            json.dumps(constant.gvt_claim), -1, step_descriptions=description)

        # 10. Get stored claims with proof request that
        # and store result into 'returned_claims'.
        self.steps.add_step(
            "Get stored claims with proof request "
            "and store result into 'returned_claims'")
        proof_req = utils.create_proof_req("1", "proof_req_1", "1.0",
                                           requested_attrs={'attr1_referent': {
                                               'name': 'name'}},
                                           requested_predicates={
                                               'predicate1_referent': {
                                                   'attr_name': 'age',
                                                   'p_type': 'GE',
                                                   'value': 25}})
        returned_claims = await utils.perform(
            self.steps, anoncreds.prover_get_claims_for_proof_req,
            self.wallet_handle, proof_req)

        returned_claims = json.loads(returned_claims)

        # 11. Create proof for proof request
        # and store result as "created_proof".
        self.steps.add_step("Create proof for proof request and "
                            "store result as 'created_proof'")
        referent = returned_claims["attrs"]["attr1_referent"][0][
            constant.claim_uuid_key]
        requested_claims_json = json.dumps({
            'self_attested_attributes': {},
            'requested_attrs': {'attr1_referent': [referent, True]},
            'requested_predicates': {}})
        schemas_json = json.dumps({referent: constant.gvt_schema})
        claims_defs_json = json.dumps({referent: json.loads(claim_def)})
        created_proof = await utils.perform(
            self.steps, anoncreds.prover_create_proof, self.wallet_handle,
            proof_req, requested_claims_json, schemas_json,
            constant.secret_name, claims_defs_json, '{}')

        created_proof = json.loads(created_proof)
        temp_proofs = created_proof['proofs']
        print(str(temp_proofs.keys()))
        temp_ref = temp_proofs[referent]
        temp_proof = temp_ref['proof']
        temp_pri_proof = temp_proof['primary_proof']
        temp_eq_proof = temp_pri_proof['eq_proof']
        temp_agg = created_proof['aggregated_proof']
        temp_req_proof = created_proof['requested_proof']

        # 12. Check created_proof['proofs'][referent]['proof']['primary_proof']
        # ['eq_proof']['revealed_attrs']['name']
        self.steps.add_step(
            "Check created_proof['proofs'][referent]['proof']"
            "['primary_proof']['eq_proof']['revealed_attrs']['name']")
        err_msg = "created_proof['proofs'][referent]['proof']" \
                  "['primary_proof']['eq_proof']['revealed_attrs']" \
                  "['name'] mismatches"
        temp = temp_eq_proof['revealed_attrs']['name']
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: temp == constant.gvt_claim['name'][1])

        # 13. Check created_proof['proofs'][referent]
        # ['proof']['primary_proof']['eq_proof']['m']
        self.steps.add_step("Check created_proof['proofs'][referent]['proof']"
                            "['primary_proof']['eq_proof']['m']")
        err_msg = "Some field is miss from created_proof['proofs'][referent]"\
                  "['proof']['primary_proof']['eq_proof']['m']"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: all(i in ('sex', 'height', 'age')
                                          for i in temp_eq_proof['m'].keys()))

        # 14. Check created_proof['proofs'][referent]['proof']
        # [non_revoc_proof']
        self.steps.add_step("Check created_proof['proofs'][referent]['proof']"
                            "[non_revoc_proof']")
        err_msg = "created_proof['proofs'][referent]['proof']" \
                  "[non_revoc_proof'] is not None"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not temp_proof['non_revoc_proof'])

        # 15. Check created_proof['proofs'][referent]['issuer_did']
        self.steps.add_step("Check created_proof['proofs']"
                            "[referent]['issuer_did']")
        err_msg = "created_proof['proofs'][referent]" \
                  "['issuer_did'] mismatches"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: temp_ref['issuer_did'] == issuer_did)

        # 16. Check created_proof['proofs'][referent]['schema_seq_no']
        self.steps.add_step("Check created_proof['proofs'][referent]"
                            "['schema_seq_no']")
        err_msg = "Check created_proof['proofs'][referent]" \
                  "['schema_seq_no'] mismatches"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: temp_ref['schema_seq_no'] ==
                    constant.gvt_schema_seq)

        # 17. Check created_proof['aggregated_proof']
        self.steps.add_step("Check created_proof"
                            "['aggregated_proof']")
        err_msg = "Some field is missing from " \
                  "created_proof['aggregated_proof']"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: all(i in ('c_hash', 'c_list') for
                                          i in temp_agg))

        # 18. Check created_proof['requested_proof']
        # ['revealed_attrs']['attr1_referent']
        self.steps.add_step("Check created_proof['requested_proof']"
                            "['revealed_attrs']['attr1_referent']")
        err_msg = "created_proof['requested_proof']" \
                  "['revealed_attrs']['attr1_referent'] mismatches"
        temp = temp_req_proof['revealed_attrs']['attr1_referent']
        utils.check(self.steps, err_msg,
                    lambda: all(i in [referent, constant.gvt_claim['name'][1],
                                      constant.gvt_claim['name'][0]]
                                for i in temp))

        # 19. Check created_proof['requested_proof']['unrevealed_attrs']
        self.steps.add_step("Check created_proof"
                            "['requested_proof']['unrevealed_attrs']")
        err_msg = "created_proof['requested_proof']" \
                  "['unrevealed_attrs'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not temp_req_proof['unrevealed_attrs'])

        # 20. Check created_proof['requested_proof']['self_attested_attrs']
        self.steps.add_step("Check created_proof"
                            "['requested_proof']['self_attested_attrs']")
        err_msg = "created_proof['requested_proof']" \
                  "['self_attested_attrs'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not
                    temp_req_proof['self_attested_attrs'])

        # 21. Check created_proof['requested_proof']['predicates']
        self.steps.add_step("Check created_proof['requested_proof']"
                            "['predicates']")
        err_msg = "created_proof['requested_proof']" \
                  "['predicates'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not temp_req_proof['predicates'])


if __name__ == '__main__':
    TestProverCreateProofWithValidData().execute_scenario()
