#!/usr/bin/env python3
"""
Quick Commands for Bridge API
Easy-to-use functions that wrap the CLI commands
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

def check_connection():
    """Check if Bridge API connection is working"""
    print("🔍 Checking Bridge API connection...")
    stdout, stderr, success = run_cli_command("status")
    if success:
        print("✅ Connection successful!")
        print(stdout)
    else:
        print("❌ Connection failed!")
        print(stderr)
    return success

def list_customers():
    """List all customers"""
    print("👥 Listing customers...")
    stdout, stderr, success = run_cli_command("customers list --limit 10")
    if success:
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    return success

def list_transfers():
    """List all transfers"""
    print("💸 Listing transfers...")
    stdout, stderr, success = run_cli_command("transfers list --limit 10")
    if success:
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    return success

def get_customer_details(customer_id):
    """Get details for a specific customer"""
    print(f"👤 Getting customer details for {customer_id}...")
    stdout, stderr, success = run_cli_command(f"customers get {customer_id}")
    if success:
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    return success

def create_tos_link():
    """Create a Terms of Service link"""
    print("📋 Creating Terms of Service link...")
    stdout, stderr, success = run_cli_command("customers create-tos-link")
    if success:
        print("✅ TOS link created!")
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    return success

def main():
    """Run quick examples"""
    print("=== Bridge API Quick Commands ===")
    print()
    
    # Run some quick examples
    check_connection()
    print("\n" + "-"*50 + "\n")
    
    list_customers()
    print("\n" + "-"*50 + "\n")
    
    list_transfers()
    print("\n" + "-"*50 + "\n")
    
    create_tos_link()
    print("\n" + "-"*50 + "\n")
    
    print("🎉 All examples completed!")
    print("\nTo use these functions in your own code:")
    print("  from quick_commands import check_connection, list_customers")
    print("  check_connection()")
    print("  list_customers()")

if __name__ == "__main__":
    main()