"""
Created on Dec 19, 2017

@author: nhan.nguyen
Verify that 'anoncreds.prover_get_claim_offers' return empty list if there
is no result that satisfy filter json.
"""

import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common


class TestProverGetClaimOffersForNoResults(AnoncredsTestBase):

    @pytest.mark.skip
    # Method under test is deleted.
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Get claim offers and store returned value into 'list_claim_offer'.
        self.steps.add_step("Get claim offers and store "
                            "returned value in to 'list_claim_offer'")
        list_claim_offer = await utils.perform(
            self.steps, anoncreds.prover_get_claim_offers,
            self.wallet_handle, '{}')
        list_claim_offer = json.loads(list_claim_offer)

        # 4. Check length of 'list_claim_offer'.
        self.steps.add_step("Check length of 'list_claim_offer'")
        error_msg = "Length of 'list_claim_offer' is not equal with 0"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: len(list_claim_offer) == 0)
