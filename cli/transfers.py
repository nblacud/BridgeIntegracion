"""
Transfer CLI commands for Bridge API integration
"""

import click
import json
from typing import Dict, Any

from services.transfers import TransferService
from models import TransferRequest, TransferSource, TransferDestination
from utils.logger import setup_logger

logger = setup_logger(__name__)

@click.group()
def transfers_cli():
    """Transfer management commands"""
    pass

@transfers_cli.command()
@click.option('--amount', required=True, help='Transfer amount')
@click.option('--customer-id', required=True, help='Customer ID (on_behalf_of)')
@click.option('--source-rail', required=True, type=click.Choice(['ach', 'wire', 'polygon', 'ethereum', 'arbitrum', 'base']), help='Source payment rail')
@click.option('--source-currency', required=True, type=click.Choice(['usd', 'usdc', 'usdt']), help='Source currency')
@click.option('--source-address', help='Source address (for crypto)')
@click.option('--source-account-id', help='Source external account ID (for fiat)')
@click.option('--dest-rail', required=True, type=click.Choice(['ach', 'wire', 'polygon', 'ethereum', 'arbitrum', 'base']), help='Destination payment rail')
@click.option('--dest-currency', required=True, type=click.Choice(['usd', 'usdc', 'usdt']), help='Destination currency')
@click.option('--dest-address', help='Destination address (for crypto)')
@click.option('--dest-account-id', help='Destination external account ID (for fiat)')
@click.pass_context
def create(ctx, **kwargs):
    """Create a new transfer"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        # Build source
        source = TransferSource(
            payment_rail=kwargs['source_rail'],
            currency=kwargs['source_currency'],
            from_address=kwargs['source_address'],
            external_account_id=kwargs['source_account_id']
        )
        
        # Build destination
        destination = TransferDestination(
            payment_rail=kwargs['dest_rail'],
            currency=kwargs['dest_currency'],
            to_address=kwargs['dest_address'],
            external_account_id=kwargs['dest_account_id']
        )
        
        # Build transfer request
        transfer_request = TransferRequest(
            amount=kwargs['amount'],
            on_behalf_of=kwargs['customer_id'],
            source=source,
            destination=destination
        )
        
        transfer = transfer_service.create_transfer(transfer_request)
        
        click.echo(f"✅ Transfer created successfully!")
        click.echo(f"Transfer ID: {transfer.id}")
        click.echo(f"Amount: {transfer.amount}")
        click.echo(f"Status: {transfer.status}")
        click.echo(f"Customer: {transfer.on_behalf_of}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create transfer: {e}", err=True)

@transfers_cli.command()
@click.argument('transfer_id')
@click.pass_context
def get(ctx, transfer_id):
    """Get transfer by ID"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        transfer = transfer_service.get_transfer(transfer_id)
        
        click.echo(f"Transfer ID: {transfer.id}")
        click.echo(f"Amount: {transfer.amount}")
        click.echo(f"Status: {transfer.status}")
        click.echo(f"Customer: {transfer.on_behalf_of}")
        click.echo(f"Source: {transfer.source.payment_rail} ({transfer.source.currency})")
        click.echo(f"Destination: {transfer.destination.payment_rail} ({transfer.destination.currency})")
        click.echo(f"Created: {transfer.created_at}")
        click.echo(f"Updated: {transfer.updated_at}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get transfer: {e}", err=True)

@transfers_cli.command()
@click.option('--limit', default=10, help='Number of transfers to retrieve')
@click.option('--cursor', help='Pagination cursor')
@click.option('--customer-id', help='Filter by customer ID')
@click.pass_context
def list(ctx, limit, cursor, customer_id):
    """List transfers"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        response = transfer_service.list_transfers(limit=limit, cursor=cursor, customer_id=customer_id)
        transfers = response.get('data', [])
        
        if not transfers:
            click.echo("No transfers found.")
            return
        
        click.echo(f"Found {len(transfers)} transfers:")
        click.echo()
        
        for transfer in transfers:
            click.echo(f"ID: {transfer.get('id')}")
            click.echo(f"Amount: {transfer.get('amount')}")
            click.echo(f"Status: {transfer.get('status')}")
            click.echo(f"Customer: {transfer.get('on_behalf_of')}")
            click.echo("---")
        
        # Show pagination info
        if response.get('has_next_page'):
            click.echo(f"Next cursor: {response.get('next_cursor')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list transfers: {e}", err=True)

@transfers_cli.command()
@click.argument('transfer_id')
@click.pass_context
def cancel(ctx, transfer_id):
    """Cancel a pending transfer"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        response = transfer_service.cancel_transfer(transfer_id)
        
        click.echo(f"✅ Transfer {transfer_id} cancelled successfully!")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to cancel transfer: {e}", err=True)

@transfers_cli.command()
@click.argument('transfer_id')
@click.pass_context
def receipt(ctx, transfer_id):
    """Get transfer receipt"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        response = transfer_service.get_transfer_receipt(transfer_id)
        
        click.echo(f"Receipt for transfer {transfer_id}:")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get transfer receipt: {e}", err=True)

@transfers_cli.command()
@click.option('--source-currency', required=True, help='Source currency')
@click.option('--dest-currency', required=True, help='Destination currency')
@click.option('--amount', required=True, help='Amount to quote')
@click.pass_context
def quote(ctx, source_currency, dest_currency, amount):
    """Get exchange rate quote"""
    client = ctx.obj['client']
    transfer_service = TransferService(client)
    
    try:
        response = transfer_service.get_quote(source_currency, dest_currency, amount)
        
        click.echo(f"Quote for {amount} {source_currency} → {dest_currency}:")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get quote: {e}", err=True)
