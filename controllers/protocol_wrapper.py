from pytezos import Key, Contract, pytezos
from pytezos.operation.result import OperationResult
from decimal import *
import datetime
import requests
import json

class Protocol:
    def __init__(self):
        self.contract = Contract.from_file('./smart_contracts/protocol.tz')
        self.protocol = 'KT1Q72pNNiCnBamwttWvXGE9N2yuz6c7guSD'  
        self.oracle = ''
        self.network = 'mainnet'

    def initialize_contract_instance(self, kt, tz):
        p = pytezos.using(key=tz, shell='https://api.tez.ie/rpc/mainnet/')
        protocol = p.contract(kt)
        return protocol

    def origination(self, tz, network, fa2, oracle):
        
        p = pytezos.using(key=tz, shell=network)
        op = p.origination(script=self.contract.script(storage={"fa2" : fa2, "opensources" : {}, "oracle" : oracle, "paused" : False, "tk_counter" : 1})).autofill()
        forge = op.forge()
        print([op, forge])
        return [op, forge]
    
    def opensource_origin(self, tz, meta, goal):

        protocol = self.initialize_contract_instance(self.protocol, tz)
        return protocol.originate_hicetnuncDAO({"address" : tz, "goal" : goal, 'meta' : meta}).operation_group.json_payload()

    def contribute(self, kt, tz, amount):
        protocol = self.initialize_contract_instance(kt, tz)
        return protocol.contribute(None).with_amount(Decimal(amount)).operation_group.json_payload()

    def withdraw_funds(self, payload):
        protocol = self.initialize_contract_instance(payload['kt'], payload['tz'])
        return protocol.withdraw({"address" : payload['tz'], "amount" : Decimal(payload['amount'])}).operation_group.json_payload()

    def get_opensources(self, contract_i):
        r = requests.get('https://api.better-call.dev/v1/bigmap/{}/{}/keys'.format(self.network, contract_i.storage()['auth']))
        return [ {
            "key" : e['data']['key']['value'],
            "value" : e['data']['value']['value'] # add a tz address + token id record
        } for e in json.loads(r.content) ]

    # administrator
    def update_adm(self, kt, tz, adm):
        protocol = self.initialize_contract_instance(kt, tz)
        return protocol.update_adm(adm).operation_group

    def update_linktree(self, kt, tz, links):
        pass