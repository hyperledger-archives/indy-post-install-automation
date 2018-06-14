"""
Created on Nov 9, 2017
@author: khoi.ngo
Containing all functions used by several test steps on test scenarios.
"""
import os
import json
from indy.error import IndyError
from utilities import constant
from utilities.result import Status
from utilities.step import Steps


def generate_random_string(prefix="", suffix="", size=20):
    """
    Generate random string .
    :param prefix:  (optional) Prefix of a string.
    :param suffix:  (optional) Suffix of a string.
    :param size: (optional) Max length of a string (include prefix and suffix)
    :return: The random string.
    """
    import random
    import string
    left_size = size - len(prefix) - len(suffix)
    random_str = ""
    if left_size > 0:
        random_str = ''.join(
            random.choice(string.ascii_uppercase +
                          string.digits) for _ in range(left_size))
    else:
        print("Warning: Length of prefix and suffix more than %s chars"
              % str(size))
    result = str(prefix) + random_str + str(suffix)
    return result


def get_project_path():
    """
    return the path of the project directory.
    """
    file_path = os.path.abspath(__file__)
    root_dir = os.path.join(os.path.dirname(file_path), "..")
    return os.path.abspath(root_dir)


def compare_json(js1, js2):
    """
    Check whether js1 contain js2.
    :param js1:
    :param js2:
    :return:
    """
    return js1.items() <= js2.items()


async def perform(steps, func, *args, ignore_exception=False):
    """
    Execute an function and set status, message for the last test step depend
    on the result of the function.
    :param steps: list of test steps.
    :param func: executed function.
    :param args: argument of function.
    :param ignore_exception: (optional) raise exception or not.
    :return: the result of function of the exception that the function raise.
    """
    try:
        result = await func(*args)
        steps.get_last_step().set_status(Status.PASSED)
    except IndyError as E:
        print_error(constant.INDY_ERROR.format(str(E)))
        steps.get_last_step().set_status(Status.FAILED, str(E))
        result = E
    except Exception as Ex:
        print_error(constant.EXCEPTION.format(str(Ex)))
        steps.get_last_step().set_status(Status.FAILED, str(Ex))
        result = Ex

    if isinstance(result, Exception) and not ignore_exception:
        raise result

    return result


async def perform_with_expected_code(steps, func, *args, expected_code=0,
                                     ignore_exception=False):
    """
    Execute the "func" with expectation that the "func" raise an IndyError that
    IndyError.error_code = "expected_code".
    :param steps: list of test steps.
    :param func: executed function.
    :param args: arguments of "func".
    :param expected_code: (optional) the error code that you expect
                          in IndyError.
    :param ignore_exception: (optional) raise exception or not.
    :return: exception if the "func" raise it without "expected_code".
             'None' if the "func" run without any exception of the exception
             contain "expected_code".
    """
    try:
        result = await func(*args)
        if isinstance(result, tuple):
            result = result[0]
        if json.loads(result)['op'] == 'REJECT':
            steps.get_last_step().set_status(Status.PASSED)
        elif json.loads(result)['op'] == 'REQNACK':
            steps.get_last_step().set_status(Status.PASSED)
        else:
            message = "Expected exception %s but not." % str(expected_code)
            steps.get_last_step().set_status(Status.FAILED, message)

    except IndyError as E:
        if E.error_code == expected_code:
            steps.get_last_step().set_status(Status.PASSED)
            result = True
        else:
            print_error(constant.INDY_ERROR.format(str(E)))
            steps.get_last_step().set_status(Status.FAILED, str(E))
            result = E

    except KeyError:
        steps.get_last_step().set_status(Status.PASSED)
        result = True

    except Exception as Ex:
        print_error(constant.EXCEPTION.format(str(Ex)))
        steps.get_last_step().set_status(Status.FAILED, str(Ex))
        result = Ex

    if isinstance(result, BaseException) and not ignore_exception:
        raise result
    return result


