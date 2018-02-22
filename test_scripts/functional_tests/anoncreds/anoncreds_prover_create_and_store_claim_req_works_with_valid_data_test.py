"""
Created on Jan 4, 2018

@author: nhan.nguyen
Verify that user can create a claim request.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestProverCreateClaimReq(AnoncredsTestBase):

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
        claim_offer = utils.create_claim_offer(issuer_did,
                                               constant.gvt_schema_seq)
        claim_req = await utils.perform(
            self.steps, anoncreds.prover_create_and_store_claim_req,
            self.wallet_handle, prover_did, json.dumps(claim_offer), claim_def,
            constant.secret_name)

        claim_req = json.loads(claim_req)

        # 8. Check claim_req['blinded_ms'].
        self.steps.add_step("Check claim_req['blinded_ms']")
        err_msg = "claim_req['blinded_ms'] missing some fields"
        blinded_ms = claim_req["blinded_ms"]
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: "prover_did" in blinded_ms and
                                      "u" in blinded_ms and "ur" in blinded_ms)

        # 9. Check claim_req['blinded_ms']['prover_did'].
        self.steps.add_step("Check claim_req['blinded_ms']['prover_did']")
        err_msg = "Prover did in claim request mismatches"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: blinded_ms["prover_did"] == prover_did)

        # 10. Check claim_req['blinded_ms']['u'].
        self.steps.add_step("Check claim_req['blinded_ms']['u']")
        err_msg = "claim_req['blinded_ms']['u'] is empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(blinded_ms["u"]) > 0)

        # 11. Check claim_req['blinded_ms']['ur'].
        self.steps.add_step("Check claim_req['blinded_ms']['ur']")
        err_msg = "claim_req['blinded_ms']['ur'] is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not blinded_ms["ur"])

        # 12. Check claim_req['issuer_did'].
        self.steps.add_step("Check claim_req['issuer_did']")
        err_msg = "Issuer did in claim request mismatches"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: claim_req["issuer_did"] == issuer_did)

        # 13. Check claim_req['schema_seq_no'].
        self.steps.add_step("Check claim_req['schema_seq_no']")
        err_msg = "Schema sequence number in claim request mismatches"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: claim_req["schema_seq_no"] ==
                    constant.gvt_schema_seq)
