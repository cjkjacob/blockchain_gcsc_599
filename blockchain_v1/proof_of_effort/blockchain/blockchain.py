import hashlib
import json, os
from time import time
from .validator import EffortValidator, verify_proof
from .models import TokenLedger, UserWallet  # or wherever you keep models

CHAIN_FILE = "data/chain.json"

class Block:
    def __init__(self, index, effort_data, previous_hash, validated_by, proof, timestamp=None, hash=None):
        self.index = index
        self.timestamp = timestamp or time()
        self.effort_data = effort_data  # includes user_id, task_id, evidence, etc.
        self.validated_by = validated_by
        self.proof = proof  # a dict with both signatures
        self.previous_hash = previous_hash
        self.hash = hash or self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "effort_data": self.effort_data,
            "validated_by": self.validated_by,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def from_dict(data):
        return Block(
            index=data["index"],
            effort_data=data["effort_data"],
            previous_hash=data["previous_hash"],
            validated_by=data["validated_by"],
            proof=data["proof"],
            timestamp=data["timestamp"],
            hash=data["hash"]
        )
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "effort_data": self.effort_data,
            "validated_by": self.validated_by,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }
    
class Blockchain:
    def __init__(self):
        self.chain = []
        self.validator = EffortValidator(min_score=10)
        self.load_chain()

    def create_genesis_block(self):
        genesis_data = {
            "user_id": "genesis",
            "task_id": "genesis_task",
            "effort_type": "none",
            "submission": None,
            "effort_score": 0
        }

        fixed_timestamp = 1710000000.0  # ✅ Hardcoded epoch timestamp

        genesis_block = Block(
            index=0,
            effort_data=genesis_data,
            previous_hash="0",
            validated_by="system",
            proof="genesis",
            timestamp=fixed_timestamp
        )

        self.chain.append(genesis_block)

    def load_chain(self):
        if os.path.exists(CHAIN_FILE):
            with open(CHAIN_FILE, "r") as f:
                data = json.load(f)
                self.chain = [Block.from_dict(block_data) for block_data in data]
        else:
            self.create_genesis_block()

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=2)

    def get_last_block(self):
        return self.chain[-1]
        
    def add_block(self, effort_data, validated_by, proof, user_public_key):
        if not self.validator.is_valid(effort_data, validated_by):
            print("Effort validation failed")
            return None

        # Verify proof again
        if not verify_proof(effort_data, proof["user_signature"], user_public_key):
            print("Proof of effort invalid")
            return None

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            effort_data=effort_data,
            previous_hash=last_block.hash,
            validated_by=validated_by,
            proof=proof
        )

        if self.is_valid_block(new_block, last_block):
            self.chain.append(new_block)
            self.save_chain()
            user_wallet = UserWallet.objects.get(user__username=effort_data["user_id"])
            reward = effort_data.get("effort_score", 0)

            TokenLedger.objects.create(
                user=user_wallet,
                amount=reward,
                source_block_index=new_block.index,
                reason="Reward for validated effort"
            )
            return new_block
        else:
            return None

    def is_valid_block(self, new_block, previous_block):
        if previous_block.index + 1 != new_block.index:
            return False
        if previous_block.hash != new_block.previous_hash:
            return False
        if new_block.hash != new_block.compute_hash():
            return False
        return True
    
    def display_chain(self):
        for block in self.chain:
            print(block.__dict__)

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            if not self.is_valid_block(self.chain[i], self.chain[i-1]):
                return False
        return True