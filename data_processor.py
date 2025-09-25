"""
Data Processing Utilities for AI Agent Platform
Provides common data processing functions for all agents
"""

import pandas as pd
import numpy as np
import json
import csv
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import re
import sqlite3
from pathlib import Path
import logging

class DataProcessor:
    """Common data processing utilities"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-.,!?@]', '', text)
        
        return text
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Check if it's a valid length (10-15 digits)
        return 10 <= len(digits) <= 15
    
    def parse_date(self, date_str: str, formats: List[str] = None) -> Optional[datetime]:
        """Parse date string with multiple format attempts"""
        if not date_str:
            return None
        
        if formats is None:
            formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%Y-%m-%d %H:%M:%S',
                '%m/%d/%Y %H:%M:%S',
                '%d/%m/%Y %H:%M:%S'
            ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        self.logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def calculate_age(self, birth_date: Union[str, datetime]) -> Optional[int]:
        """Calculate age from birth date"""
        if isinstance(birth_date, str):
            birth_date = self.parse_date(birth_date)
        
        if birth_date is None:
            return None
        
        today = datetime.now()
        age = today.year - birth_date.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age
    
    def normalize_currency(self, amount: Union[str, float, int]) -> Optional[float]:
        """Normalize currency values"""
        if isinstance(amount, (int, float)):
            return float(amount)
        
        if isinstance(amount, str):
            # Remove currency symbols and commas
            amount = re.sub(r'[$,€£¥]', '', amount.strip())
            try:
                return float(amount)
            except ValueError:
                self.logger.warning(f"Could not parse currency: {amount}")
                return None
        
        return None
    
    def categorize_numeric_value(self, value: float, thresholds: Dict[str, float]) -> str:
        """Categorize numeric value based on thresholds"""
        for category, threshold in sorted(thresholds.items(), key=lambda x: x[1]):
            if value <= threshold:
                return category
        
        # Return the highest category if value exceeds all thresholds
        return max(thresholds.keys(), key=lambda x: thresholds[x])
    
    def calculate_statistics(self, data: List[Union[int, float]]) -> Dict[str, float]:
        """Calculate basic statistics for numeric data"""
        if not data:
            return {}
        
        data = [x for x in data if x is not None]
        if not data:
            return {}
        
        return {
            'count': len(data),
            'mean': np.mean(data),
            'median': np.median(data),
            'std': np.std(data),
            'min': min(data),
            'max': max(data),
            'q25': np.percentile(data, 25),
            'q75': np.percentile(data, 75)
        }
    
    def detect_outliers(self, data: List[Union[int, float]], method: str = 'iqr') -> List[int]:
        """Detect outliers in numeric data"""
        if not data:
            return []
        
        data = np.array([x for x in data if x is not None])
        if len(data) == 0:
            return []
        
        if method == 'iqr':
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = []
            for i, value in enumerate(data):
                if value < lower_bound or value > upper_bound:
                    outliers.append(i)
            
            return outliers
        
        elif method == 'zscore':
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
            return [i for i, z in enumerate(z_scores) if z > 3]
        
        return []
    
    def group_data_by_period(self, data: List[Dict], date_field: str, period: str = 'month') -> Dict[str, List[Dict]]:
        """Group data by time period"""
        grouped = {}
        
        for item in data:
            date_value = item.get(date_field)
            if not date_value:
                continue
            
            if isinstance(date_value, str):
                date_value = self.parse_date(date_value)
            
            if date_value is None:
                continue
            
            if period == 'day':
                key = date_value.strftime('%Y-%m-%d')
            elif period == 'week':
                # Get Monday of the week
                monday = date_value - timedelta(days=date_value.weekday())
                key = monday.strftime('%Y-%m-%d')
            elif period == 'month':
                key = date_value.strftime('%Y-%m')
            elif period == 'quarter':
                quarter = (date_value.month - 1) // 3 + 1
                key = f"{date_value.year}-Q{quarter}"
            elif period == 'year':
                key = str(date_value.year)
            else:
                key = date_value.strftime('%Y-%m-%d')
            
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        
        return grouped
    
    def calculate_trends(self, data: List[Union[int, float]], periods: int = 3) -> Dict[str, Any]:
        """Calculate trend analysis"""
        if len(data) < periods:
            return {'trend': 'insufficient_data', 'slope': 0, 'r_squared': 0}
        
        x = np.arange(len(data))
        y = np.array(data)
        
        # Calculate linear regression
        slope, intercept = np.polyfit(x, y, 1)
        
        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Determine trend direction
        if abs(slope) < 0.01:
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'
        
        return {
            'trend': trend,
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'strength': 'strong' if r_squared > 0.7 else 'moderate' if r_squared > 0.3 else 'weak'
        }

class DatabaseManager:
    """Database management utilities"""
    
    def __init__(self, db_path: str = "agent_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with common tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute query and return results as list of dictionaries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """Execute update/insert query and return affected rows"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def create_user(self, username: str, email: str) -> Optional[int]:
        """Create new user"""
        try:
            query = "INSERT INTO users (username, email) VALUES (?, ?)"
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (username, email))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        results = self.execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
        return results[0] if results else None
    
    def log_action(self, user_id: int, action: str, details: str = None):
        """Log user action"""
        query = "INSERT INTO logs (user_id, action, details) VALUES (?, ?, ?)"
        self.execute_update(query, (user_id, action, details))
    
    def save_session_data(self, user_id: int, session_data: Dict):
        """Save session data"""
        data_json = json.dumps(session_data)
        query = '''
            INSERT OR REPLACE INTO sessions (user_id, session_data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        '''
        self.execute_update(query, (user_id, data_json))
    
    def load_session_data(self, user_id: int) -> Optional[Dict]:
        """Load session data"""
        results = self.execute_query(
            "SELECT session_data FROM sessions WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1",
            (user_id,)
        )
        if results:
            try:
                return json.loads(results[0]['session_data'])
            except json.JSONDecodeError:
                return None
        return None

