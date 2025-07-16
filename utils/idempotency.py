"""
Idempotency key generation utilities

Generates unique idempotency keys for safe API retries
"""

import uuid
import time
from typing import Optional

def generate_idempotency_key(prefix: Optional[str] = None) -> str:
    """
    Generate a unique idempotency key for API requests
    
    Args:
        prefix: Optional prefix for the key
        
    Returns:
        Unique idempotency key string
    """
    timestamp = int(time.time() * 1000)  # milliseconds
    unique_id = str(uuid.uuid4())
    
    if prefix:
        return f"{prefix}_{timestamp}_{unique_id}"
    else:
        return f"{timestamp}_{unique_id}"

def generate_customer_key(customer_id: str) -> str:
    """Generate idempotency key for customer operations"""
    return generate_idempotency_key(f"customer_{customer_id}")

def generate_transfer_key(customer_id: str) -> str:
    """Generate idempotency key for transfer operations"""
    return generate_idempotency_key(f"transfer_{customer_id}")

def generate_wallet_key(customer_id: str) -> str:
    """Generate idempotency key for wallet operations"""
    return generate_idempotency_key(f"wallet_{customer_id}")

def generate_account_key(customer_id: str) -> str:
    """Generate idempotency key for external account operations"""
    return generate_idempotency_key(f"account_{customer_id}")
