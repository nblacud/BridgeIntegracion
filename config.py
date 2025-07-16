"""
Configuration management for Bridge API integration
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration class for Bridge API client"""
    
    api_key: str
    environment: str = 'production'
    debug: bool = False
    
    @property
    def base_url(self) -> str:
        """Get base URL based on environment"""
        if self.environment == 'production':
            return 'https://api.bridge.xyz'
        else:
            return 'https://api.bridge.xyz'  # Bridge uses same URL for sandbox
    
    @property
    def dashboard_url(self) -> str:
        """Get dashboard URL based on environment"""
        if self.environment == 'production':
            return 'https://dashboard.bridge.xyz'
        else:
            return 'https://dashboard.bridge.xyz'
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables"""
        api_key = os.getenv('BRIDGE_API_KEY')
        if not api_key:
            raise ValueError("BRIDGE_API_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            environment=os.getenv('BRIDGE_ENVIRONMENT', 'production'),
            debug=os.getenv('BRIDGE_DEBUG', 'false').lower() == 'true'
        )

# Default configuration
DEFAULT_CONFIG = Config(
    api_key=os.getenv('BRIDGE_API_KEY', ''),
    environment=os.getenv('BRIDGE_ENVIRONMENT', 'production'),
    debug=os.getenv('BRIDGE_DEBUG', 'false').lower() == 'true'
)
