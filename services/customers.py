"""
Customer service for Bridge API

Handles customer creation, KYC/KYB processes, and customer management
"""

import logging
from typing import Dict, Any, List, Optional

from bridge_client import BridgeClient, BridgeAPIError
from models import Customer, CustomerRequest, TOSLinkResponse
from utils.logger import setup_logger

logger = setup_logger(__name__)

class CustomerService:
    """Service for customer operations"""
    
    def __init__(self, client: BridgeClient):
        self.client = client
    
    def create_tos_link(self, redirect_uri: Optional[str] = None) -> TOSLinkResponse:
        """Create a Terms of Service link for customer"""
        try:
            data = {}
            if redirect_uri:
                data['redirect_uri'] = redirect_uri
            
            response = self.client.post('/v0/customers/tos_links', data)
            logger.info("TOS link created successfully")
            return TOSLinkResponse(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create TOS link: {e}")
            raise
    
    def create_customer(self, customer_data: CustomerRequest) -> Customer:
        """Create a new customer"""
        try:
            response = self.client.post('/v0/customers', customer_data.dict())
            logger.info(f"Customer created successfully with ID: {response.get('id')}")
            return Customer(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to create customer: {e}")
            raise
    
    def get_customer(self, customer_id: str) -> Customer:
        """Get customer by ID"""
        try:
            response = self.client.get(f'/v0/customers/{customer_id}')
            logger.info(f"Retrieved customer: {customer_id}")
            return Customer(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get customer {customer_id}: {e}")
            raise
    
    def list_customers(self, limit: int = 100, cursor: Optional[str] = None) -> Dict[str, Any]:
        """List customers with pagination"""
        try:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            
            response = self.client.get('/v0/customers', params=params)
            logger.info(f"Listed {len(response.get('data', []))} customers")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to list customers: {e}")
            raise
    
    def update_customer(self, customer_id: str, update_data: Dict[str, Any]) -> Customer:
        """Update customer information"""
        try:
            response = self.client.patch(f'/v0/customers/{customer_id}', update_data)
            logger.info(f"Customer {customer_id} updated successfully")
            return Customer(**response)
            
        except BridgeAPIError as e:
            logger.error(f"Failed to update customer {customer_id}: {e}")
            raise
    
    def get_customer_kyc_status(self, customer_id: str) -> Dict[str, Any]:
        """Get KYC status for customer"""
        try:
            response = self.client.get(f'/v0/customers/{customer_id}/kyc_status')
            logger.info(f"Retrieved KYC status for customer: {customer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to get KYC status for customer {customer_id}: {e}")
            raise
    
    def resubmit_customer_kyc(self, customer_id: str, kyc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resubmit KYC information for customer"""
        try:
            response = self.client.post(f'/v0/customers/{customer_id}/kyc_resubmit', kyc_data)
            logger.info(f"KYC resubmitted for customer: {customer_id}")
            return response
            
        except BridgeAPIError as e:
            logger.error(f"Failed to resubmit KYC for customer {customer_id}: {e}")
            raise
