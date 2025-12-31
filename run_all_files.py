"""
Run all blockchain files and examples
Comprehensive test runner for all components
"""
import sys
import os
import subprocess
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_python_file(file_path: str, description: str = "") -> bool:
    """Run a Python file and return success status"""
    print(f"\n{'='*70}")
    print(f"Running: {file_path}")
    if description:
        print(f"Description: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print(f"[OK] {file_path} completed successfully")
            if result.stdout:
                print("Output:")
                print(result.stdout[:500])  # First 500 chars
            return True
        else:
            print(f"[ERROR] {file_path} failed with code {result.returncode}")
            if result.stderr:
                print("Error:")
                print(result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {file_path} exceeded 60 second timeout")
        return False
    except Exception as e:
        print(f"[EXCEPTION] {file_path} raised exception: {e}")
        return False


def run_all_files():
    """Run all blockchain files"""
    print("="*70)
    print("BLOCKCHAIN COMPREHENSIVE TEST RUNNER")
    print("Running all files and examples")
    print("="*70)
    
    base_dir = Path(__file__).parent
    results = {}
    
    # Main application files
    main_files = [
        ("main.py", "Main blockchain application"),
        ("run.py", "Master launcher with all functions"),
        ("run_simple_gui.py", "Simple GUI launcher"),
        ("run_gui.py", "Full GUI launcher (with charts)"),
    ]
    
    # Example files
    example_files = [
        ("examples/basic_usage.py", "Basic usage examples"),
    ]
    
    # Test/utility files
    utility_files = [
        ("fix_imports.py", "Import verification"),
        ("test_run.py", "Quick test runner"),
    ]
    
    all_files = main_files + example_files + utility_files
    
    print(f"\nFound {len(all_files)} files to run\n")
    
    # Run each file
    for file_path, description in all_files:
        full_path = base_dir / file_path
        if full_path.exists():
            # Skip GUI files that require user interaction
            if "gui" in file_path.lower():
                print(f"[SKIP] {file_path} - Requires GUI interaction")
                results[file_path] = "skipped"
            else:
                success = run_python_file(str(full_path), description)
                results[file_path] = "passed" if success else "failed"
                time.sleep(1)  # Small delay between runs
        else:
            print(f"[NOT FOUND] {file_path}")
            results[file_path] = "not_found"
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v == "passed")
    failed = sum(1 for v in results.values() if v == "failed")
    skipped = sum(1 for v in results.values() if v == "skipped")
    not_found = sum(1 for v in results.values() if v == "not_found")
    
    print(f"Total files: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Not found: {not_found}")
    print("="*70)
    
    # Detailed results
    print("\nDetailed Results:")
    for file_path, status in results.items():
        status_symbol = {
            "passed": "[OK]",
            "failed": "[FAIL]",
            "skipped": "[SKIP]",
            "not_found": "[MISSING]"
        }.get(status, "[?]")
        print(f"{status_symbol} {file_path}")
    
    return failed == 0


def run_all_modules():
    """Test all blockchain modules by importing them"""
    print("\n" + "="*70)
    print("TESTING ALL MODULES (Import Test)")
    print("="*70)
    
    modules = [
        "blockchain.core.blockchain",
        "blockchain.core.block",
        "blockchain.core.genesis",
        "blockchain.crypto.signature",
        "blockchain.crypto.hashing",
        "blockchain.crypto.encoding",
        "blockchain.wallet.wallet",
        "blockchain.wallet.transaction_builder",
        "blockchain.network.node",
        "blockchain.network.protocol",
        "blockchain.network.message",
        "blockchain.storage.database",
        "blockchain.storage.cache",
        "blockchain.security.auditor",
        "blockchain.security.validator",
        "blockchain.performance.profiler",
        "blockchain.performance.metrics",
        "blockchain.utils.config",
        "blockchain.utils.logger",
        "blockchain.utils.miner",
        "blockchain.utils.validator",
        "blockchain.advanced.merkle_proof",
        "blockchain.advanced.script_engine",
        "blockchain.advanced.consensus",
        "blockchain.obfuscation.encryption",
        "blockchain.obfuscation.compression",
        "blockchain.obfuscation.encoding",
    ]
    
    # Try heavy compute modules
    heavy_modules = [
        "blockchain.compute.gpu_accelerator",
        "blockchain.compute.cpu_intensive",
        "blockchain.compute.parallel_miner",
        "blockchain.compute.power_consumer",
    ]
    
    # Try native modules
    native_modules = [
        "blockchain.native.rust_simulator",
        "blockchain.native.go_simulator",
        "blockchain.native.assembly_simulator",
    ]
    
    all_modules = modules + heavy_modules + native_modules
    
    passed = 0
    failed = 0
    
    for module_name in all_modules:
        try:
            __import__(module_name)
            print(f"[OK] {module_name}")
            passed += 1
        except ImportError as e:
            print(f"[FAIL] {module_name} - {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {module_name} - {e}")
            failed += 1
    
    print(f"\nModule Test Results: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run all blockchain files')
    parser.add_argument(
        '--modules-only',
        action='store_true',
        help='Only test module imports'
    )
    parser.add_argument(
        '--files-only',
        action='store_true',
        help='Only run files, skip module tests'
    )
    
    args = parser.parse_args()
    
    success = True
    
    if not args.modules_only:
        print("Running all files...")
        success = run_all_files() and success
    
    if not args.files_only:
        print("\nTesting all modules...")
        success = run_all_modules() and success
    
    if success:
        print("\n[OK] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAIL] Some tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()

