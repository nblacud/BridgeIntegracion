#!/usr/bin/env python3
"""
Bridge API Integration Application

A comprehensive Python application for interacting with the Bridge API.
Supports customer management, transfers, and wallet operations with sandbox testing.
"""

import click
import logging
import os
from dotenv import load_dotenv
from typing import Optional

from config import Config
from bridge_client import BridgeClient
from utils.logger import setup_logger
from cli.customers import customers_cli
from cli.transfers import transfers_cli
from cli.wallets import wallets_cli
from cli.accounts import accounts_cli

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

@click.group()
@click.option('--api-key', envvar='BRIDGE_API_KEY', help='Bridge API Key')
@click.option('--environment', default='sandbox', type=click.Choice(['sandbox', 'production']), help='Environment to use')
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.pass_context
def cli(ctx, api_key: Optional[str], environment: str, debug: bool):
    """Bridge API Integration CLI Tool"""
    
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not api_key:
        click.echo("Error: API key is required. Set BRIDGE_API_KEY environment variable or use --api-key option.", err=True)
        ctx.exit(1)
    
    # Initialize configuration
    config = Config(
        api_key=api_key,
        environment=environment,
        debug=debug
    )
    
    # Initialize Bridge client
    bridge_client = BridgeClient(config)
    
    # Store in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['client'] = bridge_client
    
    logger.info(f"Initialized Bridge API client for {environment} environment")

@cli.command()
@click.pass_context
def status(ctx):
    """Check API connection status"""
    client = ctx.obj['client']
    
    try:
        # Test API connection by attempting to list customers
        response = client.get('/v0/customers', params={'limit': 1})
        click.echo(f"✅ API connection successful!")
        click.echo(f"Environment: {ctx.obj['config'].environment}")
        click.echo(f"Base URL: {ctx.obj['config'].base_url}")
    except Exception as e:
        click.echo(f"❌ API connection failed: {e}", err=True)
        ctx.exit(1)

# Add subcommand groups
cli.add_command(customers_cli, name='customers')
cli.add_command(transfers_cli, name='transfers')
cli.add_command(wallets_cli, name='wallets')
cli.add_command(accounts_cli, name='accounts')

if __name__ == '__main__':
    cli()
