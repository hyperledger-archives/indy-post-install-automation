"""
Created on Nov 13, 2017

@author: khoi.ngo

Containing all functions that is common among test scenarios.
"""

import json
import os
import shutil
from indy import wallet, pool, ledger, anoncreds, did
from indy.error import IndyError
from utilities import constant, utils, step


async def prepare_pool_and_wallet(pool_name, wallet_name, wallet_credentials,
                                  pool_genesis_txn_file):
    """
    Prepare pool and wallet to use in a test case.

    :param pool_name: Name of the pool ledger configuration.
    :param wallet_name: Name of the wallet.
    :param pool_genesis_txn_file: path of pool_genesis_transaction file.
    :return: The pool handle and the wallet handle were created.
    """
    pool_handle = await \
        create_and_open_pool(pool_name, pool_genesis_txn_file)

    wallet_handle = await \
        create_and_open_wallet(pool_name, wallet_name, wallet_credentials)

    return pool_handle, wallet_handle


async def clean_up_pool_and_wallet(pool_name, pool_handle,
                                   wallet_name, wallet_handle, wallet_credentials):
    """
    Clean up pool and wallet. Using as a post condition of a test case.

    :param pool_name: The name of the pool.
    :param pool_handle: The handle of the pool.
    :param wallet_name: The name of the wallet.
    :param wallet_handle: The handle of the wallet.
    """
    await close_and_delete_wallet(wallet_name, wallet_handle, wallet_credentials)
    await close_and_delete_pool(pool_name, pool_handle)


def clean_up_pool_and_wallet_folder(pool_name, wallet_name):
    """
    Delete pool and wallet folder without using lib-indy.

    :param pool_name: The name of the pool.
    :param wallet_name: The name of the wallet.
    """
    delete_pool_folder(pool_name)
    delete_wallet_folder(wallet_name)


async def build_and_send_nym_request(pool_handle, wallet_handle,
                                     submitter_did, target_did,
                                     target_verkey, alias, role):
    """
    Build a nym request and send it.

    :param pool_handle: pool handle returned by indy_open_pool_ledger.
    :param wallet_handle: wallet handle returned by indy_open_wallet.
    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :param target_verkey: verification key.
    :param alias: alias.
    :param role: Role of a user NYM record.
    :raise Exception if the method has error.
    """
    nym_txn_req = await \
        ledger.build_nym_request(submitter_did, target_did,
                                 target_verkey, alias, role)
    result = await ledger.sign_and_submit_request(pool_handle, wallet_handle,
                                         submitter_did, nym_txn_req)
    return result


async def create_and_open_pool(pool_name, pool_genesis_txn_file):
    """
    Creates a new local pool ledger configuration.
    Then open that pool and return the pool handle that can be used later
    to connect pool nodes.

    :param pool_name: Name of the pool ledger configuration.
    :param pool_genesis_txn_file: Pool configuration json. if NULL, then
    default config will be used.
    :return: The pool handle was created.
    """
    utils.print_header("\nCreate Ledger\n")
    await create_pool_ledger_config(pool_name,
                                    pool_genesis_txn_file)

    utils.print_header("\nOpen pool ledger\n")
    pool_handle = await pool.open_pool_ledger(pool_name, None)
    return pool_handle


async def create_and_open_wallet(pool_name, wallet_name, wallet_credentials):
    """
    Creates a new secure wallet with the given unique name.
    Then open that wallet and get the wallet handle that can
    be used later to use in methods that require wallet access.

    :param pool_name: Name of the pool that corresponds to this wallet.
    :param wallet_name: Name of the wallet.
    :return: The wallet handle was created.
    """
    utils.print_header("\nCreate wallet\n")
    await wallet.create_wallet(pool_name, wallet_name, None, None, wallet_credentials)

    utils.print_header("\nGet wallet handle\n")
    wallet_handle = await wallet.open_wallet(wallet_name, None, wallet_credentials)
    return wallet_handle


