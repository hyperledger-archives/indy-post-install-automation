'''
Created on Jan 17, 2018

@author: khoi.ngo
Implementing test case IssuerCreateClaimDefs with 2 DIDs and the same schema.
'''
import json

from indy import anoncreds, did
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateClaimDefsWith2DIDsAndTheSameSchema(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer1_did'")
        (issuer1_did, _) = await utils.perform(self.steps,
                                               did.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 4. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer2_did'")
        (issuer2_did, _) = await utils.perform(self.steps,
                                               did.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 5. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
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
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer1_did, prover_did)
        gvt_claim_req1 = json.loads(
                        await utils.perform(
                            self.steps,
                            anoncreds.prover_create_and_store_claim_req,
                            self.wallet_handle, prover_did,
                            claim_offer, gvt_claim_def1,
                            constant.secret_name))

        # 10. Check gvt_claim_req1['issuer_did'].
        self.steps.add_step("gvt_claim_req1['issuer_did']")
        err_msg = "gvt_claim_req1['issuer_did'] isn't equal issuer1_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req1['issuer_did'] == issuer1_did)

        # 11 Check gvt_claim_req1['schema_key']['name'].
        self.steps.add_step("gvt_claim_req1['schema_key']['name']")
        err_msg = "gvt_claim_req1['schema_key']['name'] isn't equal" + \
            str(constant.gvt_schema['data']['name'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req1['schema_key']['name'] ==
            constant.gvt_schema['data']['name'])

        # 12. Check gvt_claim_req1['schema_key']['did'].
        self.steps.add_step("gvt_claim_req1['schema_key']['did']")
        err_msg = "gvt_claim_req1['schema_key']['did'] isn't equal" + \
                  str(constant.gvt_schema['dest'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req1['schema_key']['did'] ==
                              constant.gvt_schema['dest'])

        # 13. Create claim request with issuer2.
        self.steps.add_step("Create claim request with issuer2")
        claim_offer = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer2_did, prover_did)
        gvt_claim_req2 = json.loads(
                        await utils.perform(
                            self.steps,
                            anoncreds.prover_create_and_store_claim_req,
                            self.wallet_handle, prover_did,
                            claim_offer, gvt_claim_def2,
                            constant.secret_name))

        # 14. Check gvt_claim_req2['issuer_did'].
        self.steps.add_step("gvt_claim_req2['issuer_did']")
        err_msg = "gvt_claim_req2['issuer_did'] isn't equal issuer2_did"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req2['issuer_did'] == issuer2_did)

        # 15. Check gvt_claim_req2['schema_key']['name'].
        self.steps.add_step("gvt_claim_req2['schema_key']['name']")
        err_msg = "gvt_claim_req2['schema_key']['name'] isn't equal" + \
                  str(constant.gvt_schema['data']['name'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req2['schema_key']['name'] ==
                              constant.gvt_schema['data']['name'])

        # 16. Check gvt_claim_req2['schema_key']['did'].
        self.steps.add_step("gvt_claim_req2['schema_key']['did']")
        err_msg = "gvt_claim_req2['schema_key']['did'] isn't equal" + \
                  str(constant.gvt_schema['dest'])
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: gvt_claim_req2['schema_key']['did'] ==
                              constant.gvt_schema['dest'])