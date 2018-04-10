"""
Created on Feb 1, 2018

@author: khoi.ngo

Implementing negative test cases of get_schema.
"""
import json

from indy import did, ledger
from indy.error import ErrorCode
import pytest

from utilities import common
from utilities.constant import seed_default_trustee
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, generate_random_string, \
    perform_with_expected_code


def generate_argvalues_and_ids():
    argvalues = []
    ids = list()
    err = ErrorCode.CommonInvalidStructure

    ids.append("IS_549_build_get_schema_fail_due_to_invalid_version")
    argvalues.append(("", "", '{"name":"valid_name", "version":"1ab.0"}', err))

    ids.append("IS_550_build_get_schema_fail_due_to_special_character")
    argvalues.append(("", "", '{"name":"name!@##$%", "version":"1.1"}', err))

    ids.append("build_get_schema_fail_since_miss_required_fields")
    argvalues.append(("", "", '{"version":"1.1.0"}', err))

    ids.append("IS_551_build_get_schema_fail_due_to_the_empty_values")
    argvalues.append(("", "", '{"name":"", "version":"1.1"}', err))

    ids.append("build_get_schema_fail_due_to_duplicate_field")
    argvalues.append(("", "", '{"name":"valid", "name":"other_name", \
                    "version":"1.1"}', err))

    ids.append("build_get_schema_fail_since_schema_did_is_incorrect")
    argvalues.append(("", "DFSD@#@$@#$", '{"name":"name", "version":"1.1"}',
                      err))

    ids.append("build_get_schema_fail_since_submitter_did_is_incorrect")
    argvalues.append(("DFSD@#@$@#$", "", '{"name":"name", "version":"1.1"}',
                      err))

    ids.append("build_get_schema_fail_since_data_is_none")
    argvalues.append(("", "", '{}', err))

    ids.append("build_get_schema_fail_since_version_has_more_than_128_chars")
    argvalues.append(("", "", '{"name":"128 characters", \
                    "version":"1321321321321231325456"\
                              "31213213616546545213212312.3121321321"\
                              "32132132132132123132132.13213131"\
                              "3213213213212132132213515.3135148766"}', err))

    return argvalues, ids


class TestNegativeGetSchemaRequest(TestScenarioBase):

    # IS-540 is not fixed.

    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_bug_is540(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create DID")
        (submitter_did, _) = \
            await perform(self.steps,
                          did.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": seed_trustee_2}))
        (schema_did, _) = await perform(self.steps,
                                        did.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({
                                            "seed": seed_default_trustee}))
        # 3. build schema request
        self.steps.add_step("Build schema request")
        name = generate_random_string(size=4)
        version = "1.1.1"
        print("name request: " + name)
        data_request = \
            ('{"name":"%s", "version":"%s", "attr_names":["name","male"]}' % (
              name, version))
        schema_req = await perform(self.steps, ledger.build_schema_request,
                                   submitter_did, data_request)

        # 4. send schema request
        self.steps.add_step("send schema request")
        await perform(self.steps, ledger.sign_and_submit_request,
                      self.pool_handle, self.wallet_handle,
                      submitter_did, schema_req)

        # 5. Prepare data to check and build get schema request
        self.steps.add_step("build get schema request")
        data_get_schema = ('{"name":"%s", "version":"%s"}' % (name, version))
        get_schema_req = await perform(self.steps,
                                       ledger.build_get_schema_request,
                                       submitter_did, schema_did,
                                       data_get_schema)

        # 6. send get_schema request
        self.steps.add_step("send get schema request")
        result = await perform(self.steps, ledger.sign_and_submit_request,
                               self.pool_handle, self.wallet_handle,
                               submitter_did, get_schema_req)

        # 6. verify result
        self.steps.add_step("verify result")
        if not isinstance(result, Exception):
            err_msg = ("result is should the error code instead of %s" %
                       (str(result)))
            self.steps.get_last_step().set_status(Status.FAILED, err_msg)
            assert False
        else:
            self.steps.get_last_step().set_status(Status.PASSED)

    data_test = generate_argvalues_and_ids()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("argvalues", data_test[0], ids=data_test[1])
    async def test_negative_cases(self, argvalues):
        # 0. initial data
        submitter_did = argvalues[0]
        schema_did = argvalues[1]
        data = argvalues[2]
        expected_result = argvalues[3]

        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        if not submitter_did:
            (submitter_did, _) = await perform(
                self.steps, did.create_and_store_my_did, self.wallet_handle,
                json.dumps({"seed": seed_default_trustee}))
        if not schema_did:
            seed_trustee_2 = "000000000000000000000000Trustee2"
            (schema_did, _) = await perform(self.steps,
                                            did.create_and_store_my_did,
                                            self.wallet_handle,
                                            json.dumps({
                                                "seed": seed_trustee_2}))

        # 3. build get schema request
        self.steps.add_step("Build schema request")
        result = await perform_with_expected_code(
            self.steps, ledger.build_get_schema_request,
            submitter_did, schema_did, data,
            expected_code=expected_result)
