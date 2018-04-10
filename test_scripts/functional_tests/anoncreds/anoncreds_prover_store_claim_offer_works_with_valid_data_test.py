"""
Created on Dec 15, 2017

@author: nhan.nguyen
Verify that a claim offer can be stored by anoncreds.prover_store_claim_offer
"""

import json

from indy import anoncreds, did
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, constant, common


class TestProverStoreClaimOfferWithValidData(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        await utils.perform(self.steps,
                            anoncreds.issuer_create_and_store_claim_def,
                            self.wallet_handle, issuer_did,
                            json.dumps(constant.gvt_schema),
                            constant.signature_type, False)

        # 5. Store claim offer and verify that there is no exception raise.
        self.steps.add_step("Store claim offer and verify that "
                            "there is no exception raise")
        offer_json = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                               issuer_did, prover_did)

        await utils.perform(self.steps, anoncreds.prover_store_claim_offer,
                            self.wallet_handle, offer_json,
                            ignore_exception=False)

        # 6. Get claim offers and store returned value into 'list_claim_offer'.
        self.steps.add_step("Get claim offers and store "
                            "returned value in to 'list_claim_offer'")
        list_claim_offer = await utils.perform(
            self.steps, anoncreds.prover_get_claim_offers,
            self.wallet_handle, '{}')
        list_claim_offer = json.loads(list_claim_offer)

        # 7. Verify that 'offer_json' exists in 'list_claim_offer'.
        self.steps.add_step("Verify that 'offer_json' exists "
                            "in 'list_claim_offer'")
        utils.check(self.steps, error_message="Cannot store a claim offer",
                    condition=lambda: constant.gvt_schema_key == list_claim_offer[0]['schema_key'])
