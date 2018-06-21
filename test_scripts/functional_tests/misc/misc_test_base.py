from utilities import common
from utilities.test_scenario_base import TestScenarioBase


class MiscTestBase(TestScenarioBase):

    async def setup_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def teardown_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle,
                                             self.wallet_credentials)