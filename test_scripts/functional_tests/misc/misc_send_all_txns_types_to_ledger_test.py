import json

from indy import anoncreds, did, ledger, blob_storage, pool
import pytest

from test_scripts.functional_tests.misc.misc_test_base \
    import MiscTestBase
from utilities import utils, common, constant


class TestSendAllTxnsTypesToLedger(MiscTestBase):

    @pytest.mark.asyncio
    async def test(self):
        # 1. Create and open pool.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, self.pool_genesis_txn_file)

        # 2. Create and open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name,
                                                    credentials=self.wallet_credentials)

        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        issuer_did, issuer_vk = await utils.perform(self.steps,
                                                    did.create_and_store_my_did,
                                                    self.wallet_handle, "{}")

        # 4. Create 'submitter_did'.
        self.steps.add_step("Create 'submitter_did'")
        await utils.perform(self.steps,
                            did.create_and_store_my_did,
                            self.wallet_handle, "{\"seed\":\"000000000000000000000000Trustee1\"}")

        # 5. Build and send NYM.
        self.steps.add_step("Add issuer to the ledger")
        req = await ledger.build_nym_request(
            constant.did_default_trustee, issuer_did, issuer_vk, alias=None, role='TRUSTEE')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 6. Build and send ATTRIB.
        self.steps.add_step("Add ATTRIB to the ledger")
        req = await ledger.build_get_attrib_request(constant.did_default_trustee, issuer_did,
                                                    'test raw string',
                                                    '',
                                                    '')
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, constant.did_default_trustee, req)

        # 7. Build and send SCHEMA and CRED_DEF.
        self.steps.add_step("Build and send SCHEMA and CRED_DEF")
        schema_id, schema_json = await anoncreds.issuer_create_schema(
            issuer_did, constant.gvt_schema_name, "1.0", constant.gvt_schema_attr_names)
        schema_request = await ledger.build_schema_request(issuer_did, schema_json)
        schema_result = await utils.perform(self.steps,
                                            ledger.sign_and_submit_request,
                                            self.pool_handle, self.wallet_handle, issuer_did, schema_request)

        schema_json = json.loads(schema_json)
        schema_json['seqNo'] = json.loads(schema_result)['result']['txnMetadata']['seqNo']
        schema_json = json.dumps(schema_json)

        cred_def_id, cred_def_json = await \
            anoncreds.issuer_create_and_store_credential_def(self.wallet_handle, issuer_did, schema_json, constant.tag,
                                                             constant.signature_type, constant.config_true)
        req = await ledger.build_cred_def_request(issuer_did, cred_def_json)
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, issuer_did, req)

        # 8. Build and send REVOC_REG_DEF and REVOC_REG_ENTRY.
        self.steps.add_step("Build and send REVOC_REG_DEF and REVOC_REG_ENTRY")
        tails_writer_config = json.dumps({'base_dir': 'tails', 'uri_pattern': ''})
        tails_writer = await blob_storage.open_writer('default', tails_writer_config)

        revoc_reg_def_id, revoc_reg_def_json, revoc_reg_entry_json = \
            await anoncreds.issuer_create_and_store_revoc_reg(
                self.wallet_handle, issuer_did, "CL_ACCUM", 'tag',
                json.loads(cred_def_json)['id'],
                json.dumps({"max_cred_num": 10, "issuance_type": "ISSUANCE_ON_DEMAND"}),
                tails_writer)

        revoc_reg_def_req = await ledger.build_revoc_reg_def_request(issuer_did, revoc_reg_def_json)
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, issuer_did, revoc_reg_def_req)

        revoc_reg_entry_req = await ledger.build_revoc_reg_entry_request(
            issuer_did, revoc_reg_def_id, "CL_ACCUM", revoc_reg_entry_json)
        await utils.perform(self.steps,
                            ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, issuer_did, revoc_reg_entry_req)
