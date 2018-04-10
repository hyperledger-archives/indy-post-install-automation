'''
Created on Jan 17, 2018

@author: khoi.ngo
Implementing test case IssuerCreateClaimDefs with create_none_revoc.
'''
import json

from indy import anoncreds, did
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common, constant


class TestIssuerCreateAndStoreClaimDefsWithCreateNoneRevoc(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              did.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        claim_def = json.loads(await utils.perform(
                              self.steps,
                              anoncreds.issuer_create_and_store_claim_def,
                              self.wallet_handle, issuer_did,
                              json.dumps(constant.gvt_schema),
                              constant.signature_type, True))
        print("claim_def: " + str(claim_def))
        # 5. Check len(claim_def['data']['primary']['r']).
        self.steps.add_step("len(claim_def['data']['primary']['r'])")
        err_msg = "len(claim_def['data']['primary']['r']) isn't equal 4"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: len(claim_def['data']['primary']['r']) == 4)

        # 6. Check claim_def['data']['primary']['n'].
        self.steps.add_step("claim_def['data']['primary']['n']")
        err_msg = "claim_def['data']['primary']['n'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: claim_def['data']['primary']['n'])

        # 7. Check claim_def['data']['primary']['s'].
        self.steps.add_step("claim_def['data']['primary']['s']")
        err_msg = "claim_def['data']['primary']['s'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: claim_def['data']['primary']['s'])

        # 8. Check claim_def['data']['primary']['rms'].
        self.steps.add_step("claim_def['data']['primary']['rms']")
        err_msg = "claim_def['data']['primary']['rms'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: claim_def['data']['primary']['rms'])

        # 9. Check claim_def['data']['primary']['z'].
        self.steps.add_step("claim_def['data']['primary']['z']")
        err_msg = "claim_def['data']['primary']['z'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: claim_def['data']['primary']['z'])

        # 10. Check claim_def['data']['primary']['rctxt'].
        self.steps.add_step("claim_def['data']['primary']['rctxt']")
        err_msg = "claim_def['data']['primary']['rctxt'] is empty"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: claim_def['data']['primary']['rctxt'])

        # 11. Check length of claim_def['data']['revocation'].
        self.steps.add_step("Length of claim_def['data']['revocation']")
        err_msg = "Length of claim_def['data']['revocation'] isn't equal 11"
        utils.check(
            self.steps, error_message=err_msg,
            condition=lambda: len(claim_def['data']['revocation']) == 11)

        # 12. Check length of claim_def['data']['revocation'].
        self.steps.add_step("Length of claim_def['data']['revocation']")
        err_msg = "Length of claim_def['data']['revocation'] isn't empty"
        result = True
        for _, value in claim_def['data']['revocation'].items():
            if not value:
                result = False
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: result)
