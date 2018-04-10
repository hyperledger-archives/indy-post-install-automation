"""
Created on Dec 20, 2017

@author: nhan.nguyen
Verify that user can parse an authenticated message.
"""

from indy import crypto, did
import pytest

from test_scripts.functional_tests.agent.agent_test_base import AgentTestBase
from utilities import utils, common


class TestAgentParseAuthMessage(AgentTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Created wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create "sender_verkey" with "did.created_and_store_my_did".
        self.steps.add_step(
            "Create 'sender_verkey' with 'did.created_and_store_my_did'")
        (_, self.sender_verkey) = await utils.perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            "{}",  ignore_exception=False)

        # 4. Create "recipient_verkey" with "did.created_and_store_my_did".
        self.steps.add_step(
            "Create 'recipient_verkey' with 'did.created_and_store_my_did'")
        (_, self.recipient_verkey) = await utils.perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            "{}", ignore_exception=False)

        # 5. Prepare message.
        self.steps.add_step("Prepare encrypted message")
        self.encrypted_msg = await utils.perform(self.steps, crypto.auth_crypt,
                                                 self.wallet_handle,
                                                 self.sender_verkey,
                                                 self.recipient_verkey,
                                                 self.message,
                                                 ignore_exception=False)

        # 6. Parsed 'encrypted_message'.
        # 7. Check 'parsed_message'
        # 8. Check 'parsed_verkey'
        await super()._parsed_and_check_encrypted_msg_auth()
