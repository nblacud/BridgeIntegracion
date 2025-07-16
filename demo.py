#!/usr/bin/env python3
"""
Bridge API Demo Script
Simple interactive examples of how to use the Bridge API CLI application
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run a CLI command and show the output"""
    print(f"\n🔹 Running: {cmd}")
    print("-" * 50)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("=== Bridge API CLI Demo ===")
    print("This shows examples of how to use the Bridge API application")
    print()
    
    # Check if API key is set
    if not os.getenv('BRIDGE_API_KEY'):
        print("❌ BRIDGE_API_KEY environment variable is not set")
        print("Please set your Bridge API key first")
        return
    
    print("✅ API key is configured")
    print()
    
    # Example commands
    examples = [
        ("Check API connection", "python main.py status"),
        ("List customers", "python main.py customers list --limit 5"),
        ("List transfers", "python main.py transfers list --limit 5"),
        ("Get customer help", "python main.py customers --help"),
        ("Get transfer help", "python main.py transfers --help"),
        ("Get wallet help", "python main.py wallets --help"),
    ]
    
    print("Available examples:")
    for i, (desc, cmd) in enumerate(examples, 1):
        print(f"{i}. {desc}")
    
    print("\nRunning examples:")
    
    # Run first few examples automatically
    for desc, cmd in examples[:3]:
        success = run_command(cmd)
        if not success:
            print(f"❌ Command failed: {cmd}")
    
    print("\n" + "="*60)
    print("To use the CLI manually, run commands like:")
    print("  python main.py status")
    print("  python main.py customers list")
    print("  python main.py transfers list")
    print("  python main.py wallets list [customer_id]")
    print("  python main.py --help")

if __name__ == "__main__":
    main()