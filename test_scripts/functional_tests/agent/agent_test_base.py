"""
Created on Dec 20, 2017

@author: nhan.nguyen

Containing a base class for agent testing.
"""

from indy import agent
from utilities import utils, common
from utilities.test_scenario_base import TestScenarioBase


class AgentTestBase(TestScenarioBase):
    def __init__(self):
        if self.__class__ is not AgentTestBase:
            super().__init__()
            self.message = "Test agent".encode("utf-8")
            self.sender_verkey = None
            self.recipient_verkey = None
            self.encrypted_msg = None

    async def execute_precondition_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not AgentTestBase:
            super().execute_scenario(time_out)

    async def _parsed_and_check_encrypted_msg(self):
        # Parse encrypted_message.
        self.steps.add_step("Parse encrypted message")
        parsed_verkey, parsed_msg = await utils.perform(self.steps,
                                                        agent.parse_msg,
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
