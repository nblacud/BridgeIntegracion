# Bridge API Integration Application

A comprehensive Python application for interacting with the Bridge API. This application supports customer management, transfers, wallet operations, and external account management with full sandbox testing capabilities.

## Features

- **Customer Management**: Create, update, and manage customers with KYC/KYB processing
- **Transfer Operations**: Support for fiat-to-crypto, crypto-to-fiat, and crypto-to-crypto transfers
- **Wallet Management**: Custodial wallet creation and management
- **External Accounts**: Bank account and crypto wallet management
- **Sandbox Testing**: Full sandbox environment support for testing
- **CLI Interface**: Easy-to-use command-line interface for all operations
- **Comprehensive Error Handling**: Detailed error messages and retry mechanisms
- **Logging**: Structured logging for debugging and monitoring

## Installation

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install requests pydantic click python-dotenv
   ```

3. Copy the environment file and configure your API key:
   ```bash
   cp .env.example .env
   # Edit .env with your Bridge API key
   ```

## Configuration

Set your Bridge API key in the `.env` file:

```env
BRIDGE_API_KEY=your_bridge_api_key_here
BRIDGE_ENVIRONMENT=sandbox
BRIDGE_DEBUG=false
```

## Getting Started

1. First, get your Bridge API key from the [Bridge Dashboard](https://dashboard.bridge.xyz/)
2. Update the `.env` file with your API key
3. Test the connection:
   ```bash
   python main.py --api-key your_api_key_here status
   ```

## Usage

The CLI supports the following main commands:

### Customer Management

```bash
# Create a Terms of Service link
python main.py customers create-tos-link

# Create a new customer (example for US individual)
python main.py customers create \
  --type individual \
  --first-name John \
  --last-name Doe \
  --email john@example.com \
  --birth-date 1990-01-01 \
  --signed-agreement-id <tos_agreement_id> \
  --address-line1 "123 Main St" \
  --city "New York" \
  --state "NY" \
  --postal-code "10001" \
  --country "USA" \
  --id-type ssn \
  --id-country usa \
  --id-number "123-45-6789"

# List customers
python main.py customers list

# Get customer details
python main.py customers get <customer_id>

# Check KYC status
python main.py customers kyc-status <customer_id>
```

### External Account Management

```bash
# Create a bank account
python main.py accounts create \
  --customer-id <customer_id> \
  --currency usd \
  --account-type us \
  --bank-name "Chase Bank" \
  --account-name "John Checking" \
  --first-name John \
  --last-name Doe \
  --owner-type individual \
  --owner-name "John Doe" \
  --routing-number "021000021" \
  --account-number "1234567890" \
  --account-subtype checking \
  --address-line1 "123 Main St" \
  --city "New York" \
  --state "NY" \
  --postal-code "10001" \
  --country "USA"

# List external accounts
python main.py accounts list <customer_id>

# Get Plaid link token
python main.py accounts plaid-token <customer_id>
```

### Wallet Management

```bash
# Create a custodial wallet
python main.py wallets create --customer-id <customer_id> --currency usdc

# List wallets
python main.py wallets list --customer-id <customer_id>

# Get wallet details
python main.py wallets get <wallet_id>

# Get wallet balance
python main.py wallets balance <wallet_id>

# Get wallet transactions
python main.py wallets transactions <wallet_id>

# Get wallet address
python main.py wallets address <wallet_id> --currency usdc
```

### Transfer Operations

```bash
# Create a transfer (crypto to fiat example)
python main.py transfers create \
  --amount "100.00" \
  --customer-id <customer_id> \
  --source-rail polygon \
  --source-currency usdc \
  --source-address "0x..." \
  --dest-rail wire \
  --dest-currency usd \
  --dest-account-id <external_account_id>

# List transfers
python main.py transfers list

# Get transfer details
python main.py transfers get <transfer_id>

# Cancel a transfer
python main.py transfers cancel <transfer_id>

# Get transfer receipt
python main.py transfers receipt <transfer_id>

# Get exchange rate quote
python main.py transfers quote --source-currency usdc --dest-currency usd --amount 100
```

## Project Structure

```
├── cli/                    # CLI command modules
│   ├── customers.py        # Customer management commands
│   ├── transfers.py        # Transfer operation commands
│   ├── wallets.py          # Wallet management commands
│   └── accounts.py         # External account commands
├── services/               # API service modules
│   ├── customers.py        # Customer service
│   ├── transfers.py        # Transfer service
│   ├── wallets.py          # Wallet service
│   └── external_accounts.py # External account service
├── utils/                  # Utility modules
│   ├── idempotency.py      # Idempotency key generation
│   └── logger.py           # Logging utilities
├── bridge_client.py        # HTTP client for Bridge API
├── config.py              # Configuration management
├── models.py              # Pydantic data models
└── main.py                # Main CLI application
```

## Supported Operations

### Customer Operations
- Create Terms of Service links
- Create and manage customers (individual/business)
- Handle KYC/KYB processes
- Check customer status and details

### Transfer Operations
- Fiat-to-crypto transfers (on-ramps)
- Crypto-to-fiat transfers (off-ramps)
- Crypto-to-crypto transfers
- Transfer status tracking and receipts
- Exchange rate quotes

### Wallet Operations
- Create custodial wallets
- Check wallet balances
- View transaction history
- Generate wallet addresses

### External Account Operations
- Add bank accounts
- Plaid integration for account linking
- Account verification and management

## Error Handling

The application includes comprehensive error handling:
- Automatic retries with exponential backoff
- Detailed error messages
- Idempotency key generation for safe retries
- Structured logging for debugging

## Development

### Testing with Sandbox

The application defaults to the sandbox environment. All operations can be tested safely without affecting real funds or data.

### Logging

Enable debug logging with the `--debug` flag:
```bash
python main.py --debug customers list
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BRIDGE_API_KEY` | Your Bridge API key | Required |
| `BRIDGE_ENVIRONMENT` | Environment (`sandbox` or `production`) | `sandbox` |
| `BRIDGE_DEBUG` | Enable debug logging | `false` |

## API Documentation

For detailed API documentation, visit: https://apidocs.bridge.xyz/

## Support

For Bridge API support, contact: support@bridge.xyz
