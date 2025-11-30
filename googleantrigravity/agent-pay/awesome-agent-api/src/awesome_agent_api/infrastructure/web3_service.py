import json
import os
from typing import Optional
from web3 import Web3
from web3.contract import Contract
from src.awesome_agent_api.exceptions import AwesomeAgentException

class Web3Service:
    def __init__(self, provider_uri: Optional[str] = None):
        self.provider_uri = provider_uri or os.getenv("WEB3_PROVIDER_URI")
        if not self.provider_uri:
            # Fallback to a public RPC if not provided (e.g. for testing)
            # For now, we'll raise an error if not configured, or use a default
            # Assuming Sepolia for now based on context, but ideally should be env var
            pass
        
        self.w3 = Web3(Web3.HTTPProvider(self.provider_uri))
        self.mnee_address = "0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF"
        self._contract: Optional[Contract] = None

    @property
    def contract(self) -> Contract:
        if self._contract is None:
            abi_path = os.path.join(os.path.dirname(__file__), "mnee_abi.json")
            with open(abi_path, "r") as f:
                abi = json.load(f)
            self._contract = self.w3.eth.contract(address=self.mnee_address, abi=abi)
        return self._contract

    def is_connected(self) -> bool:
        return self.w3.is_connected()

    def get_balance(self, address: str) -> float:
        """Get MNEE balance for an address"""
        if not self.is_connected():
            raise AwesomeAgentException("Web3 provider not connected")
        
        # MNEE has 6 decimals (USD-backed usually), but let's check decimals()
        # For efficiency we could cache decimals
        decimals = self.contract.functions.decimals().call()
        balance_wei = self.contract.functions.balanceOf(address).call()
        return balance_wei / (10 ** decimals)

    def verify_transaction(self, tx_hash: str, expected_amount: float, expected_to: str) -> bool:
        """
        Verify that a transaction transferred the expected amount of MNEE to the expected address.
        """
        if not self.is_connected():
            raise AwesomeAgentException("Web3 provider not connected")

        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            if receipt['status'] != 1:
                return False # Transaction failed

            # Parse logs to find Transfer event
            # Topic 0 for Transfer is keccak256("Transfer(address,address,uint256)")
            transfer_event_signature = self.w3.keccak(text="Transfer(address,address,uint256)").hex()
            
            for log in receipt['logs']:
                if log['address'].lower() == self.mnee_address.lower():
                    if log['topics'][0].hex() == transfer_event_signature:
                        # Decode log
                        # topics[1] is from, topics[2] is to
                        to_address = "0x" + log['topics'][2].hex()[-40:]
                        amount_wei = int(log['data'], 16)
                        
                        decimals = self.contract.functions.decimals().call()
                        amount = amount_wei / (10 ** decimals)

                        if to_address.lower() == expected_to.lower() and abs(amount - expected_amount) < 1e-6:
                            return True
            
            return False
        except Exception as e:
            print(f"Error verifying transaction: {e}")
            return False
