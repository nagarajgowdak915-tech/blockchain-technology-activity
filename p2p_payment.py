
import hashlib
import json
from datetime import datetime


class PaymentBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def calculate_hash(self, block):
        block_data = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def create_genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": str(datetime.now()),
            "payment": "Genesis Block - Payment System",
            "previous_hash": "0"
        }
        genesis["hash"] = self.calculate_hash(genesis)
        self.chain.append(genesis)

    def add_payment(self, sender, receiver, amount):
        if amount <= 0:
            print("Payment amount must be greater than zero.")
            return

        previous_block = self.chain[-1]

        new_block = {
            "index": len(self.chain),
            "timestamp": str(datetime.now()),
            "payment": {
                "sender": sender,
                "receiver": receiver,
                "amount": amount
            },
            "previous_hash": previous_block["hash"]
        }

        new_block["hash"] = self.calculate_hash(new_block)
        self.chain.append(new_block)
        print("Payment recorded successfully!")

    def display_chain(self):
        print("\n===== PAYMENT BLOCKCHAIN =====")
        for block in self.chain:
            print(json.dumps(block, indent=4))

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            block_data = {
                key: value
                for key, value in current_block.items()
                if key != "hash"
            }

            if self.calculate_hash(block_data) != current_block["hash"]:
                return False

            if current_block["previous_hash"] != previous_block["hash"]:
                return False

        return True


# Run the P2P Payment System
payment_system = PaymentBlockchain()

payment_system.add_payment("Alice", "Bob", 500)
payment_system.add_payment("Bob", "Charlie", 200)

payment_system.display_chain()

print("\n===== BLOCKCHAIN VERIFICATION =====")
if payment_system.verify_chain():
    print("Blockchain is valid!")
else:
    print("Blockchain has been changed!")


# Test whether a changed payment is detected
print("\n===== TAMPERING TEST =====")

payment_system.chain[1]["payment"]["amount"] = 9999

if payment_system.verify_chain():
    print("Blockchain is valid!")
else:
    print("Tampering detected: Blockchain is invalid!")
