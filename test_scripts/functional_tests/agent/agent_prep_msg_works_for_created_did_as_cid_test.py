"""
Created on Dec 20, 2017

@author: nhan.nguyen
Verify that user can prepare a message that associates with a created did
as cid.
"""

import json

from indy import agent, signus
import pytest

from test_scripts.functional_tests.agent.agent_test_base import AgentTestBase
from utilities import utils, common


class TestAgentPrepMessageWithCreatedDidAsCid(AgentTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Created wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create "sender_verkey" with
        # "signus.created_and_store_my_did" as cid.
        self.steps.add_step(
            "Create 'sender_verkey' with 'signus.created_and_store_my_did'")
        (_, self.sender_verkey) = await utils.perform(
            self.steps, signus.create_and_store_my_did, self.wallet_handle,
            json.dumps({"cid": True}))

        # 4. Create "recipient_verkey" with "signus.created_and_store_my_did".
        self.steps.add_step(
            "Create 'recipient_verkey' with 'signus.created_and_store_my_did'")
        (_, self.recipient_verkey) = await utils.perform(
            self.steps, signus.create_and_store_my_did, self.wallet_handle,
            "{}", ignore_exception=False)

        # 5. Prepare message.
        self.steps.add_step("Prepare encrypted message")
        self.encrypted_msg = await utils.perform(self.steps, agent.prep_msg,
                                                 self.wallet_handle,
                                                 self.sender_verkey,
                                                 self.recipient_verkey,
                                                 self.message,
                                                 ignore_exception=False)

        # 6. Parsed 'encrypted_message'.
        # 7. Check 'parsed_message'
        # 8. Check 'parsed_verkey'
        await super()._parsed_and_check_encrypted_msg()
