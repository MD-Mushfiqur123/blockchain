"""
Launch heavy blockchain with maximum GPU/CPU usage
WARNING: High power consumption!
"""
from main_heavy import main

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 HEAVY BLOCKCHAIN MODE")
    print("=" * 60)
    print("⚠️  WARNING: This will consume maximum CPU/GPU power!")
    print("🌡️  Ensure adequate cooling and power supply!")
    print("=" * 60)
    
    response = input("Continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        main()
    else:
        print("Cancelled.")

