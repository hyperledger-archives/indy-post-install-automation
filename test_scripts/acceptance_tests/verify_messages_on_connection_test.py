"""
Created on Nov 8, 2017

@author: khoi.ngo

Containing test script of test scenario 02: verify messages on connection.

Verify that displayed message on connection is correct.
"""

import pytest
import json
import os

from indy import pool

from utilities.constant import pool_genesis_txn_file, \
    original_pool_genesis_txn_file
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


""" cmds """
back_up_pool_genesis_file = 'sudo cp ' + pool_genesis_txn_file + \
    " " + original_pool_genesis_txn_file
remove_pool_genesis_file = 'sudo rm ' + pool_genesis_txn_file
restore_pool_genesis_file = 'sudo cp ' + \
    original_pool_genesis_txn_file + " " + pool_genesis_txn_file
create_empty_pool_genesis_file = 'sudo touch ' + pool_genesis_txn_file


class TestMessagesOnConnection(TestScenarioBase):

    async def setup_steps(self):
        os.system(back_up_pool_genesis_file)
        os.system(remove_pool_genesis_file)
        os.system(create_empty_pool_genesis_file)

    async def teardown_steps(self):
        os.system(remove_pool_genesis_file)
        os.system(restore_pool_genesis_file)

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create ledger config from genesis txn file
        self.steps.add_step("Create Ledger -> "
                            "Bug: https://jira.hyperledger.org/browse/IS-332")
        pool_config = json.dumps(
            {"genesis_txn": str(self.pool_genesis_txn_file)})
        self.pool_handle = await perform(self.steps,
                                         pool.create_pool_ledger_config,
                                         self.pool_name, pool_config)

        # 2. Open pool ledger -------------------------------------------------
        self.steps.add_step("Open pool ledger")
        bug_is332 = "Bug: https://jira.hyperledger.org/browse/IS-332"
        message_2 = "Failed due to the Bug IS-332" + "\n" + bug_is332
        self.steps.get_last_step().set_status(Status.FAILED, message_2)

        # 3. verifying the message --------------------------------------------
        self.steps.add_step("verifying the message")
        message_3 = "TODO after fix IS-332"
        self.steps.get_last_step().set_status(Status.FAILED, message_3)
