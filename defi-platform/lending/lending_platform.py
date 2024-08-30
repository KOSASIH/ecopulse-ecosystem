import json
import web3
from web3 import Web3, HTTPProvider

class LendingPlatform:
    def __init__(self, ethereum_node, lending_contract_address):
        self.ethereum_node = ethereum_node
        self.lending_contract_address = lending_contract_address
        self.web3 = Web3(HTTPProvider(self.ethereum_node))
        self.contract = self.web3.eth.contract(address=self.lending_contract_address, abi=self.get_abi())

    def get_abi(self):
        # Load the lending contract ABI from a file or database
        with open("lending_contract_abi.json", "r") as f:
            return json.load(f)

    def deposit(self, user_address, amount):
        # Deposit funds into the lending platform
        tx_hash = self.contract.functions.deposit(user_address, amount).transact({"from": user_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Deposited {amount} to lending platform for user {user_address}")

    def lend(self, user_address, amount, interest_rate):
        # Lend funds to another user
        tx_hash = self.contract.functions.lend(user_address, amount, interest_rate).transact({"from": user_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Lent {amount} to user {user_address} at {interest_rate}% interest rate")

    def withdraw(self, user_address, amount):
        # Withdraw funds from the lending platform
        tx_hash = self.contract.functions.withdraw(user_address, amount).transact({"from": user_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Withdrew {amount} from lending platform for user {user_address}")

# Example usage:
if __name__ == "__main__":
    lending_platform = LendingPlatform("https://mainnet.infura.io/v3/YOUR_PROJECT_ID", "0x...LendingContractAddress")
    user_address = "0x...UserAddress"
    lending_platform.deposit(user_address, 1.0)
    lending_platform.lend(user_address, 0.5, 10.0)
    lending_platform.withdraw(user_address, 0.2)
