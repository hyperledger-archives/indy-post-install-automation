"""
Created on Dec 19, 2017

@author: nhan.nguyen
Verify that a claim offer cannot be stored by
anoncreds.prover_store_claim_offer with invalid json.
"""

import json

from indy import anoncreds, did
from indy.error import ErrorCode
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, constant, common


class TestProverStoreClaimOfferWithInvalidJson(AnoncredsTestBase):

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

        # 5. Store claim offer with invalid json and
        # verify that claim offer cannot be stored.
        self.steps.add_step("Store claim offer with invalid json and "
                            "verify that claim offer cannot be stored")
        offer_json = await anoncreds.issuer_create_claim_offer(self.wallet_handle, json.dumps(constant.gvt_schema),
                                                               issuer_did, prover_did)

        offer_json = json.dumps(json.loads(offer_json).pop('schema_key'))

        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(
            self.steps, anoncreds.prover_store_claim_offer, self.wallet_handle,
            offer_json, expected_code=error_code)
