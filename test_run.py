"""
Quick test to verify everything works before running GUI
"""
import sys
import os

print("Testing blockchain imports...")

try:
    from blockchain.core.blockchain import Blockchain
    print("✓ Blockchain import successful")
except Exception as e:
    print(f"✗ Blockchain import failed: {e}")
    sys.exit(1)

try:
    from blockchain.wallet.wallet import Wallet
    print("✓ Wallet import successful")
except Exception as e:
    print(f"✗ Wallet import failed: {e}")
    sys.exit(1)

try:
    from blockchain.native.rust_simulator import RustSimulator
    print("✓ Rust simulator import successful")
except Exception as e:
    print(f"✗ Rust simulator import failed: {e}")

try:
    from blockchain.native.go_simulator import GoSimulator
    print("✓ Go simulator import successful")
except Exception as e:
    print(f"✗ Go simulator import failed: {e}")

try:
    from blockchain.native.assembly_simulator import AssemblySimulator
    print("✓ Assembly simulator import successful")
except Exception as e:
    print(f"✗ Assembly simulator import failed: {e}")

print("\n✓ All critical imports successful!")
print("\nYou can now run:")
print("  python run_gui.py")
print("  OR")
print("  python main.py")

