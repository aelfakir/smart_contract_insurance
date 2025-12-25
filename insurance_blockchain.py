import hashlib
import json
from time import time

class InsuranceBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=100, previous_hash='1') # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount, policy_details):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'policy_details': policy_details
        })
        return self.get_last_block()['index'] + 1

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_last_block(self):
        return self.chain[-1]
