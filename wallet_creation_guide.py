#!/usr/bin/env python3
"""
Wallet Creation Guide for Bridge API
Demonstrates how to create wallets for different currencies and networks
"""

import subprocess
import json
import sys

def run_cli_command(command):
    """Run a CLI command and return the result"""
    try:
        result = subprocess.run(f"python main.py {command}", 
                              shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode == 0
    except Exception as e:
        return "", str(e), False

def get_active_customers():
    """Get list of active customers"""
    stdout, stderr, success = run_cli_command("customers list")
    if success:
        print("📋 Available customers:")
        print(stdout)
        return True
    else:
        print(f"❌ Error getting customers: {stderr}")
        return False

def create_wallet_for_customer(customer_id, currency, network=None):
    """Create a wallet for a customer"""
    print(f"\n💼 Creating {currency.upper()} wallet for customer {customer_id}...")
    
    if network:
        print(f"🌐 Target network: {network}")
    
    # Try creating the wallet
    stdout, stderr, success = run_cli_command(f"wallets create --customer-id {customer_id} --currency {currency}")
    
    if success:
        print(f"✅ {currency.upper()} wallet created successfully!")
        print(stdout)
        return True
    else:
        print(f"❌ Failed to create {currency.upper()} wallet: {stderr}")
        return False

def list_customer_wallets(customer_id):
    """List all wallets for a customer"""
    print(f"\n📱 Listing wallets for customer {customer_id}...")
    stdout, stderr, success = run_cli_command(f"wallets list --customer-id {customer_id}")
    
    if success:
        print(stdout)
        return True
    else:
        print(f"❌ Error listing wallets: {stderr}")
        return False

def get_wallet_address(wallet_id, currency):
    """Get wallet address for specific currency"""
    print(f"\n🔗 Getting {currency.upper()} address for wallet {wallet_id}...")
    stdout, stderr, success = run_cli_command(f"wallets address --wallet-id {wallet_id} --currency {currency}")
    
    if success:
        print(f"✅ {currency.upper()} address retrieved:")
        print(stdout)
        return True
    else:
        print(f"❌ Error getting address: {stderr}")
        return False

def main():
    print("=== Bridge API Wallet Creation Guide ===")
    print()
    
    # Get available customers
    print("Step 1: Getting available customers...")
    if not get_active_customers():
        return
    
    # Example customer IDs from your data
    example_customers = [
        "6913c1d4-18e5-4334-8f67-875b7f450f2f",  # NICOLAS BLACUD (active)
        "88dced26-cd90-402b-aa37-eb8105dcd720",  # Payglo LLC (active)
    ]
    
    print("\n" + "="*60)
    print("Step 2: Creating wallets for different currencies...")
    
    for customer_id in example_customers:
        print(f"\n🎯 Working with customer: {customer_id}")
        
        # Try creating different types of wallets
        currencies = ["usd", "usdc", "usdt"]
        
        for currency in currencies:
            success = create_wallet_for_customer(customer_id, currency, "solana" if currency in ["usdc", "usdt"] else "fiat")
            if success:
                # List wallets after creation
                list_customer_wallets(customer_id)
                break  # Stop after first successful wallet creation
        
        print("\n" + "-"*40)
    
    print("\n" + "="*60)
    print("💡 Wallet Creation Tips:")
    print("1. USDT wallets on Solana network are supported")
    print("2. USD wallets are fiat-based for ACH/Wire transfers")
    print("3. USDC wallets support multiple blockchain networks")
    print("4. Customers must be in 'active' status for wallet creation")
    print("5. Use 'wallets address' command to get network-specific addresses")
    
    print("\n📚 Available Commands:")
    print("• python main.py wallets create --customer-id [ID] --currency usdt")
    print("• python main.py wallets list --customer-id [ID]")
    print("• python main.py wallets address --wallet-id [ID] --currency usdt")
    print("• python main.py wallets balance --wallet-id [ID]")

if __name__ == "__main__":
    main()