async def create_and_open_pool_ledger_for_steps(steps, pool_name,
                                                pool_genesis_txn_file,
                                                pool_config=None):
    """
    Do two common steps within test cases: create and open pool ledger.
    :param steps: list step of test case.
    :param pool_name:
    :param pool_genesis_txn_file: link to config file.
    :param pool_config: (optional)
    :return: pool handle.
    """
    # Create a pool ledger config.
    steps.add_step("Create pool ledger config")
    await utils.perform(steps, create_pool_ledger_config, pool_name,
                        pool_genesis_txn_file, ignore_exception=False)

    # Open pool ledger.
    steps.add_step("Open pool ledger")
    result = await utils.perform(steps, pool.open_pool_ledger, pool_name,
                                 pool_config, ignore_exception=False)

    return result


async def create_and_open_wallet_for_steps(steps, wallet_name, pool_name,
                                           wallet_config=None, xtype=None,
                                           credentials=None,
                                           runtime_config=None):
    """
    Do two common steps within test cases create and open wallet.

    :param steps: list step of test case.
    :param wallet_name:
    :param pool_name:
    :param wallet_config: (optional) use for created wallet
    :param xtype: (optional)
    :param credentials: (optional)
    :param runtime_config: (optional) use for open wallet with
                            some configurations.
    :return: wallet handle. (optional)
    """
    # Create a wallet.
    steps.add_step("Create wallet")
    await utils.perform(steps, wallet.create_wallet, pool_name,
                        wallet_name, xtype, wallet_config, credentials)

    # Open wallet.
    steps.add_step("Open wallet")
    result = await utils.perform(steps, wallet.open_wallet, wallet_name,
                                 runtime_config, credentials)

    return result


async def create_pool_ledger_config(pool_name, pool_genesis_txn_file):
    """
    Create a pool ledger config.

    :param pool_name:
    :param pool_genesis_txn_file: link to config file to create
                                  pool ledger config.
    """
    if os.path.exists(pool_genesis_txn_file) is not True:
        error_message = (constant.Color.FAIL +
                         "\n{}\n".format(constant.ERR_PATH_DOES_NOT_EXIST.
                                         format(pool_genesis_txn_file)) +
                         constant.Color.ENDC)
        raise ValueError(error_message)

    pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_file)})
    await pool.create_pool_ledger_config(pool_name, pool_config)


async def close_and_delete_pool(pool_name, pool_handle):
    """
    Close and delete pool ledger by using libindy.

    :param pool_name:
    :param pool_handle: return by pool.open_pool_ledger.
    """
    if pool_handle:
        try:
            utils.print_header("\nClose pool\n")
            await pool.close_pool_ledger(pool_handle)
        except IndyError as ie:
            utils.print_error(str(ie))

    if pool_name:
        try:
            utils.print_header("\nDelete pool\n")
            await pool.delete_pool_ledger_config(pool_name)
        except IndyError as ie:
            utils.print_error(str(ie))


async def close_and_delete_wallet(wallet_name, wallet_handle, wallet_credentials):
    """
    Close and delete wallet by using libindy.

    :param wallet_name:
    :param wallet_handle: return by wallet.open_wallet.
    :param credentials: (optional) credentials of wallet.
    """
    if wallet_handle:
        try:
            utils.print_header("\nClose wallet\n")
            await wallet.close_wallet(wallet_handle)
        except IndyError as ie:
            utils.print_error(str(ie))

    if wallet_name:
        try:
            utils.print_header("\nDelete wallet\n")
            await wallet.delete_wallet(wallet_name, wallet_credentials)
        except IndyError as ie:
            utils.print_error(str(ie))


def delete_pool_folder(pool_name: str):
    """
    Delete pool folder by os operation.

    :param pool_name:
    """
    if not pool_name:
        return

    work_dir = constant.work_dir
    utils.print_header("\nClean up pool ledger\n")
    if os.path.exists(work_dir + "/pool/" + pool_name):
        try:
            shutil.rmtree(work_dir + "/pool/" + pool_name)
        except IOError as E:
            utils.print_error(str(E))


