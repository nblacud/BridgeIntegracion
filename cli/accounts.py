"""
External Account CLI commands for Bridge API integration
"""

import click
import json
from typing import Dict, Any

from services.external_accounts import ExternalAccountService
from models import ExternalAccountRequest, Address
from utils.logger import setup_logger

logger = setup_logger(__name__)

@click.group()
def accounts_cli():
    """External account management commands"""
    pass

@accounts_cli.command()
@click.option('--customer-id', required=True, help='Customer ID')
@click.option('--currency', required=True, type=click.Choice(['usd']), help='Account currency')
@click.option('--account-type', required=True, help='Account type (us, international)')
@click.option('--bank-name', required=True, help='Bank name')
@click.option('--account-name', required=True, help='Account name')
@click.option('--first-name', required=True, help='Account holder first name')
@click.option('--last-name', required=True, help='Account holder last name')
@click.option('--owner-type', required=True, type=click.Choice(['individual', 'business']), help='Account owner type')
@click.option('--owner-name', required=True, help='Account owner name')
@click.option('--routing-number', required=True, help='Bank routing number')
@click.option('--account-number', required=True, help='Bank account number')
@click.option('--account-subtype', required=True, type=click.Choice(['checking', 'savings']), help='Checking or savings')
@click.option('--address-line1', required=True, help='Address line 1')
@click.option('--address-line2', help='Address line 2')
@click.option('--city', required=True, help='City')
@click.option('--state', required=True, help='State')
@click.option('--postal-code', required=True, help='Postal code')
@click.option('--country', required=True, help='Country')
@click.pass_context
def create(ctx, **kwargs):
    """Create a new external account"""
    client = ctx.obj['client']
    account_service = ExternalAccountService(client)
    
    try:
        # Build address
        address = Address(
            street_line_1=kwargs['address_line1'],
            street_line_2=kwargs['address_line2'],
            city=kwargs['city'],
            subdivision=kwargs['state'],
            postal_code=kwargs['postal_code'],
            country=kwargs['country']
        )
        
        # Build account request
        account_request = ExternalAccountRequest(
            currency=kwargs['currency'],
            account_type=kwargs['account_type'],
            bank_name=kwargs['bank_name'],
            account_name=kwargs['account_name'],
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            account_owner_type=kwargs['owner_type'],
            account_owner_name=kwargs['owner_name'],
            account={
                'routing_number': kwargs['routing_number'],
                'account_number': kwargs['account_number'],
                'checking_or_savings': kwargs['account_subtype']
            },
            address=address
        )
        
        account = account_service.create_external_account(kwargs['customer_id'], account_request)
        
        click.echo(f"✅ External account created successfully!")
        click.echo(f"Account ID: {account.id}")
        click.echo(f"Customer ID: {account.customer_id}")
        click.echo(f"Bank: {account.bank_name}")
        click.echo(f"Account Name: {account.account_name}")
        click.echo(f"Last 4: {account.last_4}")
        click.echo(f"Active: {account.active}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create external account: {e}", err=True)

@accounts_cli.command()
@click.argument('customer_id')
@click.argument('account_id')
@click.pass_context
def get(ctx, customer_id, account_id):
    """Get external account by ID"""
    client = ctx.obj['client']
    account_service = ExternalAccountService(client)
    
    try:
        account = account_service.get_external_account(customer_id, account_id)
        
        click.echo(f"Account ID: {account.id}")
        click.echo(f"Customer ID: {account.customer_id}")
        click.echo(f"Bank: {account.bank_name}")
        click.echo(f"Account Name: {account.account_name}")
        click.echo(f"Owner: {account.account_owner_name}")
        click.echo(f"Type: {account.account_owner_type}")
        click.echo(f"Currency: {account.currency}")
        click.echo(f"Last 4: {account.last_4}")
        click.echo(f"Active: {account.active}")
        click.echo(f"Created: {account.created_at}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get external account: {e}", err=True)

@accounts_cli.command()
@click.argument('customer_id')
@click.option('--limit', default=10, help='Number of accounts to retrieve')
@click.option('--cursor', help='Pagination cursor')
@click.pass_context
def list(ctx, customer_id, limit, cursor):
    """List external accounts for customer"""
    client = ctx.obj['client']
    account_service = ExternalAccountService(client)
    
    try:
        response = account_service.list_external_accounts(customer_id, limit=limit, cursor=cursor)
        accounts = response.get('data', [])
        
        if not accounts:
            click.echo("No external accounts found.")
            return
        
        click.echo(f"Found {len(accounts)} external accounts for customer {customer_id}:")
        click.echo()
        
        for account in accounts:
            click.echo(f"ID: {account.get('id')}")
            click.echo(f"Bank: {account.get('bank_name')}")
            click.echo(f"Account Name: {account.get('account_name')}")
            click.echo(f"Last 4: {account.get('last_4')}")
            click.echo(f"Active: {account.get('active')}")
            click.echo("---")
        
        # Show pagination info
        if response.get('has_next_page'):
            click.echo(f"Next cursor: {response.get('next_cursor')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list external accounts: {e}", err=True)

@accounts_cli.command()
@click.argument('customer_id')
@click.argument('account_id')
@click.pass_context
def delete(ctx, customer_id, account_id):
    """Delete external account"""
    client = ctx.obj['client']
    account_service = ExternalAccountService(client)
    
    try:
        response = account_service.delete_external_account(customer_id, account_id)
        
        click.echo(f"✅ External account {account_id} deleted successfully!")
        
    except Exception as e:
        click.echo(f"❌ Failed to delete external account: {e}", err=True)

@accounts_cli.command()
@click.argument('customer_id')
@click.pass_context
def plaid_token(ctx, customer_id):
    """Get Plaid link token for customer"""
    client = ctx.obj['client']
    account_service = ExternalAccountService(client)
    
    try:
        response = account_service.get_plaid_link_token(customer_id)
        
        click.echo(f"Plaid link token for customer {customer_id}:")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get Plaid link token: {e}", err=True)
