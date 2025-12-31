"""
Fix import issues and verify all modules
"""
import sys
import os

def check_imports():
    """Check all imports"""
    errors = []
    
    try:
        from blockchain.core.blockchain import Blockchain
        print("✓ blockchain.core.blockchain")
    except Exception as e:
        errors.append(f"blockchain.core.blockchain: {e}")
    
    try:
        from blockchain.wallet.wallet import Wallet
        print("✓ blockchain.wallet.wallet")
    except Exception as e:
        errors.append(f"blockchain.wallet.wallet: {e}")
    
    try:
        from blockchain.crypto.signature import generate_keypair
        print("✓ blockchain.crypto.signature")
    except Exception as e:
        errors.append(f"blockchain.crypto.signature: {e}")
    
    try:
        from blockchain.native.rust_simulator import RustSimulator
        print("✓ blockchain.native.rust_simulator")
    except Exception as e:
        errors.append(f"blockchain.native.rust_simulator: {e}")
    
    try:
        from blockchain.native.go_simulator import GoSimulator
        print("✓ blockchain.native.go_simulator")
    except Exception as e:
        errors.append(f"blockchain.native.go_simulator: {e}")
    
    try:
        from blockchain.native.assembly_simulator import AssemblySimulator
        print("✓ blockchain.native.assembly_simulator")
    except Exception as e:
        errors.append(f"blockchain.native.assembly_simulator: {e}")
    
    try:
        from blockchain.background.service_manager import ServiceManager
        print("✓ blockchain.background.service_manager")
    except Exception as e:
        errors.append(f"blockchain.background.service_manager: {e}")
    
    if errors:
        print("\n✗ Errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✓ All imports successful!")
        return True

if __name__ == '__main__':
    check_imports()

