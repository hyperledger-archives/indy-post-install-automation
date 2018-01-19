'''
Created on Jan 17, 2018

@author: khoi.ngo
Implementing test case IssuerCreateClaimDefs with 2 DIDs and the same schema.
'''
import json

from indy import anoncreds, signus
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class IssuerCreateClaimDefsWith2DIDsAndTheSameSchema(AnoncredsTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer1_did'")
        (issuer1_did, _) = await utils.perform(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 4. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer2_did'")
        (issuer2_did, _) = await utils.perform(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 5. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, '{}')

        # 6. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 7. Create and store claim definition.
        self.steps.add_step("Create and store claim definition for issuer1")
        gvt_claim_def1 = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer1_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 8. Create and store claim definition.
        self.steps.add_step("Create and store claim definition for issuer2")
        gvt_claim_def2 = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer2_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 9. Create claim1 request with issuer1.
        self.steps.add_step("Create claim request with issuer1")
        claim_offer = utils.create_claim_offer(issuer1_did,
                                               constant.gvt_schema_seq)
        gvt_claim_req1 = json.loads(
                        await utils.perform(
                            self.steps,
                            anoncreds.prover_create_and_store_claim_req,
                            self.wallet_handle, prover_did,
                            json.dumps(claim_offer), gvt_claim_def1,
                            constant.secret_name))

        # 10. Check gvt_claim_req1['issuer_did'].
        self.steps.add_step("gvt_claim_req1['issuer_did']")
        err_msg = "gvt_claim_req1['issuer_did'] isn't equal issuer1_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req1['issuer_did'] == issuer1_did)

        # 11. Check gvt_claim_req1['schema_seq_no'].
        self.steps.add_step("gvt_claim_req1['schema_seq_no']")
        err_msg = "gvt_claim_req1['schema_seq_no'] isn't equal" + \
            str(constant.gvt_schema['seqNo'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req1['schema_seq_no'] ==
            constant.gvt_schema['seqNo'])

        # 12. Create claim request with issuer2.
        self.steps.add_step("Create claim request with issuer2")
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.gvt_schema_seq)
        gvt_claim_req2 = json.loads(
                        await utils.perform(
                            self.steps,
                            anoncreds.prover_create_and_store_claim_req,
                            self.wallet_handle, prover_did,
                            json.dumps(claim_offer), gvt_claim_def2,
                            constant.secret_name))

        # 13. Check gvt_claim_req2['issuer_did'].
        self.steps.add_step("gvt_claim_req2['issuer_did']")
        err_msg = "gvt_claim_req2['issuer_did'] isn't equal issuer2_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req2['issuer_did'] == issuer2_did)

        # 14. Check gvt_claim_req2['schema_seq_no'].
        self.steps.add_step("gvt_claim_req2['schema_seq_no']")
        err_msg = "gvt_claim_req2['schema_seq_no'] isn't equal" + \
            str(constant.gvt_schema['seqNo'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req2['schema_seq_no'] ==
            constant.gvt_schema['seqNo'])


if __name__ == '__main__':
    IssuerCreateClaimDefsWith2DIDsAndTheSameSchema().execute_scenario()
