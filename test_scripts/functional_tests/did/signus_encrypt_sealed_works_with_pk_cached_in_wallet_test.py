"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that user can encrypt anonymous
message with public key cached in wallet.
"""

import pytest
import json

from indy import did, crypto
from utilities import utils, common
from test_scripts.functional_tests.did.signus_test_base \
    import DidTestBase


class TestEncryptSealedWithPkInWallet(DidTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create 'their_did' and 'their_verkey'.
        self.steps.add_step("Create 'their_did' and 'their_verkey'")
        (their_did, their_verkey) = await \
            utils.perform(self.steps, did.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Store 'their_did' and 'their_verkey' into wallet.
        self.steps.add_step("Store 'their_did' and 'their_verkey' into wallet")
        their_did_json = json.dumps({"did": their_did, "verkey": their_verkey})
        await utils.perform(self.steps, did.store_their_did,
                            self.wallet_handle, their_did_json)

        # 5. Encrypt message by 'did.encrypt_sealed'
        self.steps.add_step("Encrypt message by 'did.encrypt_sealed' -> "
                            "Bug: https://jira.hyperledger.org/browse/IS-508")
        message = "Test did".encode("utf-8")
        encrypted_message = await utils.perform(
            self.steps, crypto.anon_crypt,
            their_verkey, message)

        # 6. Check returned nonce.
        # self.steps.add_step("Check returned nonce")
        # error_message = "Returned nonce is not a binary string"
        # utils.check(self.steps, error_message,
        #             condition=lambda: isinstance(nonce, bytes))

        # 7. Check encrypted message.
        self.steps.add_step("Check encrypted message")
        error_message = "Encrypted message is not a binary string"
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(encrypted_message, tuple))

        # 8. Decrypt message by 'did.decrypt_sealed'.
        self.steps.add_step("Decrypt message by 'did.decrypt_sealed'")
        decrypted_msg = await utils.perform(self.steps, crypto.anon_decrypt,
                                            self.wallet_handle, their_verkey,
                                            encrypted_message)

        # 9. Check decrypted message.
        self.steps.add_step("Check decrypted message")
        error_msg = "Decrypted message is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: decrypted_msg == message)
