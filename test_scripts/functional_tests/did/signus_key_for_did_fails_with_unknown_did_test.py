"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user cannot get verkey of an unknown did.
"""

import pytest
from indy import did
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.did.signus_test_base\
    import DidTestBase


class TestKeyForDidWithUnknownDid(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file
        )

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 5. Get verkey for unknown did and verify that user cannot get
        # verkey for an unknown did.
        self.steps.add_step("Get verkey for unknown did and verify that "
                            "user cannot get verkey for an unknown did")
        error_code = ErrorCode.WalletItemNotFound
        await utils.perform_with_expected_code(self.steps, did.key_for_did,
                                               self.pool_handle,
                                               self.wallet_handle,
                                               constant.did_my2,
                                               expected_code=error_code)
