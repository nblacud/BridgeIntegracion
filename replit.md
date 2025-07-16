# Bridge API Integration Application

## Overview

This is a comprehensive Python application for interacting with the Bridge API, providing customer management, transfer operations, wallet management, and external account handling. The application is structured as a CLI tool with modular services and comprehensive error handling, designed for both sandbox testing and production use.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### July 16, 2025 - Bridge API Integration Complete
- ✅ Built comprehensive Python CLI application for Bridge API
- ✅ Implemented all core Bridge API functionality
- ✅ Added customer management (KYC/KYB, TOS links)
- ✅ Added transfer operations (fiat-to-crypto, crypto-to-fiat, crypto-to-crypto)
- ✅ Added wallet management (custodial wallets, balances, transactions)
- ✅ Added external account management (bank accounts, Plaid integration)
- ✅ Configured for sandbox testing environment
- ✅ Added comprehensive error handling and retry logic
- ✅ Created detailed CLI interface with all Bridge API features
- ✅ Added extensive documentation and usage examples

## System Architecture

### Core Architecture
- **CLI-based Application**: Command-line interface using Click framework
- **Service-Oriented Architecture**: Modular services for different API endpoints
- **HTTP Client Layer**: Centralized API client with authentication and retry logic
- **Model Layer**: Pydantic models for data validation and serialization
- **Configuration Management**: Environment-based configuration system

### Key Technologies
- **Python 3.x**: Primary programming language
- **Click**: CLI framework for command-line interface
- **Pydantic**: Data validation and serialization
- **Requests**: HTTP client for API communication
- **Python-dotenv**: Environment variable management

## Key Components

### 1. Bridge API Client (`bridge_client.py`)
- Centralized HTTP client for all Bridge API interactions
- Handles authentication via API key headers
- Implements retry logic with exponential backoff
- Comprehensive error handling with custom exceptions
- Supports both sandbox and production environments

### 2. Configuration System (`config.py`)
- Environment-based configuration management
- Supports sandbox and production environments
- Loads API keys and settings from environment variables
- Provides base URLs for different environments

### 3. Data Models (`models.py`)
- Pydantic models for all Bridge API data structures
- Includes customer, transfer, wallet, and external account models
- Enum definitions for status types, currencies, and payment rails
- Input validation and serialization

### 4. Service Layer (`services/`)
- **CustomerService**: Customer creation, KYC/KYB processing, TOS management
- **TransferService**: Transfer operations (fiat-to-crypto, crypto-to-fiat, crypto-to-crypto)
- **WalletService**: Custodial wallet creation and management
- **ExternalAccountService**: Bank account and crypto wallet management

### 5. CLI Interface (`cli/`)
- **customers_cli**: Customer management commands
- **transfers_cli**: Transfer operation commands
- **wallets_cli**: Wallet management commands
- **accounts_cli**: External account management commands

### 6. Utilities (`utils/`)
- **Idempotency**: Unique key generation for safe API retries
- **Logger**: Structured logging with consistent formatting

## Data Flow

### Customer Onboarding Flow
1. Create Terms of Service link
2. Customer accepts TOS (external process)
3. Create customer with KYC/KYB information
4. Customer undergoes verification process
5. Create custodial wallets and external accounts as needed

### Transfer Flow
1. Validate customer and account information
2. Create transfer request with source and destination
3. Bridge API processes transfer
4. Monitor transfer status
5. Handle completion or failure

### Wallet Management Flow
1. Create custodial wallet for customer
2. Manage wallet balances
3. Support multiple currencies (USD, USDC, USDT)
4. Handle wallet operations and queries

## External Dependencies

### Bridge API
- Primary integration target
- Handles customer KYC/KYB, transfers, and wallet management
- Sandbox environment for testing
- Production environment for live operations

### Payment Rails Supported
- **Fiat**: ACH, Wire transfers
- **Crypto**: Polygon, Ethereum, Arbitrum, Base networks

### Supported Currencies
- **Fiat**: USD
- **Crypto**: USDC, USDT

## Deployment Strategy

### Environment Configuration
- Sandbox environment for development and testing
- Production environment for live operations
- Environment variables for sensitive configuration
- Configurable debug logging

### Error Handling
- Comprehensive exception handling throughout the application
- Custom `BridgeAPIError` for API-specific errors
- Structured logging for debugging and monitoring
- Retry mechanisms for transient failures

### Security Considerations
- API key authentication
- Environment variable management for sensitive data
- Idempotency keys for safe retry operations
- Input validation using Pydantic models

### CLI Usage
The application provides a command-line interface with the following structure:
- `customers`: Customer management operations
- `transfers`: Transfer operations
- `wallets`: Wallet management
- `accounts`: External account management

Each command group includes create, get, list, and update operations as appropriate for the resource type.

### Testing Support
- Full sandbox environment support
- Comprehensive logging for debugging
- Structured error messages
- Idempotency support for safe testing