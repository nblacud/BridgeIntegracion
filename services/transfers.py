"""
Transfer service for Bridge API

Handles transfer operations including fiat-to-crypto, crypto-to-fiat, and crypto-to-crypto
"""

import logging
from typing import Dict, Any, List, Optional

from bridge_client import BridgeClient, BridgeAPIError
from models import Transfer, TransferRequest
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TransferService:
    """Service for transfer operations"""
    
    def __init__(self, client: BridgeClient):
        self.client = client
    
    def create_transfer(self, transfer_data: TransferRequest) -> Transfer:
        """Create a new transfer"""
        try:
            response = self.client.post('/v0/transfers', transfer_data.dict())
            logger.info(f"Transfer created successfully with ID: {response.get('id')}")
            return Transfer(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create transfer: {e}")
            raise
    
    def get_transfer(self, transfer_id: str) -> Transfer:
        """Get transfer by ID"""
        try:
            response = self.client.get(f'/v0/transfers/{transfer_id}')
            logger.info(f"Retrieved transfer: {transfer_id}")
            return Transfer(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get transfer {transfer_id}: {e}")
            raise
    
    def list_transfers(self, limit: int = 100, cursor: Optional[str] = None, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """List transfers with pagination"""
        try:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            if customer_id:
                params['customer_id'] = customer_id
            
            response = self.client.get('/v0/transfers', params=params)
            logger.info(f"Listed {len(response.get('data', []))} transfers")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to list transfers: {e}")
            raise
    
    def cancel_transfer(self, transfer_id: str) -> Dict[str, Any]:
        """Cancel a pending transfer"""
        try:
            response = self.client.post(f'/v0/transfers/{transfer_id}/cancel', {})
            logger.info(f"Transfer {transfer_id} cancelled successfully")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to cancel transfer {transfer_id}: {e}")
            raise
    
    def get_transfer_receipt(self, transfer_id: str) -> Dict[str, Any]:
        """Get transfer receipt"""
        try:
            response = self.client.get(f'/v0/transfers/{transfer_id}/receipt')
            logger.info(f"Retrieved receipt for transfer: {transfer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get receipt for transfer {transfer_id}: {e}")
            raise
    
    def estimate_transfer_fee(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate transfer fee"""
        try:
            response = self.client.post('/v0/transfers/estimate_fee', transfer_data)
            logger.info("Transfer fee estimated successfully")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to estimate transfer fee: {e}")
            raise
    
    def get_quote(self, source_currency: str, destination_currency: str, amount: str) -> Dict[str, Any]:
        """Get exchange rate quote"""
        try:
            params = {
                'source_currency': source_currency,
                'destination_currency': destination_currency,
                'amount': amount
            }
            response = self.client.get('/v0/quotes', params=params)
            logger.info(f"Quote retrieved for {source_currency} to {destination_currency}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get quote: {e}")
            raise