class ReportGenerator:
    """Generate reports and summaries"""
    
    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
    
    def generate_summary_report(self, data: List[Dict], title: str = "Summary Report") -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        if not data:
            return {'title': title, 'error': 'No data available'}
        
        report = {
            'title': title,
            'generated_at': datetime.now().isoformat(),
            'total_records': len(data),
            'summary': {}
        }
        
        # Analyze numeric fields
        numeric_fields = []
        for key in data[0].keys():
            values = [item.get(key) for item in data if item.get(key) is not None]
            if values and all(isinstance(v, (int, float)) for v in values):
                numeric_fields.append(key)
                report['summary'][key] = self.data_processor.calculate_statistics(values)
        
        # Analyze categorical fields
        categorical_fields = []
        for key in data[0].keys():
            if key not in numeric_fields:
                values = [str(item.get(key, '')) for item in data if item.get(key)]
                if values:
                    categorical_fields.append(key)
                    value_counts = {}
                    for value in values:
                        value_counts[value] = value_counts.get(value, 0) + 1
                    
                    report['summary'][key] = {
                        'unique_values': len(value_counts),
                        'most_common': max(value_counts.items(), key=lambda x: x[1]) if value_counts else None,
                        'distribution': dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:10])
                    }
        
        report['field_types'] = {
            'numeric': numeric_fields,
            'categorical': categorical_fields
        }
        
        return report
    
    def generate_trend_report(self, data: List[Dict], date_field: str, value_field: str, period: str = 'month') -> Dict[str, Any]:
        """Generate trend analysis report"""
        grouped_data = self.data_processor.group_data_by_period(data, date_field, period)
        
        trend_data = []
        for period_key in sorted(grouped_data.keys()):
            period_items = grouped_data[period_key]
            values = [item.get(value_field) for item in period_items if item.get(value_field) is not None]
            
            if values:
                trend_data.append({
                    'period': period_key,
                    'count': len(period_items),
                    'total': sum(values),
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                })
        
        # Calculate overall trend
        if len(trend_data) >= 3:
            averages = [item['average'] for item in trend_data]
            trend_analysis = self.data_processor.calculate_trends(averages)
        else:
            trend_analysis = {'trend': 'insufficient_data'}
        
        return {
            'title': f'Trend Analysis: {value_field} by {period}',
            'generated_at': datetime.now().isoformat(),
            'period_data': trend_data,
            'trend_analysis': trend_analysis,
            'total_periods': len(trend_data)
        }

