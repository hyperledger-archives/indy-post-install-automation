"""
Created on Nov 9, 2017

@author: khoi.ngo

Containing all constants that are necessary to execute test scenario.
"""

import os
import json
import hashlib
from enum import Enum

user_home = os.path.expanduser('~') + os.sep
work_dir = user_home + ".indy_client"
seed_default_trustee = "000000000000000000000000Trustee1"
seed_default_steward = "000000000000000000000000Steward1"
endpoint = "127.0.0.0:9700"
decoded_verkey_length = 32
decoded_did_length = 16
crypto_type = "ed25519"

# Information for seed_my2 = "00000000000000000000000000000My1"
seed_my1 = "00000000000000000000000000000My1"
did_my1 = "VsKV7grR1BUE29mG2Fm2kX"
verkey_my1 = "GjZWsBLgZCR18aL468JAT7w9CZRiBnpxUPPgyQxh4voa"

# Information for seed_my2 = "00000000000000000000000000000My2"
seed_my2 = "00000000000000000000000000000My2"
did_my2 = "2PRyVHmkXQnQzJQKxHxnXC"
verkey_my2 = "kqa2HyagzfMAq42H5f9u3UMwnSBPQx2QfrSyXbUPxMn"

# Constant for anoncreds testing.
gvt_schema_seq = 1
gvt_schema = {
    "seqNo": gvt_schema_seq,
    "data": {
        "name": "gvt",
        "version": "1.0",
        "attr_names": ["age", "sex", "height", "name"],
    }
}

gvt_claim = {
    "sex": ["male", str(int(hashlib.md5("male".encode()).
                            hexdigest(), 16))],
    "name": ["Alex", str(int(hashlib.md5("Alex".encode()).
                             hexdigest(), 16))],
    "height": ["175", str(int(hashlib.md5("175".encode()).
                              hexdigest(), 16))],
    "age": ["28", str(int(hashlib.md5("28".encode()).hexdigest(), 16))]
}

gvt_other_claim = {
    "sex": ["female", str(int(hashlib.md5("female".encode()).
                              hexdigest(), 16))],
    "name": ["Anna", str(int(hashlib.md5("Anna".encode()).
                             hexdigest(), 16))],
    "height": ["160", str(int(hashlib.md5("160".encode()).
                              hexdigest(), 16))],
    "age": ["20", str(int(hashlib.md5("20".encode()).hexdigest(), 16))]
}

xyz_schema_seq = 2
xyz_schema = {
    "seqNo": xyz_schema_seq,
    "data": {
        "name": "xyz",
        "version": "1.0",
        "attr_names": ["period", "status"]
    }
}

xyz_claim = {
    "status": ["partial", str(int(hashlib.md5("partial".encode()).
                                  hexdigest(), 16))],
    "period": ["8", str(int(hashlib.md5("8".encode()).hexdigest(), 16))]
}

signature_type = "CL"
secret_name = "Master secret"
claim_uuid_key = "claim_uuid"   # Change to "referent" in next build

# The path to the genesis transaction file is configurable.
# The default directory is "/var/lib/indy/sandbox/".
genesis_transaction_file_path = "/var/lib/indy/sandbox/"
pool_genesis_txn_file = \
    genesis_transaction_file_path + "pool_transactions_sandbox_genesis"
domain_transactions_sandbox_genesis = \
    genesis_transaction_file_path + "domain_transactions_sandbox_genesis"

original_pool_genesis_txn_file = \
    genesis_transaction_file_path \
    + "original_pool_transactions_sandbox_genesis"

ERR_PATH_DOES_NOT_EXIST = "Cannot find the path specified! \"{}\""
ERR_CANNOT_FIND_ANY_TEST_SCENARIOS = "Cannot find any test scenarios!"
ERR_TIME_LIMITATION = "Aborting test scenario because of time limitation!"
ERR_COMMAND_ERROR = "Invalid command!"
INFO_RUNNING_TEST_POS_CONDITION = "Running clean up for " \
                                  "aborted test scenario."
INFO_TEST_PASS_FAIL = "\033[1m" + "Result:\n" + \
                      "\033[92m" + "Tests pass: {}\n" + "\033[91m" \
                      + "Tests fail: {}" + "\033[0m \n"
INDY_ERROR = "IndyError: {}"
EXCEPTION = "Exception: {}"
JSON_INCORRECT = "Failed. Json response is incorrect. {}"

# JSON template
operation_fields = '"type":"{}","dest":"{}"'

submit_request = '{{"reqId": {:d}, "identifier": "{}", ' \
                 '"operation": {{ "type": "{}", "dest": "{}"}},' \
                 ' "signature": "{}"}}'

submit_response = '{{"result": {{ ' \
                  '"identifier": "{}", "dest": "{}", ' \
                  '"data": "{}","type": "{}" }}, "op": "{}"}}'

node_request = str(operation_fields + ', "data": {}')
message = str(operation_fields + ', "verkey": "{}"')
claim_response = '"ref":1,"data":{},"type":"{}","signature_type":"{}"'
get_claim_response = '"type":"{}","ref":{},"signature_type":"{}","origin":"{}"'
attrib_response = str(operation_fields + ',"raw":{}')
schema_response = str(operation_fields + ',"data":{}')


def json_template(identifier, operation, json_loads=True):
    value = '{{"identifier":"{}","operation":{{{}}}}}'
    if json_loads:
        return json.loads(value.format(identifier, operation))
    else:
        return value.format(identifier, operation)


class Color(str, Enum):
    """
    Class to set the colors for text.
    Syntax:  print(Colors.OKGREEN +"TEXT HERE" +Colors.ENDC)
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Normal default color.
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Role(str, Enum):
    """
    Class to define roles.
    """
    TRUSTEE = "TRUSTEE"
    STEWARD = "STEWARD"
    TRUST_ANCHOR = "TRUST_ANCHOR"
    TGB = "TGB"  # obsolete.
    NONE = ""


class KeysForRevocation(str, Enum):
    G = "g"
    G_DASH = "g_dash"
    H = "h"
    H0 = "h0"
    H1 = "h1"
    H2 = "h2"
    H_TILDE = "htilde"
    H_CAP = "h_cap"
    U = "u"
    PK = "pk"
    Y = "y"
