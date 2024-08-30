import json
import web3
from web3 import Web3, HTTPProvider

class BorrowingPlatform:
    def __init__(self, ethereum_node, borrowing_contract_address):
        self.ethereum_node = ethereum_node
        self.borrowing_contract_address = borrowing_contract_address
        self.web3 = Web3(HTTPProvider(self.ethereum_node))
        self.contract = self.web3.eth.contract(address=self.borrowing_contract_address, abi=self.get_abi())

    def get_abi(self):
        # Load the borrowing contract ABI from a file or database
        with open("borrowing_contract_abi.json", "r") as f:
            return json.load(f)

    def request_loan(self, user_address, amount, interest_rate):
        # Request a loan from the borrowing platform
        tx_hash = self.contract.functions.requestLoan(user_address, amount, interest_rate).transact({"from": user_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Requested loan of {amount} at {interest_rate}% interest rate for user {user_address}")

    def repay_loan(self, user_address, amount):
        # Repay a loan to the borrowing platform
        tx_hash = self.contract.functions.repayLoan(user_address, amount).transact({"from": user_address})
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Repaid loan of {amount} for user {user_address}")

    def get_loan_status(self, user_address):
        # Get the loan status for a user
        loan_status = self.contract.functions.getLoanStatus(user_address).call()
        print(f"Loan status for user {user_address}: {loan_status}")

# Example usage:
if __name__ == "__main__":
    borrowing_platform = BorrowingPlatform("https://mainnet.infura.io/v3/YOUR_PROJECT_ID", "0x...BorrowingContractAddress")
    user_address = "0x...UserAddress"
    borrowing_platform.request_loan(user_address, 0.5, 10.0)
    borrowing_platform.repay_loan(user_address, 0.2)
    borrowing_platform.get_loan_status(user_address)
