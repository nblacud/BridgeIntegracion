"""
External Account service for Bridge API

Handles external account management including bank accounts and crypto wallets
"""

import logging
from typing import Dict, Any, List, Optional

from bridge_client import BridgeClient, BridgeAPIError
from models import ExternalAccount, ExternalAccountRequest
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ExternalAccountService:
    """Service for external account operations"""
    
    def __init__(self, client: BridgeClient):
        self.client = client
    
    def create_external_account(self, customer_id: str, account_data: ExternalAccountRequest) -> ExternalAccount:
        """Create a new external account for customer"""
        try:
            response = self.client.post(f'/v0/customers/{customer_id}/external_accounts', account_data.dict())
            logger.info(f"External account created successfully for customer {customer_id}")
            return ExternalAccount(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create external account for customer {customer_id}: {e}")
            raise
    
    def get_external_account(self, customer_id: str, account_id: str) -> ExternalAccount:
        """Get external account by ID"""
        try:
            response = self.client.get(f'/v0/customers/{customer_id}/external_accounts/{account_id}')
            logger.info(f"Retrieved external account: {account_id}")
            return ExternalAccount(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get external account {account_id}: {e}")
            raise
    
    def list_external_accounts(self, customer_id: str, limit: int = 100, cursor: Optional[str] = None) -> Dict[str, Any]:
        """List external accounts for customer"""
        try:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            
            response = self.client.get(f'/v0/customers/{customer_id}/external_accounts', params=params)
            logger.info(f"Listed {len(response.get('data', []))} external accounts for customer {customer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to list external accounts for customer {customer_id}: {e}")
            raise
    
    def update_external_account(self, customer_id: str, account_id: str, update_data: Dict[str, Any]) -> ExternalAccount:
        """Update external account information"""
        try:
            response = self.client.patch(f'/v0/customers/{customer_id}/external_accounts/{account_id}', update_data)
            logger.info(f"External account {account_id} updated successfully")
            return ExternalAccount(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to update external account {account_id}: {e}")
            raise
    
    def delete_external_account(self, customer_id: str, account_id: str) -> Dict[str, Any]:
        """Delete external account"""
        try:
            response = self.client.delete(f'/v0/customers/{customer_id}/external_accounts/{account_id}')
            logger.info(f"External account {account_id} deleted successfully")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to delete external account {account_id}: {e}")
            raise
    
    def verify_external_account(self, customer_id: str, account_id: str, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify external account with micro-deposits"""
        try:
            response = self.client.post(f'/v0/customers/{customer_id}/external_accounts/{account_id}/verify', verification_data)
            logger.info(f"External account {account_id} verification initiated")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to verify external account {account_id}: {e}")
            raise
    
    def get_plaid_link_token(self, customer_id: str) -> Dict[str, Any]:
        """Get Plaid link token for account connection"""
        try:
            response = self.client.post(f'/v0/customers/{customer_id}/plaid_link_token', {})
            logger.info(f"Plaid link token created for customer {customer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create Plaid link token for customer {customer_id}: {e}")
            raise
    
    def connect_plaid_account(self, customer_id: str, plaid_data: Dict[str, Any]) -> Dict[str, Any]:
        """Connect external account via Plaid"""
        try:
            response = self.client.post(f'/v0/customers/{customer_id}/plaid_accounts', plaid_data)
            logger.info(f"Plaid account connected for customer {customer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to connect Plaid account for customer {customer_id}: {e}")
            raise
