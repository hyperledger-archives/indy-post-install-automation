"""
Created on Dec 22, 2017

@author: nhan.nguyen

Verify that an anonymous encrypted message can be decrypted.
"""

import pytest
import json

from indy import signus
from utilities import utils, common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestDecryptSealedWithValidData(SignusTestBase):
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
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Store 'their_did' and 'their_verkey' into wallet.
        self.steps.add_step("Store 'their_did' and 'their_verkey' into wallet")
        their_did_json = json.dumps({"did": their_did, "verkey": their_verkey})
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle, their_did_json)

        # 5. Encrypte message by 'signus.encrypt_sealed'
        self.steps.add_step("Encrypte message by 'signus.encrypt_sealed' -> "
                            "Bug: https://jira.hyperledger.org/browse/IS-508")
        message = "Test signus".encode("utf-8")
        (encrypted_message, nonce) = await utils.perform(
            self.steps, signus.encrypt_sealed, self.wallet_handle, -1,
            their_did, message)

        # 6. Decrypt message by 'signus.decrypt_sealed'.
        self.steps.add_step("Decrypt message by 'signus.decrypt_sealed'")
        decrypted_msg = await utils.perform(self.steps, signus.decrypt_sealed,
                                            self.wallet_handle, their_did,
                                            encrypted_message)

        # 7. Check decrypted message.
        self.steps.add_step("Check decrypted message")
        error_msg = "Decrypted message is incorrect"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: decrypted_msg == message)
