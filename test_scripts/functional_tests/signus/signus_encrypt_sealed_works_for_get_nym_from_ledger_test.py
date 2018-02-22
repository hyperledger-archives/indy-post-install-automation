"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that user can encrypt anonymous message with gotten nym form ledger.
"""

import pytest
import json

from indy import signus, ledger
from utilities import utils, constant, common
from utilities.test_scenario_base import TestScenarioBase


class TestEncryptSealedWithNymFromLedger(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Create 'my_did' and 'my_verkey' with default trustee seed.
        self.steps.add_step("Create 'my_did' and 'my_verkey'")
        my_did_json = json.dumps({"seed": constant.seed_default_trustee})
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, my_did_json)

        # 6. Create 'their_did' and 'their_verkey'.
        self.steps.add_step("Create 'their_did' and 'their_verkey'")
        (their_did, their_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 7. Build NYM request to add 'their_did' as a identity.
        self.steps.add_step("Build NYM request to add "
                            "'their_did' as a identity")
        identity_request = await \
            utils.perform(self.steps, ledger.build_nym_request, my_did,
                          their_did, their_verkey, None, None)

        # 8. Submit built request to add identity.
        self.steps.add_step("Submit built request to add identity")
        await utils.perform(self.steps, ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle,
                            my_did, identity_request)

        # 9. Encrypt message by 'signus.encrypt_sealed'
        self.steps.add_step("Encrypt message by 'signus.encrypt_sealed' -> "
                            "Bug: https://jira.hyperledger.org/browse/IS-508")
        message = "Test signus".encode("utf-8")
        (encrypted_message, nonce) = await utils.perform(
            self.steps, signus.encrypt_sealed, self.wallet_handle,
            self.pool_handle, their_did, message)

        # 10. Check returned nonce.
        self.steps.add_step("Check returned nonce")
        error_message = "Returned nonce is not a binary string"
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(nonce, bytes))

        # 11. Check encrypted message.
        error_message = "Encrypted message is not a binary string"
        self.steps.add_step("Check encrypted message")
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(encrypted_message, bytes))

        # 12. Decrypt message by 'signus.decrypt_sealed'.
        self.steps.add_step("Decrypt message by 'signus.decrypt_sealed'")
        decrypted_msg = await utils.perform(self.steps, signus.decrypt_sealed,
                                            self.wallet_handle, their_did,
                                            encrypted_message)

        # 13. Check decrypted message.
        self.steps.add_step("Check decrypted message")
        error_msg = "Decrypted message is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: decrypted_msg == message)
