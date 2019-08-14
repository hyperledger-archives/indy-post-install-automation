"""
Created on Nov 22, 2017

@author: khoi.ngo

Containing the test base class.
"""

import inspect
import os
import time

import pytest

from utilities import utils, constant, common
from utilities.result import Result
from utilities.step import Steps


class TestScenarioBase:
    """
    Test base....
    All test scenario should inherit from this class.
    This class controls the work flow and hold some general test data for test
    scenarios that inherit it.
    """

    def setup_method(self):
        self.test_name = os.path.splitext(
            os.path.basename(inspect.getfile(self.__class__)))[0]
        if pytest.current_id:
            self.test_name = pytest.current_id

        self.test_result = Result(self.test_name)
        self.steps = Steps()
        self.pool_name = utils.generate_random_string("test_pool")
        self.wallet_name = utils.generate_random_string("test_wallet")
        self.pool_handle = None
        self.wallet_handle = None
        self.wallet_credentials = constant.wallet_credentials
        self.pool_genesis_txn_file = constant.pool_genesis_txn_file
        self.begin_time = time.time()
        utils.run_async_method(self.setup_steps)

    def teardown_method(self):
        utils.run_async_method(self.teardown_steps)
        utils.make_final_result(self.test_result,
                                self.steps.get_list_step(),
                                self.begin_time)
        test_result_status = self.test_result.get_test_status()
        utils.print_test_result(self.test_name, test_result_status)

    async def setup_steps(self):
        """
         Execute pre-condition of test scenario.
         If the test case need some extra step in pre-condition
         then just override this method.
        """
        common.clean_up_pool_and_wallet_folder(self.pool_name,
                                               self.wallet_name)

    async def teardown_steps(self):
        """
        Execute post-condition of test scenario.
        If the test case need some extra step in post-condition then
        just override this method.
        """
        await common.clean_up_pool_and_wallet(self.pool_name,
                                              self.pool_handle,
                                              self.wallet_name,
                                              self.wallet_handle,
                                              self.wallet_credentials)
