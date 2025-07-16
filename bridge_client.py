"""
Bridge API Client

HTTP client for interacting with the Bridge API with proper authentication,
error handling, and retry mechanisms.
"""

import requests
import time
import logging
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

from config import Config
from utils.idempotency import generate_idempotency_key
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BridgeAPIError(Exception):
    """Base exception for Bridge API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class BridgeClient:
    """HTTP client for Bridge API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Api-Key': config.api_key
        })
        
        # Configure retries
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
        logger.info(f"Bridge client initialized for {config.environment} environment")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        idempotency_key: Optional[str] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make HTTP request to Bridge API with retry logic"""
        
        url = urljoin(self.config.base_url, endpoint)
        
        # Add idempotency key if provided
        headers = {}
        if idempotency_key:
            headers['Idempotency-Key'] = idempotency_key
        
        logger.debug(f"Making {method} request to {url}")
        if data:
            logger.debug(f"Request data: {data}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=30
            )
            
            logger.debug(f"Response status: {response.status_code}")
            
            # Handle successful responses
            if response.status_code < 400:
                try:
                    return response.json()
                except ValueError:
                    return {'status': 'success', 'data': response.text}
            
            # Handle error responses
            try:
                error_data = response.json()
            except ValueError:
                error_data = {'message': response.text}
            
            error_message = error_data.get('message', f'HTTP {response.status_code} error')
            
            # Handle rate limiting
            if response.status_code == 429 and retry_count < self.max_retries:
                retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params, idempotency_key, retry_count + 1)
            
            # Handle server errors with retry
            if response.status_code >= 500 and retry_count < self.max_retries:
                delay = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                logger.warning(f"Server error {response.status_code}. Retrying after {delay} seconds...")
                time.sleep(delay)
                return self._make_request(method, endpoint, data, params, idempotency_key, retry_count + 1)
            
            raise BridgeAPIError(
                message=error_message,
                status_code=response.status_code,
                response_data=error_data
            )
            
        except requests.exceptions.RequestException as e:
            if retry_count < self.max_retries:
                delay = self.retry_delay * (2 ** retry_count)
                logger.warning(f"Request failed: {e}. Retrying after {delay} seconds...")
                time.sleep(delay)
                return self._make_request(method, endpoint, data, params, idempotency_key, retry_count + 1)
            
            raise BridgeAPIError(f"Request failed: {e}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Make POST request"""
        if idempotency_key is None:
            idempotency_key = generate_idempotency_key()
        return self._make_request('POST', endpoint, data=data, idempotency_key=idempotency_key)
    
    def put(self, endpoint: str, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Make PUT request"""
        if idempotency_key is None:
            idempotency_key = generate_idempotency_key()
        return self._make_request('PUT', endpoint, data=data, idempotency_key=idempotency_key)
    
    def patch(self, endpoint: str, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Make PATCH request"""
        if idempotency_key is None:
            idempotency_key = generate_idempotency_key()
        return self._make_request('PATCH', endpoint, data=data, idempotency_key=idempotency_key)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint)
