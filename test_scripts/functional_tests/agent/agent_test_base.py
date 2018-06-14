"""
Created on Dec 20, 2017

@author: nhan.nguyen

Containing a base class for agent testing.
"""

from indy import crypto
from utilities import utils, common
from utilities.test_scenario_base import TestScenarioBase


class AgentTestBase(TestScenarioBase):

    message = "Test agent".encode("utf-8")
    sender_verkey = None
    recipient_verkey = None
    encrypted_msg = None

    async def setup_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def teardown_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle,
                                             self.wallet_credentials)

    async def _parsed_and_check_encrypted_msg_auth(self):
        # Parse encrypted_message.
        self.steps.add_step("Parse encrypted message")
        parsed_verkey, parsed_msg = await utils.perform(self.steps,
                                                        crypto.auth_decrypt,
                                                        self.wallet_handle,
                                                        self.recipient_verkey,
                                                        self.encrypted_msg,
                                                        ignore_exception=False)
        # Verify "parsed_msg".
        self.steps.add_step("Verify 'parsed_message'")
        utils.check(self.steps,
                    error_message="'parsed_message' mismatches with "
                                  "original 'message'",
                    condition=lambda: self.message == parsed_msg)

        # Verify "parsed_verkey".
        self.steps.add_step("Verify 'parsed_verkey'")
        utils.check(self.steps,
                    error_message="'parsed_verkey' mismatches with "
                                  "'sender_verkey'",
                    condition=lambda: self.sender_verkey == parsed_verkey)

    async def _parsed_and_check_encrypted_msg_anon(self):
        # Parse encrypted_message.
        self.steps.add_step("Parse encrypted message")
        parsed_msg = await utils.perform(self.steps,
                                         crypto.anon_decrypt,
                                         self.wallet_handle,
                                         self.recipient_verkey,
                                         self.encrypted_msg,
                                         ignore_exception=False)

        # Verify "parsed_msg".
        self.steps.add_step("Verify 'parsed_message'")
        utils.check(self.steps,
                    error_message="'parsed_message' mismatches with "
                                  "original 'message'",
                    condition=lambda: self.message == parsed_msg)
