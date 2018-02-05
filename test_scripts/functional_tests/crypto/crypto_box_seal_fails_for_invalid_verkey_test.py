"""
Created on Jan 2, 2018

@author: nhan.nguyen

Verify that user cannot encrypt message with invalid verkey.
"""

import pytest
from indy import crypto
from indy.error import ErrorCode
from utilities import utils
from utilities.test_scenario_base import TestScenarioBase


class TestCryptoBoxSealWithInvalidKey(TestScenarioBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create sealed crypto box with invalid verkey and
        # verify that sealed crypto box cannot be created.
        self.steps.add_step("Create sealed crypto box with invalid verkey and "
                            "verify that sealed crypto box cannot be created")
        msg = "Testcrypto"
        invalid_key = "CnEDk___MnmiHXEV1WFgbV___eYnPqs___TdcZaNhFVW"
        error_code = ErrorCode.CommonInvalidStructure
        await utils.perform_with_expected_code(self.steps,
                                               crypto.crypto_box_seal,
                                               invalid_key, msg,
                                               expected_code=error_code)
