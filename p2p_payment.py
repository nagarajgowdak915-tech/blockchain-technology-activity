import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, transaction, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transaction": self.transaction,
            "previous_hash": self.previous_hash
        }

        encoded_data = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_data).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            time.time(),
            {"message": "Genesis Block Created"},
            "0"
        )
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }

        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            time.time(),
            transaction,
            previous_block.hash
        )

        self.chain.append(new_block)
        print("\nPayment successfully recorded!")

    def display_blockchain(self):
        print("\n===== BLOCKCHAIN DETAILS =====")

        for block in self.chain:
            print("\nBlock Number:", block.index)
            print("Timestamp:", block.timestamp)
            print("Transaction:", block.transaction)
            print("Previous Hash:", block.previous_hash)
            print("Current Hash:", block.hash)

    def verify_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


# Main Program
blockchain = Blockchain()

print("===== P2P PAYMENT SYSTEM =====")

while True:
    print("\n1. Make Payment")
    print("2. Display Blockchain")
    print("3. Verify Blockchain")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        sender = input("Enter Sender Name: ")
        receiver = input("Enter Receiver Name: ")

        try:
            amount = float(input("Enter Amount: "))

            if amount <= 0:
                print("Enter a valid positive amount!")
                continue

            blockchain.add_transaction(sender, receiver, amount)

        except ValueError:
            print("Please enter a valid amount!")

    elif choice == "2":
        blockchain.display_blockchain()

    elif choice == "3":
        print("\n===== BLOCKCHAIN VERIFICATION =====")

        if blockchain.verify_blockchain():
            print("Blockchain is valid!")
        else:
            print("Blockchain is invalid!")

    elif choice == "4":
        print("Thank you for using P2P Payment System!")
        break

    else:
        print("Invalid choice! Please try again.")
