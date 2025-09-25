"""
Configuration Manager for AI Agent Platform
Handles configuration for both premium and basic deployment models
"""

import json
import os
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import base64

class ConfigManager:
    """Manages configuration for different deployment models"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "deployment_model": "basic",  # "premium" or "basic"
            "app_settings": {
                "theme": "light",
                "language": "en",
                "auto_save": True,
                "notifications": True
            },
            "api_settings": {
                "timeout": 30,
                "max_retries": 3,
                "rate_limit": 100
            },
            "security_settings": {
                "encryption_enabled": True,
                "session_timeout": 3600,
                "max_login_attempts": 5
            },
            "feature_flags": {
                "advanced_analytics": False,
                "export_functionality": True,
                "batch_processing": False,
                "custom_integrations": False
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def is_premium(self) -> bool:
        """Check if running in premium mode"""
        return self.get('deployment_model') == 'premium'
    
    def get_api_key(self) -> Optional[str]:
        """Get API key based on deployment model"""
        if self.is_premium():
            # Premium version - return embedded key
            return self._get_embedded_api_key()
        else:
            # Basic version - return user-configured key
            return self.get('api_key')
    
    def _get_embedded_api_key(self) -> str:
        """Get embedded API key for premium version"""
        # This would contain the actual embedded API key in premium version
        # For security, this is encoded/encrypted
        encoded_key = "Z3NrX1lPVVJfQUNUVUFMX0FQSV9LRVlfSEVSRQ=="  # Placeholder
        try:
            return base64.b64decode(encoded_key).decode('utf-8')
        except:
            return ""
    
    def set_api_key(self, api_key: str):
        """Set API key for basic version"""
        if not self.is_premium():
            self.set('api_key', api_key)
    
    def get_feature_access(self, feature: str) -> bool:
        """Check if feature is available in current deployment model"""
        if self.is_premium():
            # Premium version has access to all features
            return True
        else:
            # Basic version has limited features
            return self.get(f'feature_flags.{feature}', False)
    
    def get_rate_limit(self) -> int:
        """Get rate limit based on deployment model"""
        if self.is_premium():
            return 1000  # Higher limit for premium
        else:
            return self.get('api_settings.rate_limit', 100)
    
    def create_basic_config_template(self) -> Dict[str, Any]:
        """Create configuration template for basic version"""
        return {
            "deployment_model": "basic",
            "api_key": "",  # User needs to fill this
            "app_settings": {
                "theme": "light",
                "language": "en",
                "auto_save": True,
                "notifications": True
            },
            "api_settings": {
                "timeout": 30,
                "max_retries": 3,
                "rate_limit": 100
            },
            "feature_flags": {
                "advanced_analytics": False,
                "export_functionality": True,
                "batch_processing": False,
                "custom_integrations": False
            }
        }
    
    def create_premium_config_template(self) -> Dict[str, Any]:
        """Create configuration template for premium version"""
        return {
            "deployment_model": "premium",
            "app_settings": {
                "theme": "dark",
                "language": "en",
                "auto_save": True,
                "notifications": True
            },
            "api_settings": {
                "timeout": 60,
                "max_retries": 5,
                "rate_limit": 1000
            },
            "feature_flags": {
                "advanced_analytics": True,
                "export_functionality": True,
                "batch_processing": True,
                "custom_integrations": True
            }
        }

class APIKeyManager:
    """Manages API key encryption and storage"""
    
    def __init__(self, key_file: str = ".api_key"):
        self.key_file = key_file
        self.cipher_key = self._get_or_create_cipher_key()
    
    def _get_or_create_cipher_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = ".cipher_key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key"""
        f = Fernet(self.cipher_key)
        encrypted = f.encrypt(api_key.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key"""
        try:
            f = Fernet(self.cipher_key)
            encrypted = base64.b64decode(encrypted_key.encode())
            return f.decrypt(encrypted).decode()
        except:
            return ""
    
    def save_encrypted_key(self, api_key: str):
        """Save encrypted API key to file"""
        encrypted = self.encrypt_api_key(api_key)
        with open(self.key_file, 'w') as f:
            f.write(encrypted)
    
    def load_encrypted_key(self) -> str:
        """Load and decrypt API key from file"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'r') as f:
                encrypted = f.read().strip()
                return self.decrypt_api_key(encrypted)
        return ""

class EnvironmentManager:
    """Manages environment-specific settings"""
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development environment"""
        return os.getenv('ENVIRONMENT', 'production').lower() == 'development'
    
    @staticmethod
    def is_production() -> bool:
        """Check if running in production environment"""
        return os.getenv('ENVIRONMENT', 'production').lower() == 'production'
    
    @staticmethod
    def get_log_level() -> str:
        """Get appropriate log level"""
        if EnvironmentManager.is_development():
            return 'DEBUG'
        else:
            return 'INFO'
    
    @staticmethod
    def get_database_url() -> str:
        """Get database URL based on environment"""
        if EnvironmentManager.is_development():
            return os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')
        else:
            return os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    
    @staticmethod
    def get_cache_settings() -> Dict[str, Any]:
        """Get cache settings based on environment"""
        if EnvironmentManager.is_development():
            return {
                'enabled': False,
                'ttl': 60
            }
        else:
            return {
                'enabled': True,
                'ttl': 3600
            }

