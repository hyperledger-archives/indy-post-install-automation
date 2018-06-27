"""
Created on Jan 31, 2018

@author: nhan.nguyen

Containing 10 test cases (implemented by data driven) to test some cases that
schema is invalid.
"""

import pytest
import json
import copy
from indy import did, ledger
from indy.error import ErrorCode
from utilities.test_scenario_base import TestScenarioBase
from utilities import common, utils, constant


def schema():
    """
    :return: a test schema.
    """
    return copy.deepcopy(constant.gvt_schema['data'])


def generate_invalid_transaction_schemas():
    """
    Generate schemas that make the schema request cannot be built.

    :return: schemas and ids.
    """

    data = list()
    ids = list()

    ids.append("schema_submit_schema_req_fails_with_schema_name_too_long")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['name'] = utils.generate_random_string(size=257)
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_submit_schema_req_fails"
               "_with_schema_name_is_empty_string")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['name'] = ""
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_submit_schema_req_fails_"
               "with_schema_version_is_empty_string")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['version'] = ""
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_submit_schema_req_fails_with_"
               "schema_version_not_contain_only_digit")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['version'] = "v1.0.1"
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_submit_schema_req_fails_with_schema_version_too_long")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['version'] = utils.generate_random_string(size=129)
    temp['err'] = ErrorCode.CommonInvalidStructure

    return data, ids


def generate_common_invalid_structure_schemas():
    """
    Generate schemas that make schema request cannot be submitted to ledger.

    :return: schema and ids.
    """

    data = list()
    ids = list()

    ids.append("schema_build_schema_req_fails_with_missing_schema_version")
    data.append({'data': schema()})
    temp = data[-1]
    del temp['data']['version']
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_build_schema_req_fails_with_missing_schema_attr_names")
    data.append({'data': schema()})
    temp = data[-1]
    del temp['data']['attr_names']
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_build_schema_req_fails_with_schema_version_is_int")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['version'] = 1
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_build_schema_req_fails_with_missing_schema_name")
    data.append({'data': schema()})
    temp = data[-1]
    del temp['data']['name']
    temp['err'] = ErrorCode.CommonInvalidStructure

    ids.append("schema_build_schema_req_fails_with_schema_name_is_int")
    data.append({'data': schema()})
    temp = data[-1]
    temp['data']['name'] = 1
    temp['err'] = ErrorCode.CommonInvalidStructure

    return data, ids


invalid_transaction_data = generate_invalid_transaction_schemas()
invalid_common_structure_data = generate_common_invalid_structure_schemas()


class TestInvalidSchema(TestScenarioBase):

    @pytest.mark.skip
    # Should be completely reworked with anoncreds' schema_json parameterization
    @pytest.mark.parametrize("schema_data",
                             invalid_common_structure_data[0],
                             ids=invalid_common_structure_data[1])
    @pytest.mark.asyncio
    async def test_cannot_build_req_with_invalid_schema(self, schema_data):
        """
        Test all schema that make schema request cannot be built.

        :param schema_data:
        """
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 5. Create and store did of default trustee as 'did_default_trustee'.
        self.steps.add_step("Create and store did of "
                            "default trustee as 'did_default_trustee'")
        did_default_trustee, _ = await utils.perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            json.dumps({'seed': constant.seed_default_trustee}))

        # 6. Build schema request and verify
        # that schema request cannot be built.
        self.steps.add_step("Build schema request and verify "
                            "that schema request cannot be built")
        await utils.perform_with_expected_code(
            self.steps, ledger.build_schema_request, did_default_trustee,
            json.dumps(schema_data['data']), expected_code=schema_data['err'])

    @pytest.mark.skip
    # Should be completely reworked with anoncreds' schema_json parameterization
    @pytest.mark.parametrize("schema_data",
                             invalid_transaction_data[0],
                             ids=invalid_transaction_data[1])
    @pytest.mark.asyncio
    async def test_cannot_submit_req_with_invalid_schema(self, schema_data):
        """
        Test all schema that make the schema request
        cannot be submitted to ledger.

        :param schema_data:
        """
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 5. Create and store did of default trustee as 'did_default_trustee'.
        self.steps.add_step("Create and store did of "
                            "default trustee as 'did_default_trustee'")
        did_default_trustee, _ = await utils.perform(
            self.steps, did.create_and_store_my_did, self.wallet_handle,
            json.dumps({'seed': constant.seed_default_trustee}))

        # 6. Build schema request and store result as 'schema_req'.
        self.steps.add_step("Build schema request and "
                            "store result as 'schema_req'")
        schema_req = await utils.perform(
            self.steps, ledger.build_schema_request, did_default_trustee,
            json.dumps(schema_data['data']))

        # 7. Submit 'schema_req' to ledger and
        # verify that 'schema_req' cannot be submited.
        self.steps.add_step("Submit 'schema_req' to ledger and "
                            "verify that 'schema_req' cannot be submited")
        await utils.perform_with_expected_code(
            self.steps, ledger.sign_and_submit_request,
            self.pool_handle, self.wallet_handle,
            did_default_trustee, schema_req, expected_code=schema_data['err'])