def run_async_method(method, time_out=None):
    """
    Run async method until it complete or until the time is over.
    :param method: The method want to run with event loop.
    :param time_out:
    @note: We can customize this method to adapt different situations
           in the future.
    """
    import asyncio
    loop = asyncio.get_event_loop()

    if not time_out:
        loop.run_until_complete(method())
    else:
        loop.run_until_complete(asyncio.wait_for(method(), time_out))


def make_final_result(test_result, steps, begin_time):
    """
    Making a test result.
    :param test_result: the object result was collected into test case.
    :param steps: list of steps.
    :param begin_time: time that the test begin.
    """
    import time
    import pytest
    if pytest.current_exception:
        steps[-1].set_status(Status.FAILED, pytest.current_exception)
    test_failed = False
    for step in steps:
        test_result.add_step(step)
        if step.get_status() == Status.FAILED:
            print('%s: ' % str(step.get_id()) + constant.Color.FAIL +
                  'failed\nMessage: ' + step.get_message() +
                  constant.Color.ENDC)
            test_failed = True

    if not test_failed:
        test_result.set_test_passed()
    else:
        test_result.set_test_failed()

    test_result.set_duration(time.time() - begin_time)
    test_result.write_result_to_file()


def verify_json(steps, expected_response, response):
    """
    Verify two json are equal.
    :param steps: list step of test case.
    :param expected_response: expected json.
    :param response: actual json.
    """
    try:
        assert expected_response.items() <= response.items()
        steps.get_last_step().set_status(Status.PASSED)
    except AssertionError as e:
        message = constant.JSON_INCORRECT.format(str(e))
        steps.get_last_step().set_status(Status.FAILED, message)


def check_pool_exist(pool_name: str) -> bool:
    """
    Check whether pool config exist or not.
    :param pool_name:
    :return: bool
    """
    if not pool_name:
        return False
    return os.path.exists(constant.work_dir + "/pool/" + pool_name)


def print_with_color(message: str, color: str):
    """
    Print a message with specified color onto console.
    :param message:
    :param color:
    """
    import sys
    print(color + message + constant.Color.ENDC, file=sys.stderr)


def print_error(message: str):
    """
    Print message onto console with "Fail" color.
    :param message:
    """
    print_with_color(message, constant.Color.FAIL)


def print_header(message: str):
    """
    Print message onto console with "Header" color.
    :param message:
    """
    print_with_color(message, constant.Color.HEADER)


def print_ok_green(message: str):
    """
    Print message onto console with "OK_GREEN" color.
    :param message:
    """
    print_with_color(message, constant.Color.OKGREEN)


def print_ok_blue(message: str):
    """
    Print message onto console with "OK_BLUE" color.
    :param message:
    """
    print_with_color(message, constant.Color.OKBLUE)


def print_test_result(test_name, test_status):
    if test_status == Status.PASSED:
        print_with_color("Test case: {} ----> {}\n".
                         format(test_name, "PASSED"),
                         constant.Color.OKGREEN)
    else:
        print_error("Test case: {} ----> {}\n".format(test_name, "FAILED"))


def check(steps: Steps, error_message: str, condition) -> bool:
    """
    Check if the condition are return True.
    Set message into last step if the condition return False.
    :param steps: list step of test case.
    :param error_message: message to set if condition return False.
    :param condition: a callable.
    :return: True or False depend on result of "condition".
    """
    if steps:
        step = steps.get_last_step()
        if not callable(condition):
            raise ValueError("The 'condition' argument "
                             "must be a callable object")
        else:
            if not condition():
                raise ValueError(error_message)
            else:
                step.set_status(Status.PASSED)
                return True

    return False


def create_claim_offer(issuer_did: str = "", schema_seq: int = None) -> dict:
    """
    Return a claim offer.
    :param issuer_did: create by did.create_and_store_did.
    :param schema_seq:
    :return: claim offer.
    """
    result = {}
    if issuer_did:
        result['issuer_did'] = issuer_did

    if schema_seq:
        result["schema_seq_no"] = schema_seq

    return result


