"""
Wallet service for Bridge API

Handles custodial wallet operations including balance management and wallet creation
"""

import logging
from typing import Dict, Any, List, Optional

from bridge_client import BridgeClient, BridgeAPIError
from models import Wallet
from utils.logger import setup_logger

logger = setup_logger(__name__)

class WalletService:
    """Service for wallet operations"""
    
    def __init__(self, client: BridgeClient):
        self.client = client
    
    def create_wallet(self, customer_id: str, currency: str) -> Wallet:
        """Create a new custodial wallet for customer"""
        try:
            data = {
                'customer_id': customer_id,
                'currency': currency
            }
            response = self.client.post('/v0/wallets', data)
            logger.info(f"Wallet created successfully for customer {customer_id}")
            return Wallet(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create wallet for customer {customer_id}: {e}")
            raise
    
    def get_wallet(self, wallet_id: str) -> Wallet:
        """Get wallet by ID"""
        try:
            response = self.client.get(f'/v0/wallets/{wallet_id}')
            logger.info(f"Retrieved wallet: {wallet_id}")
            return Wallet(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get wallet {wallet_id}: {e}")
            raise
    
    def list_wallets(self, customer_id: Optional[str] = None, limit: int = 100, cursor: Optional[str] = None) -> Dict[str, Any]:
        """List wallets with pagination"""
        try:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            if customer_id:
                params['customer_id'] = customer_id
            
            response = self.client.get('/v0/wallets', params=params)
            logger.info(f"Listed {len(response.get('data', []))} wallets")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to list wallets: {e}")
            raise
    
    def get_wallet_balance(self, wallet_id: str) -> Dict[str, Any]:
        """Get wallet balance"""
        try:
            response = self.client.get(f'/v0/wallets/{wallet_id}/balance')
            logger.info(f"Retrieved balance for wallet: {wallet_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get balance for wallet {wallet_id}: {e}")
            raise
    
    def get_wallet_transactions(self, wallet_id: str, limit: int = 100, cursor: Optional[str] = None) -> Dict[str, Any]:
        """Get wallet transaction history"""
        try:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            
            response = self.client.get(f'/v0/wallets/{wallet_id}/transactions', params=params)
            logger.info(f"Retrieved {len(response.get('data', []))} transactions for wallet: {wallet_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get transactions for wallet {wallet_id}: {e}")
            raise
    
    def transfer_from_wallet(self, wallet_id: str, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transfer funds from wallet"""
        try:
            response = self.client.post(f'/v0/wallets/{wallet_id}/transfer', transfer_data)
            logger.info(f"Transfer initiated from wallet: {wallet_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to transfer from wallet {wallet_id}: {e}")
            raise
    
    def get_wallet_address(self, wallet_id: str, currency: str) -> Dict[str, Any]:
        """Get wallet address for specific currency"""
        try:
            params = {'currency': currency}
            response = self.client.get(f'/v0/wallets/{wallet_id}/address', params=params)
            logger.info(f"Retrieved address for wallet {wallet_id} currency {currency}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get address for wallet {wallet_id}: {e}")
            raise
