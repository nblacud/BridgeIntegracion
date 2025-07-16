"""
Customer CLI commands for Bridge API integration
"""

import click
import json
from typing import Dict, Any

from services.customers import CustomerService
from models import CustomerRequest, Address, IdentifyingInformation
from utils.logger import setup_logger

logger = setup_logger(__name__)

@click.group()
def customers_cli():
    """Customer management commands"""
    pass

@customers_cli.command()
@click.option('--redirect-uri', help='Redirect URI after TOS acceptance')
@click.pass_context
def create_tos_link(ctx, redirect_uri):
    """Create Terms of Service link for customer"""
    client = ctx.obj['client']
    customer_service = CustomerService(client)
    
    try:
        response = customer_service.create_tos_link(redirect_uri)
        click.echo(f"✅ TOS Link created successfully!")
        click.echo(f"URL: {response.url}")
        click.echo("\nShare this URL with your customer to accept terms of service.")
        
    except Exception as e:
        click.echo(f"❌ Failed to create TOS link: {e}", err=True)

@customers_cli.command()
@click.option('--type', type=click.Choice(['individual', 'business']), required=True, help='Customer type')
@click.option('--first-name', required=True, help='First name')
@click.option('--last-name', required=True, help='Last name')
@click.option('--email', required=True, help='Email address')
@click.option('--phone', help='Phone number')
@click.option('--birth-date', required=True, help='Birth date (YYYY-MM-DD)')
@click.option('--signed-agreement-id', required=True, help='Signed agreement ID from TOS')
@click.option('--address-line1', required=True, help='Address line 1')
@click.option('--address-line2', help='Address line 2')
@click.option('--city', required=True, help='City')
@click.option('--state', help='State/subdivision')
@click.option('--postal-code', required=True, help='Postal code')
@click.option('--country', required=True, help='Country (ISO 3166-1 alpha3)')
@click.option('--id-type', required=True, help='ID type (ssn, passport, drivers_license)')
@click.option('--id-country', required=True, help='ID issuing country')
@click.option('--id-number', required=True, help='ID number')
@click.option('--id-front-image', help='Base64 encoded front image')
@click.option('--id-back-image', help='Base64 encoded back image')
@click.pass_context
def create(ctx, **kwargs):
    """Create a new customer"""
    client = ctx.obj['client']
    customer_service = CustomerService(client)
    
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
        
        # Build identifying information
        id_info = IdentifyingInformation(
            type=kwargs['id_type'],
            issuing_country=kwargs['id_country'],
            number=kwargs['id_number'],
            image_front=kwargs['id_front_image'],
            image_back=kwargs['id_back_image']
        )
        
        # Build customer request
        customer_request = CustomerRequest(
            type=kwargs['type'],
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            email=kwargs['email'],
            phone=kwargs['phone'],
            residential_address=address,
            birth_date=kwargs['birth_date'],
            signed_agreement_id=kwargs['signed_agreement_id'],
            identifying_information=[id_info]
        )
        
        customer = customer_service.create_customer(customer_request)
        
        click.echo(f"✅ Customer created successfully!")
        click.echo(f"Customer ID: {customer.id}")
        click.echo(f"Status: {customer.status}")
        click.echo(f"Email: {customer.email}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create customer: {e}", err=True)

@customers_cli.command()
@click.argument('customer_id')
@click.pass_context
def get(ctx, customer_id):
    """Get customer by ID"""
    client = ctx.obj['client']
    customer_service = CustomerService(client)
    
    try:
        customer = customer_service.get_customer(customer_id)
        
        click.echo(f"Customer ID: {customer.id}")
        click.echo(f"Name: {customer.first_name} {customer.last_name}")
        click.echo(f"Email: {customer.email}")
        click.echo(f"Status: {customer.status}")
        click.echo(f"Type: {customer.type}")
        click.echo(f"Created: {customer.created_at}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get customer: {e}", err=True)

@customers_cli.command()
@click.option('--limit', default=10, help='Number of customers to retrieve')
@click.option('--cursor', help='Pagination cursor')
@click.pass_context
def list(ctx, limit, cursor):
    """List customers"""
    client = ctx.obj['client']
    customer_service = CustomerService(client)
    
    try:
        response = customer_service.list_customers(limit=limit, cursor=cursor)
        customers = response.get('data', [])
        
        if not customers:
            click.echo("No customers found.")
            return
        
        click.echo(f"Found {len(customers)} customers:")
        click.echo()
        
        for customer in customers:
            click.echo(f"ID: {customer.get('id')}")
            click.echo(f"Name: {customer.get('first_name')} {customer.get('last_name')}")
            click.echo(f"Email: {customer.get('email')}")
            click.echo(f"Status: {customer.get('status')}")
            click.echo("---")
        
        # Show pagination info
        if response.get('has_next_page'):
            click.echo(f"Next cursor: {response.get('next_cursor')}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list customers: {e}", err=True)

@customers_cli.command()
@click.argument('customer_id')
@click.pass_context
def kyc_status(ctx, customer_id):
    """Get KYC status for customer"""
    client = ctx.obj['client']
    customer_service = CustomerService(client)
    
    try:
        response = customer_service.get_customer_kyc_status(customer_id)
        
        click.echo(f"KYC Status for customer {customer_id}:")
        click.echo(json.dumps(response, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Failed to get KYC status: {e}", err=True)
