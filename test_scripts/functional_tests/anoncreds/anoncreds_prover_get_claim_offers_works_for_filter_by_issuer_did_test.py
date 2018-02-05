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
         (issuer_did2, _)) = await common.create_and_store_dids_and_verkeys(
            self.steps, self.wallet_handle, number=2,
            step_descriptions=["Create 'issuer_did1'", "Create 'issuer_did2'"])

        # 5. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        await utils.perform(self.steps,
                            anoncreds.issuer_create_and_store_claim_def,
                            self.wallet_handle, issuer_did1,
                            json.dumps(constant.gvt_schema),
                            constant.signature_type, False)

        # 6. Store claim offer for 'issuer_did1'.
        self.steps.add_step("Store claim offer for 'issuer_did1'")
        offer_json1 = utils.create_claim_offer(issuer_did1,
                                               constant.gvt_schema_seq)
        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, json.dumps(offer_json1))

        # 7. Store another claim offer for 'issuer_did1'.
        self.steps.add_step("Store another claim offer for 'issuer_did1'")
        offer_json2 = utils.create_claim_offer(issuer_did1, 2)
        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, json.dumps(offer_json2))

        # 8. Store claim offer for 'issuer_did2'.
        self.steps.add_step("Store claim offer for 'issuer_did2'")
        offer_json3 = utils.create_claim_offer(issuer_did2, 2)
        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, json.dumps(offer_json3))

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
                    condition=lambda: offer_json1 in list_claim_offer and
                    offer_json2 in list_claim_offer)
