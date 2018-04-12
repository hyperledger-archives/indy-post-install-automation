"""
Created on Dec 19, 2017

@author: nhan.nguyen
Verify that user can get claim offers for filtering by issuer's did.
"""

import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, constant, common


class TestProverGetClaimOffersForFilterByIssuerDid(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'issuer_did1'.
        # 4. Create 'issuer_did2'.
        ((issuer_did1, _),
         (issuer_did2, _),
         (prover_did, _)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=3,
            step_descriptions=["Create 'issuer_did1'", "Create 'issuer_did2'", "Create 'prover_did'"])

        # 5. Create and store claim definition.
        self.steps.add_step("Create and store 3 claim definitions")
        await utils.perform(self.steps,
                            anoncreds.issuer_create_and_store_claim_def,
                            self.wallet_handle, issuer_did1,
                            json.dumps(constant.gvt_schema),
                            constant.signature_type, False)

        await utils.perform(self.steps,
                            anoncreds.issuer_create_and_store_claim_def,
                            self.wallet_handle, issuer_did1,
                            json.dumps(constant.xyz_schema),
                            constant.signature_type, False)

        await utils.perform(self.steps,
                            anoncreds.issuer_create_and_store_claim_def,
                            self.wallet_handle, issuer_did2,
                            json.dumps(constant.xyz_schema),
                            constant.signature_type, False)

        # 6. Store claim offer for 'issuer_did1'.
        self.steps.add_step("Store claim offer for 'issuer_did1'")
        offer_json1 = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                                issuer_did1, prover_did)

        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, offer_json1)

        # 7. Store another claim offer for 'issuer_did1'.
        self.steps.add_step("Store another claim offer for 'issuer_did1'")
        offer_json2 = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.xyz_schema),
                                                                issuer_did1, prover_did)

        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, offer_json2)

        # 8. Store claim offer for 'issuer_did2'.
        self.steps.add_step("Store claim offer for 'issuer_did2'")
        offer_json3 = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.xyz_schema),
                                                                issuer_did2, prover_did)

        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, offer_json3)

        # 9. Get claim offers and store returned value into 'list_claim_offer'.
        self.steps.add_step("Get claim offers and store "
                            "returned value in to 'list_claim_offer'")
        list_claim_offer = await utils.perform(
            self.steps, anoncreds.prover_get_claim_offers,
            self.wallet_handle, json.dumps({"issuer_did": issuer_did1}))
        list_claim_offer = json.loads(list_claim_offer)

        # 10. Check length of "list_claim_offer".
        self.steps.add_step("Check length of 'list_claim_offer'")
        error_msg = "Length of 'list_claim_offer' is not equal with 2"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(list_claim_offer) == 2)

        # 11. Verify that 'offer_json1' and 'offer_json2'
        # exist in 'list_claim_offer'.
        self.steps.add_step("Verify that 'offer_json1' and 'offer_json2' "
                            "exist in 'list_claim_offer'")
        utils.check(self.steps, error_message="Cannot get claim offer",
                    condition=lambda: constant.gvt_schema_key == list_claim_offer[0]['schema_key'] and
                    constant.xyz_schema_key == list_claim_offer[1]['schema_key'])