def delete_wallet_folder(wallet_name: str):
    """
    Delete wallet folder by os operation.

    :param wallet_name:
    """
    if not wallet_name:
        return

    utils.print_header("\nClean up wallet\n")
    work_dir = constant.work_dir
    if os.path.exists(work_dir + "/wallet/" + wallet_name):
        try:
            shutil.rmtree(work_dir + "/wallet/" + wallet_name)
        except IOError as E:
            utils.print_error(str(E))


async def create_and_store_claim(steps: step.Steps, wallet_handle: int,
                                 prover_did: str, cred_offer: str,
                                 cred_def_json: str, secret_name: str, attr_values: str,
                                 store_in_wallet: bool=True,
                                 step_descriptions: list=None,
                                 ignore_exception: bool=False) -> \
        (str, str, str):
    """
    Create and store claim into wallet.

    :param steps: list steps of test case.
    :param wallet_handle: returned by 'wallet.open_wallet'.
    :param prover_did: prover did, returned by 'did.create_and_store_my_did'
    :param claim_offer: a claim offer. Example: {"issuer_did": <did>,
                                                 "schema_seq_no": <schema_no>}
    :param claim_def: claim definition, returned by
                     'anoncreds.issuer_create_and_store_claim_def'.
    :param secret_name: a master secret name.
    :param claim_json: sample claim json.
    :param user_index_revoc: index of revocation registry.
    :param store_in_wallet: (optional) you want to store created
                            claim into wallet or not.
    :param step_descriptions: (optional) descriptions of test case
                              (in case you want to modify it yourself).
    :param ignore_exception: (optional) ignore exception or not.
    :return: created claim request, updated revocation registry json and claim.
    """

    # Create claim request.
    step_des = "Create claim request"
    if step_descriptions and step_descriptions[0]:
        step_des = step_descriptions[0]
    steps.add_step(step_des)
    cred_req, cred_req_meta = await utils.perform(
        steps, anoncreds.prover_create_credential_req, wallet_handle,
        prover_did, cred_offer, cred_def_json, secret_name,
        ignore_exception=ignore_exception)

    # Create claim.
    step_des = "Create claim"
    if step_descriptions and len(step_descriptions) > 1 \
            and step_descriptions[1]:
        step_des = step_descriptions[1]
    steps.add_step(step_des)
    cred_json, cred_revoc_id, revoc_reg_delta_json = await \
        utils.perform(steps, anoncreds.issuer_create_credential,
                      wallet_handle, cred_offer, cred_req,
                      attr_values, None, None,
                      ignore_exception=ignore_exception)

    if store_in_wallet:
        # Store created claim into wallet.
        step_des = "Create claim"
        if step_descriptions and len(step_descriptions) > 2 \
                and step_descriptions[2]:
            step_des = step_descriptions[2]
        steps.add_step(step_des)
        await utils.perform(steps, anoncreds.prover_store_credential,
                            wallet_handle, None, cred_req_meta, cred_json, cred_def_json, None,
                            ignore_exception=ignore_exception)

    return cred_req, revoc_reg_delta_json, cred_json


async def create_and_store_dids_and_verkeys(
        steps: step.Steps, wallet_handle: int, number: int,
        did_jsons: list=None,
        step_descriptions: list=None,
        ignore_exception: bool=False) -> (str, str):
    """
    Create two did.
    :param steps: steps of test case.
    :param wallet_handle: return by 'wallet.open_wallet'.
    :param number: amount of dids and verkeys you want to create.
    :param did_jsons: all json to create did
    :param step_descriptions: step descriptions in case you want to modify.
    :param ignore_exception: ignore raised exception of not.
    :return: a tuple contains all created verkey and did.
    """
    result = []
    for i in range(0, number):
        description = "Create did and verkey"
        did_json = "{}"
        if did_jsons and len(did_jsons) > i and did_jsons[i]:
            did_json = did_jsons[i]
        if (step_descriptions and len(step_descriptions) > i and
                step_descriptions[i]):
            description = step_descriptions[i]
        steps.add_step(description)
        temp = await utils.perform(steps, did.create_and_store_my_did,
                                   wallet_handle, did_json,
                                   ignore_exception=ignore_exception)
        result.append(temp)

    return tuple(result)
