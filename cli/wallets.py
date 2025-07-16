"""
Wallet CLI commands for Bridge API integration
"""

import click
import json
from typing import Dict, Any

from services.wallets import WalletService
from utils.logger import setup_logger

logger = setup_logger(__name__)

@click.group()
def wallets_cli():
    """Wallet management commands"""
    pass

@wallets_cli.command()
@click.option('--customer-id', required=True, help='Customer ID')
@click.option('--currency', required=True, type=click.Choice(['usd', 'usdc', 'usdt']), help='Wallet currency')
@click.pass_context
def create(ctx, customer_id, currency):
    """Create a new custodial wallet"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        wallet = wallet_service.create_wallet(customer_id, currency)
        
        click.echo(f"✅ Wallet created successfully!")
        click.echo(f"Wallet ID: {wallet.id}")
        click.echo(f"Customer ID: {wallet.customer_id}")
        click.echo(f"Currency: {wallet.currency}")
        click.echo(f"Balance: {wallet.balance}")
        if wallet.address:
            click.echo(f"Address: {wallet.address}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create wallet: {e}", err=True)

@wallets_cli.command()
@click.argument('wallet_id')
@click.pass_context
def get(ctx, wallet_id):
    """Get wallet by ID"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        wallet = wallet_service.get_wallet(wallet_id)
        
        click.echo(f"Wallet ID: {wallet.id}")
        click.echo(f"Customer ID: {wallet.customer_id}")
        click.echo(f"Currency: {wallet.currency}")
        click.echo(f"Balance: {wallet.balance}")
        if wallet.address:
            click.echo(f"Address: {wallet.address}")
        click.echo(f"Created: {wallet.created_at}")
        click.echo(f"Updated: {wallet.updated_at}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get wallet: {e}", err=True)

@wallets_cli.command()
@click.option('--customer-id', help='Filter by customer ID')
@click.option('--limit', default=10, help='Number of wallets to retrieve')
@click.option('--cursor', help='Pagination cursor')
@click.pass_context
def list(ctx, customer_id, limit, cursor):
    """List wallets"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        response = wallet_service.list_wallets(customer_id=customer_id, limit=limit, cursor=cursor)
        wallets = response.get('data', [])
        
        if not wallets:
            click.echo("No wallets found.")
            return
        
        click.echo(f"Found {len(wallets)} wallets:")
        click.echo()
        
        for wallet in wallets:
            click.echo(f"ID: {wallet.get('id')}")
            click.echo(f"Customer: {wallet.get('customer_id')}")
            click.echo(f"Currency: {wallet.get('currency')}")
            click.echo(f"Balance: {wallet.get('balance')}")
            click.echo("---")
        
        # Show pagination info
        if response.get('has_next_page'):
            click.echo(f"Next cursor: {response.get('next_cursor')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list wallets: {e}", err=True)

@wallets_cli.command()
@click.argument('wallet_id')
@click.pass_context
def balance(ctx, wallet_id):
    """Get wallet balance"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        response = wallet_service.get_wallet_balance(wallet_id)
        
        click.echo(f"Balance for wallet {wallet_id}:")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get wallet balance: {e}", err=True)

@wallets_cli.command()
@click.argument('wallet_id')
@click.option('--limit', default=10, help='Number of transactions to retrieve')
@click.option('--cursor', help='Pagination cursor')
@click.pass_context
def transactions(ctx, wallet_id, limit, cursor):
    """Get wallet transaction history"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        response = wallet_service.get_wallet_transactions(wallet_id, limit=limit, cursor=cursor)
        transactions = response.get('data', [])
        
        if not transactions:
            click.echo("No transactions found.")
            return
        
        click.echo(f"Found {len(transactions)} transactions for wallet {wallet_id}:")
        click.echo()
        
        for tx in transactions:
            click.echo(f"ID: {tx.get('id')}")
            click.echo(f"Amount: {tx.get('amount')}")
            click.echo(f"Type: {tx.get('type')}")
            click.echo(f"Status: {tx.get('status')}")
            click.echo(f"Created: {tx.get('created_at')}")
            click.echo("---")
        
        # Show pagination info
        if response.get('has_next_page'):
            click.echo(f"Next cursor: {response.get('next_cursor')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get wallet transactions: {e}", err=True)

@wallets_cli.command()
@click.argument('wallet_id')
@click.option('--currency', required=True, help='Currency for address')
@click.pass_context
def address(ctx, wallet_id, currency):
    """Get wallet address for specific currency"""
    client = ctx.obj['client']
    wallet_service = WalletService(client)
    
    try:
        response = wallet_service.get_wallet_address(wallet_id, currency)
        
        click.echo(f"Address for wallet {wallet_id} ({currency}):")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get wallet address: {e}", err=True)