def create_gotten_pairwise_json(my_did: str = None, metadata=None) -> dict:
    """
    Return a pairwise json that gotten from wallet.
    :param my_did:
    :param metadata:
    :return: pairwise json.
    """
    result = {}
    if my_did is not None:
        result['my_did'] = my_did

    if metadata is not None:
        result['metadata'] = metadata

    return result


def check_claim_attrs(claim_attrs, expected_claim):
    """
    Check if field 'attrs' in gotten claim matches with expected claim json.
    :param claim_attrs: value of field 'attrs' in gotten claim.
    :param expected_claim:
    :return: True of False.
    """
    for key in expected_claim.keys():
        if claim_attrs[key] != expected_claim[key][0]:
            return False
    return True


def check_gotten_claim_is_valid(steps, gotten_claim, expected_claim_json,
                                issuer_did, schema_no):
    """
    Check if a gotten claim is valid.
    :param steps: steps of test case.
    :param gotten_claim: return by 'anoncreds.prover_get_claims'.
    :param expected_claim_json: claim json that match with claim in wallet.
    :param issuer_did: return by 'did.create_and_store_my_did'.
    :param schema_no: schema sequence number.
    :return: True or False.
    """
    # Check lst_claims[0]['claim_uuid'].
    steps.add_step("Check lst_claims[0]['{}']".format(constant.claim_uuid_key))
    err_msg = "Claim's uuid is empty"
    check(steps, error_message=err_msg,
          condition=lambda: len(gotten_claim["referent"]) > 0)

    # Check lst_claims[0]['attrs'].
    steps.add_step("Check lst_claims[0]['attrs']")
    claim_attrs = gotten_claim["attrs"]
    err_msg = "lst_claims[0]['attrs'] mismatches"
    check(steps, error_message=err_msg,
          condition=lambda: check_claim_attrs(claim_attrs,
                                              expected_claim_json))

    # Check lst_claims[0]['issuer_did'].
    steps.add_step("Check lst_claims[0]['issuer_did']")
    err_msg = "Issuer's did mismatches"
    check(steps, error_message=err_msg,
          condition=lambda: gotten_claim["issuer_did"] == issuer_did)

    # Check lst_claims[0]['issuer_did'].
    steps.add_step("Check lst_claims[0]['issuer_did']")
    err_msg = "Issuer's did mismatches"
    check(steps, error_message=err_msg,
          condition=lambda: gotten_claim["schema_key"] == constant.gvt_schema_key)


def create_proof_req(nonce: str, name: str, version: str,
                     requested_attrs: dict=None,
                     requested_predicates: dict=None) -> str:
    """
    Create a proof request.
    :param nonce: a number that unique within wallet.
    :param name: name of proof request (unique).
    :param version: version of proof request.
    :param requested_attrs:
            example: {"attr1_referent": {"name": <attr_name>}}
    :param requested_predicates:
            example: {"predicate1_referent": {"attr_name": <attr_name>,
                                              "p_type": <operator>,
                                              "value": "expected_value"}}
    :return: proof request.
    """

    return json.dumps({"nonce": nonce, "name": name, "version": version,
                       "requested_attrs": requested_attrs,
                       "requested_predicates": requested_predicates})


def get_version(program: str) -> str:
    """
    Return version of a program.
    :param program: program's name.
    :return: version.
    """
    import subprocess
    cmd = "dpkg -l | grep '{}'".format(program)
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (out, _) = process.communicate()
    result = out.decode()
    version = result.split()

    if len(version) >= 3:
        if version[1] == program:
            return version[2]
    return "Cannot find version for '{}'".format(program)


def create_folder(folder):
    """
    Create folder if it is not exist.
    :param folder: folder need to create.
    :return:
    """
    import errno
    try:
        os.makedirs(folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
