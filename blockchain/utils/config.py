"""
Configuration management
"""
import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Advanced configuration manager"""
    
    DEFAULT_CONFIG = {
        'blockchain': {
            'difficulty': 4,
            'block_time_target': 1.0,  # 1 second per block
            'max_block_size': 1000000,  # 1MB
            'difficulty_adjustment_interval': 2016,
            'halving_interval': 210000,
            'initial_block_reward': 50.0
        },
        'network': {
            'host': 'localhost',
            'port': 8333,
            'max_peers': 50,
            'connection_timeout': 30
        },
        'mining': {
            'enabled': True,
            'threads': 4,
            'max_nonce': 10000000
        },
        'wallet': {
            'data_dir': 'wallet_data',
            'encrypt_wallets': True
        }
    }
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = Path(config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._merge_config(self.config, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _merge_config(self, base: Dict, override: Dict):
        """Recursively merge configuration"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default=None):
        """Get configuration value by dot-separated path"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, key_path: str, value: Any):
        """Set configuration value by dot-separated path"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

