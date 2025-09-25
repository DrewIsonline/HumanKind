"""
Base Agent Class for AI Agent Platform
Provides common functionality for all specialized agents
"""

import json
import os
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract base class for all AI agents"""
    
    def __init__(self, config_path: str = None, api_key: str = None):
        """
        Initialize the base agent
        
        Args:
            config_path: Path to configuration file
            api_key: API key for premium version (embedded) or None for basic version
        """
        self.config_path = config_path
        self.api_key = api_key
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "app_name": "AI Agent",
            "version": "1.0.0",
            "debug": False,
            "max_retries": 3,
            "timeout": 30,
            "ui_theme": "light",
            "language": "en"
        }
        
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                self.log_error(f"Error loading config: {e}")
                
        return default_config
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = logging.DEBUG if self.config.get('debug', False) else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def log_error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from embedded source or config file"""
        if self.api_key:  # Premium version with embedded key
            return self.api_key
        
        # Basic version - try to load from config
        if self.config_path:
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key')
            except Exception as e:
                self.log_error(f"Error loading API key from config: {e}")
        
        return None
    
    def make_api_request(self, endpoint: str, data: Dict[str, Any], method: str = 'POST') -> Optional[Dict[str, Any]]:
        """Make API request with error handling and retries"""
        api_key = self.get_api_key()
        if not api_key:
            self.log_error("No API key available")
            return None
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        for attempt in range(self.config.get('max_retries', 3)):
            try:
                if method.upper() == 'POST':
                    response = requests.post(
                        endpoint, 
                        json=data, 
                        headers=headers,
                        timeout=self.config.get('timeout', 30)
                    )
                elif method.upper() == 'GET':
                    response = requests.get(
                        endpoint, 
                        params=data, 
                        headers=headers,
                        timeout=self.config.get('timeout', 30)
                    )
                else:
                    self.log_error(f"Unsupported HTTP method: {method}")
                    return None
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                self.log_error(f"API request failed (attempt {attempt + 1}): {e}")
                if attempt == self.config.get('max_retries', 3) - 1:
                    return None
        
        return None
    
    def save_data(self, data: Dict[str, Any], filename: str):
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            self.log_info(f"Data saved to {filename}")
        except Exception as e:
            self.log_error(f"Error saving data to {filename}: {e}")
    
    def load_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.log_error(f"Error loading data from {filename}: {e}")
        return None
    
    def setup_streamlit_page(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title=self.config.get('app_name', 'AI Agent'),
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .info-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #dc3545;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display_header(self, title: str, subtitle: str = None):
        """Display formatted header"""
        st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
        if subtitle:
            st.markdown(f'<div style="text-align: center; color: #666; margin-bottom: 2rem;">{subtitle}</div>', unsafe_allow_html=True)
    
    def display_info_box(self, message: str, box_type: str = "info"):
        """Display styled info box"""
        st.markdown(f'<div class="{box_type}-box">{message}</div>', unsafe_allow_html=True)
    
    def create_sidebar_navigation(self, pages: List[str]) -> str:
        """Create sidebar navigation"""
        st.sidebar.title("Navigation")
        return st.sidebar.selectbox("Select Page", pages)
    
    def validate_input(self, value: Any, validation_type: str, **kwargs) -> bool:
        """Validate user input"""
        if validation_type == "required" and not value:
            return False
        elif validation_type == "email" and value:
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, value))
        elif validation_type == "phone" and value:
            import re
            pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$'
            return bool(re.match(pattern, value))
        elif validation_type == "number" and value:
            try:
                float(value)
                return True
            except ValueError:
                return False
        elif validation_type == "range" and value:
            min_val = kwargs.get('min', float('-inf'))
            max_val = kwargs.get('max', float('inf'))
            try:
                num_val = float(value)
                return min_val <= num_val <= max_val
            except ValueError:
                return False
        
        return True
    
    @abstractmethod
    def get_agent_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    @abstractmethod
    def process_user_input(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and return results"""
        pass
    
    @abstractmethod
    def render_main_interface(self):
        """Render the main user interface"""
        pass
    
    def run(self):
        """Main entry point for the agent"""
        self.setup_streamlit_page()
        self.render_main_interface()

class AgentFactory:
    """Factory class for creating agent instances"""
    
    @staticmethod
    def create_agent(agent_type: str, config_path: str = None, api_key: str = None):
        """Create agent instance based on type"""
        if agent_type == "farm_management":
            from farm_management_agent import FarmManagementAgent
            return FarmManagementAgent(config_path, api_key)
        elif agent_type == "elderly_care":
            from elderly_care_agent import ElderlyCareAgent
            return ElderlyCareAgent(config_path, api_key)
        elif agent_type == "workforce_skills":
            from workforce_skills_agent import WorkforceSkillsAgent
            return WorkforceSkillsAgent(config_path, api_key)
        elif agent_type == "government_navigator":
            from government_navigator_agent import GovernmentNavigatorAgent
            return GovernmentNavigatorAgent(config_path, api_key)
        elif agent_type == "grant_management":
            from grant_management_agent import GrantManagementAgent
            return GrantManagementAgent(config_path, api_key)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

