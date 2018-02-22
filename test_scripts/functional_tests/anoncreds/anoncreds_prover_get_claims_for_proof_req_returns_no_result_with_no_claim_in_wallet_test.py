"""
Created on Jan 17, 2018

@author: nhan.nguyen
Verify that system returns no claim if there is no claim in wallet.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common


class TestProverGetClaimsForProofReqForNoStoredClaimInWallet\
            (AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Get stored claims with proof request
        # and store result into 'returned_claims'.
        self.steps.add_step("Get stored claims with proof request "
                            "and store result into 'returned_claims'.")
        proof_req = utils.create_proof_req(
            "1", "proof_req_1", "1.0",
            requested_attrs={'attr1_referent': {'name': 'name'}},
            requested_predicates={
                'predicate1_referent': {'attr_name': 'age', 'p_type': 'GE',
                                        'value': 25}})
        returned_claims = await utils.perform(
            self.steps, anoncreds.prover_get_claims_for_proof_req,
            self.wallet_handle, proof_req)

        returned_claims = json.loads(returned_claims)

        # 4. Check returned_claims['attrs']['attr1_referent'].
        self.steps.add_step("Check returned_claims['attrs']['attr1_referent']")
        err_msg = "returned_claims['attrs']['attr1_referent'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not
                    returned_claims['attrs']['attr1_referent'])

        # 5. Check returned_claims['predicates']['predicate1_referent'].
        self.steps.add_step(
            "Check returned_claims['predicates']['predicate1_referent']")
        err_msg = "returned_claims['predicates']['predicate1_referent'] " \
                  "is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not
                    returned_claims['predicates']['predicate1_referent'])
