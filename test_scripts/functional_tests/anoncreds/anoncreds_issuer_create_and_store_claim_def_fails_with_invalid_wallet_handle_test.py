"""
Created on Dec 15, 2017

@author: nhan.nguyen
Verify that user cannot create and store a claim definition with invalid
wallet handle.
"""

import json

from indy import anoncreds, signus
from indy.error import ErrorCode
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateAndStoreClaimDefWithInvalidWalletHandle\
            (AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create and store claim definition with invalid wallet handle
        # and verify that a claim definition cannot be created.
        self.steps.add_step("Create and store claim definition with invalid "
                            "wallet handle and verify that a "
                            "claim definition cannot be created.")
        error_code = ErrorCode.WalletInvalidHandle

        await utils.perform_with_expected_code(
            self.steps, anoncreds.issuer_create_and_store_claim_def,
            self.wallet_handle + 1, issuer_did,
            json.dumps(constant.gvt_schema),
            constant.signature_type, False, expected_code=error_code)
