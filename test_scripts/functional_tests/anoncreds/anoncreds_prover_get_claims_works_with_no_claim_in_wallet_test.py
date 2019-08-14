"""
Created on Jan 10, 2018

@author: nhan.nguyen
Verify that 'anoncreds.prover_get_claims' returns an empty list claims with
no claim in wallet.
"""
import json

from indy import anoncreds
import pytest

from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase
from utilities import utils, common


class TestProverGetClaimWithNoClaimInWallet(AnoncredsTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create and open pool.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, self.pool_genesis_txn_file)

        # 2. Create and open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Get stored claims in wallet.
        self.steps.add_step("Get stored claims in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_credentials,
                                         self.wallet_handle, '{}')

        lst_claims = json.loads(lst_claims)

        # 4. Check returned list claims.
        self.steps.add_step("Check returned list claims")
        err_msg = "Returned list claims is not empty"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: not lst_claims)
