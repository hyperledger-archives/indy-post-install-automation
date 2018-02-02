"""
Created on Dec 19, 2017

@author: nhan.nguyen
"""

import json
from indy import anoncreds, signus
from indy.error import ErrorCode
from utilities import utils, constant, common
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverStoreClaimOfferWithInvalidJson(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
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
        offer_json = utils.create_claim_offer(issuer_did)
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(
            self.steps, anoncreds.prover_store_claim_offer, self.wallet_handle,
            json.dumps(offer_json), expected_code=error_code)


if __name__ == '__main__':
    TestProverStoreClaimOfferWithInvalidJson().execute_scenario()
