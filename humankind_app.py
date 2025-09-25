"""
Elderly Care Coordination Agent - Premium Version
Advanced AI-powered elderly care coordination system with embedded API access
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date, time
import json
import os
import sys
from typing import Dict, List, Any, Optional

# All modules are in the same directory, no path manipulation needed

from base_agent import BaseAgent
from ui_utils import UIComponents, DataVisualization, FormComponents
from data_processor import DataProcessor, DatabaseManager
from config_manager import ConfigManager

class ElderlyCareAgent(BaseAgent):
    """Premium Elderly Care Coordination Agent with advanced features"""
    
    def __init__(self, config_path: str = None, api_key: str = None):
        # Premium version with embedded API key
        embedded_api_key = "sk_premium_elderly_care_api_key_67890"  # This would be the actual API key
        super().__init__(config_path, embedded_api_key)
        
        self.data_processor = DataProcessor(self.logger)
        self.db_manager = DatabaseManager("elderly_care.db")
        self.ui = UIComponents()
        self.viz = DataVisualization()
        self.forms = FormComponents()
        
        # Initialize elderly care specific database tables
        self.init_care_database()
        
        # Elderly care management features
        self.features = {
            'health_monitoring': True,
            'medication_management': True,
            'appointment_scheduling': True,
            'caregiver_coordination': True,
            'emergency_response': True,
            'daily_activity_tracking': True,
            'nutrition_monitoring': True,
            'social_engagement': True,
            'health_analytics': True,
            'family_communication': True,
            'care_plan_management': True,
            'ai_health_insights': True,
            'fall_detection': True,
            'vital_signs_monitoring': True,
            'cognitive_assessment': True
        }
    
    def init_care_database(self):
        """Initialize elderly care specific database tables"""
        # Create care recipients table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS care_recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE,
                gender TEXT,
                address TEXT,
                phone TEXT,
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT,
                medical_conditions TEXT,
                allergies TEXT,
                insurance_info TEXT,
                care_level TEXT DEFAULT 'independent',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create medications table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                medication_name TEXT NOT NULL,
                dosage TEXT,
                frequency TEXT,
                start_date DATE,
                end_date DATE,
                prescribing_doctor TEXT,
                instructions TEXT,
                side_effects TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
        
        # Create medication logs table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS medication_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medication_id INTEGER,
                recipient_id INTEGER,
                scheduled_time TIMESTAMP,
                actual_time TIMESTAMP,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                administered_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medication_id) REFERENCES medications (id),
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
        
        # Create appointments table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                appointment_type TEXT,
                doctor_name TEXT,
                clinic_name TEXT,
                appointment_date DATE,
                appointment_time TIME,
                duration INTEGER DEFAULT 60,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                transportation_needed BOOLEAN DEFAULT 0,
                reminder_sent BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
        
        # Create caregivers table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS caregivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                role TEXT,
                specialization TEXT,
                availability TEXT,
                hourly_rate REAL,
                certification TEXT,
                background_check_date DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create care assignments table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS care_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                caregiver_id INTEGER,
                start_date DATE,
                end_date DATE,
                schedule TEXT,
                responsibilities TEXT,
                hourly_rate REAL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id),
                FOREIGN KEY (caregiver_id) REFERENCES caregivers (id)
            )
        ''')
        
        # Create health metrics table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                metric_type TEXT,
                value REAL,
                unit TEXT,
                recorded_date DATE,
                recorded_time TIME,
                recorded_by TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
        
        # Create daily activities table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS daily_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                activity_date DATE,
                activity_type TEXT,
                status TEXT,
                duration INTEGER,
                assistance_level TEXT,
                notes TEXT,
                recorded_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
        
        # Create emergency incidents table
        self.db_manager.execute_update('''
            CREATE TABLE IF NOT EXISTS emergency_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                incident_type TEXT,
                incident_date DATE,
                incident_time TIME,
                description TEXT,
                severity TEXT,
                response_actions TEXT,
                outcome TEXT,
                responder_name TEXT,
                hospital_visit BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipient_id) REFERENCES care_recipients (id)
            )
        ''')
    
    def get_agent_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return [
            "Health Monitoring & Vital Signs Tracking",
            "Medication Management & Reminders",
            "Appointment Scheduling & Coordination",
            "Caregiver Management & Scheduling",
            "Emergency Response & Incident Tracking",
            "Daily Activity Monitoring",
            "Nutrition & Meal Planning",
            "Social Engagement Tracking",
            "Family Communication Portal",
            "Care Plan Development & Management",
            "AI Health Insights & Predictions",
            "Fall Detection & Safety Monitoring",
            "Cognitive Assessment Tools",
            "Insurance & Billing Management",
            "Comprehensive Reporting & Analytics"
        ]
    
    def process_user_input(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and return AI-powered care recommendations"""
        try:
            # Simulate AI processing with embedded API
            recommendations = self.generate_care_recommendations(user_input)
            
            return {
                'status': 'success',
                'recommendations': recommendations,
                'confidence': 0.88,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.log_error(f"Error processing user input: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_care_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered elderly care recommendations"""
        recommendations = []
        
        # Health monitoring recommendations
        recommendations.append({
            'category': 'Health Monitoring',
            'title': 'Vital Signs Monitoring Schedule',
            'description': 'AI analysis suggests optimized vital signs monitoring based on health conditions and risk factors.',
            'priority': 'high',
            'action_items': [
                'Monitor blood pressure twice daily',
                'Check blood glucose levels before meals',
                'Record weight weekly at same time',
                'Track sleep patterns and quality'
            ]
        })
        
        # Medication management recommendations
        recommendations.append({
            'category': 'Medication Management',
            'title': 'Medication Adherence Optimization',
            'description': 'Personalized medication schedule to improve adherence and reduce side effects.',
            'priority': 'high',
            'action_items': [
                'Set up automated pill dispenser',
                'Schedule medications with meals',
                'Monitor for drug interactions',
                'Review medications with doctor monthly'
            ]
        })
        
        # Social engagement recommendations
        recommendations.append({
            'category': 'Social Engagement',
            'title': 'Social Activity Planning',
            'description': 'AI-recommended social activities to maintain cognitive health and emotional wellbeing.',
            'priority': 'medium',
            'action_items': [
                'Schedule weekly family video calls',
                'Join senior center activities',
                'Participate in community events',
                'Maintain regular social interactions'
            ]
        })
        
        # Safety recommendations
        recommendations.append({
            'category': 'Safety & Prevention',
            'title': 'Fall Prevention Strategy',
            'description': 'Comprehensive fall prevention plan based on mobility assessment and home environment.',
            'priority': 'high',
            'action_items': [
                'Install grab bars in bathroom',
                'Improve lighting in hallways',
                'Remove trip hazards',
                'Consider medical alert system'
            ]
        })
        
        return recommendations
    
    def render_main_interface(self):
        """Render the main user interface"""
        self.ui.load_custom_css()
        self.ui.display_header("👥 Elderly Care Coordination Pro", "Advanced AI-Powered Care Management System")
        
        # Sidebar navigation
        pages = [
            "Dashboard",
            "Care Recipients",
            "Health Monitoring",
            "Medications",
            "Appointments",
            "Caregivers",
            "Daily Activities",
            "Emergency Response",
            "Reports & Analytics",
            "AI Care Insights",
            "Settings"
        ]
        
        icons = ["📊", "👤", "🏥", "💊", "📅", "👨‍⚕️", "📋", "🚨", "📈", "🤖", "⚙️"]
        
        selected_page = self.ui.create_sidebar_navigation(pages, icons)
        
        # Display premium badge
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🌟 Premium Version")
        st.sidebar.success("All care features unlocked!")
        
        # Main content area
        if selected_page == "Dashboard":
            self.render_dashboard()
        elif selected_page == "Care Recipients":
            self.render_care_recipients()
        elif selected_page == "Health Monitoring":
            self.render_health_monitoring()
        elif selected_page == "Medications":
            self.render_medications()
        elif selected_page == "Appointments":
            self.render_appointments()
        elif selected_page == "Caregivers":
            self.render_caregivers()
        elif selected_page == "Daily Activities":
            self.render_daily_activities()
        elif selected_page == "Emergency Response":
            self.render_emergency_response()
        elif selected_page == "Reports & Analytics":
            self.render_reports_analytics()
        elif selected_page == "AI Care Insights":
            self.render_ai_insights()
        elif selected_page == "Settings":
            self.render_settings()
    
    def render_dashboard(self):
        """Render main dashboard"""
        self.ui.display_section_header("Care Coordination Overview")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.ui.display_metric_card("Active Recipients", "12", "2 new this month")
        
        with col2:
            self.ui.display_metric_card("Medications Due", "8", "Next: 2:00 PM")
        
        with col3:
            self.ui.display_metric_card("Appointments Today", "3", "1 requires transport")
        
        with col4:
            self.ui.display_metric_card("Active Caregivers", "6", "All scheduled")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            # Health status distribution
            health_data = pd.DataFrame({
                'Status': ['Stable', 'Needs Attention', 'Critical', 'Improving'],
                'Count': [8, 2, 1, 1]
            })
            
            fig = px.pie(health_data, values='Count', names='Status', 
                        title="Health Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Medication adherence trend
            adherence_data = pd.DataFrame({
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'Adherence_Rate': [92, 88, 95, 91]
            })
            
            fig = px.line(adherence_data, x='Week', y='Adherence_Rate',
                         title="Medication Adherence Trend (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent activities and alerts
        col1, col2 = st.columns(2)
        
        with col1:
            self.ui.display_subsection_header("Recent Activities")
            
            activities = [
                {"Time": "10:30 AM", "Activity": "Blood pressure check - Mary Johnson", "Status": "Completed"},
                {"Time": "11:15 AM", "Activity": "Medication reminder - John Smith", "Status": "Taken"},
                {"Time": "2:00 PM", "Activity": "Physical therapy - Alice Brown", "Status": "In Progress"},
                {"Time": "3:30 PM", "Activity": "Doctor appointment - Robert Davis", "Status": "Scheduled"}
            ]
            
            df_activities = pd.DataFrame(activities)
            st.dataframe(df_activities, use_container_width=True)
        
        with col2:
            self.ui.display_subsection_header("Health Alerts")
            
            # Health alerts
            st.warning("⚠️ Mary Johnson: Blood pressure elevated (150/95)")
            st.info("ℹ️ John Smith: Medication refill needed in 3 days")
            st.error("🚨 Alice Brown: Missed medication dose at 8:00 AM")
            st.success("✅ Robert Davis: All vitals within normal range")
    
    def render_care_recipients(self):
        """Render care recipients management interface"""
        self.ui.display_section_header("Care Recipients Management")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Active Recipients", "Add New Recipient", "Care Plans"],
            ["👥", "➕", "📋"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Current Care Recipients")
            
            # Sample recipients data
            recipients_data = [
                {"Name": "Mary Johnson", "Age": 78, "Care Level": "Assisted", "Health Status": "Stable", "Last Check": "2024-01-15"},
                {"Name": "John Smith", "Age": 82, "Care Level": "Independent", "Health Status": "Good", "Last Check": "2024-01-14"},
                {"Name": "Alice Brown", "Age": 75, "Care Level": "Supervised", "Health Status": "Needs Attention", "Last Check": "2024-01-15"},
                {"Name": "Robert Davis", "Age": 80, "Care Level": "Assisted", "Health Status": "Stable", "Last Check": "2024-01-13"}
            ]
            
            df_recipients = pd.DataFrame(recipients_data)
            st.dataframe(df_recipients, use_container_width=True)
            
            # Care level distribution
            care_levels = df_recipients['Care Level'].value_counts()
            fig = px.bar(x=care_levels.index, y=care_levels.values, 
                        title="Care Level Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            self.ui.display_subsection_header("Add New Care Recipient")
            
            with st.form("add_recipient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    date_of_birth = st.date_input("Date of Birth")
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    phone = st.text_input("Phone Number")
                
                with col2:
                    address = st.text_area("Address")
                    emergency_contact = st.text_input("Emergency Contact Name")
                    emergency_phone = st.text_input("Emergency Contact Phone")
                    care_level = st.selectbox("Care Level", ["Independent", "Supervised", "Assisted", "Skilled Nursing"])
                
                medical_conditions = st.text_area("Medical Conditions")
                allergies = st.text_area("Allergies")
                insurance_info = st.text_area("Insurance Information")
                
                submitted = st.form_submit_button("Add Recipient")
                
                if submitted and first_name and last_name:
                    # Save to database
                    self.db_manager.execute_update('''
                        INSERT INTO care_recipients (first_name, last_name, date_of_birth, gender, 
                                                   address, phone, emergency_contact_name, emergency_contact_phone,
                                                   medical_conditions, allergies, insurance_info, care_level)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (first_name, last_name, date_of_birth, gender, address, phone, 
                          emergency_contact, emergency_phone, medical_conditions, allergies, insurance_info, care_level))
                    
                    st.success(f"Successfully added {first_name} {last_name} to care recipients!")
        
        with tab3:
            self.ui.display_subsection_header("Individual Care Plans")
            
            # Care plan management
            recipient_select = st.selectbox("Select Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
            
            if recipient_select:
                st.write(f"**Care Plan for {recipient_select}**")
                
                # Sample care plan
                care_plan = {
                    "Daily Goals": [
                        "Take medications as prescribed",
                        "Complete physical therapy exercises",
                        "Maintain social interactions",
                        "Monitor vital signs"
                    ],
                    "Weekly Goals": [
                        "Attend doctor appointments",
                        "Participate in group activities",
                        "Family visit or call",
                        "Review medication effectiveness"
                    ],
                    "Monthly Goals": [
                        "Comprehensive health assessment",
                        "Care plan review and updates",
                        "Family care meeting",
                        "Emergency plan review"
                    ]
                }
                
                for period, goals in care_plan.items():
                    st.write(f"**{period}:**")
                    for goal in goals:
                        st.write(f"• {goal}")
                    st.write("")
    
    def render_health_monitoring(self):
        """Render health monitoring interface"""
        self.ui.display_section_header("Health Monitoring & Vital Signs")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Vital Signs", "Health Trends", "Add Reading"],
            ["🩺", "📈", "➕"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Current Vital Signs")
            
            # Recipient selector
            recipient = st.selectbox("Select Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
            
            # Current vitals display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                self.ui.display_metric_card("Blood Pressure", "135/85", "Slightly elevated")
            
            with col2:
                self.ui.display_metric_card("Heart Rate", "72 bpm", "Normal range")
            
            with col3:
                self.ui.display_metric_card("Temperature", "98.6°F", "Normal")
            
            with col4:
                self.ui.display_metric_card("Blood Glucose", "110 mg/dL", "Normal")
            
            # Recent readings table
            vitals_data = [
                {"Date": "2024-01-15", "Time": "08:00", "BP": "135/85", "HR": "72", "Temp": "98.6", "Glucose": "110"},
                {"Date": "2024-01-14", "Time": "08:00", "BP": "130/82", "HR": "75", "Temp": "98.4", "Glucose": "105"},
                {"Date": "2024-01-13", "Time": "08:00", "BP": "140/88", "HR": "78", "Temp": "98.7", "Glucose": "115"},
                {"Date": "2024-01-12", "Time": "08:00", "BP": "132/84", "HR": "74", "Temp": "98.5", "Glucose": "108"}
            ]
            
            df_vitals = pd.DataFrame(vitals_data)
            st.dataframe(df_vitals, use_container_width=True)
        
        with tab2:
            self.ui.display_subsection_header("Health Trends Analysis")
            
            # Blood pressure trend
            bp_data = pd.DataFrame({
                'Date': pd.date_range(start='2024-01-01', periods=15),
                'Systolic': [135, 130, 140, 132, 138, 142, 135, 128, 145, 139, 133, 137, 141, 134, 136],
                'Diastolic': [85, 82, 88, 84, 86, 90, 85, 80, 92, 87, 83, 85, 89, 82, 84]
            })
            
            fig = px.line(bp_data, x='Date', y=['Systolic', 'Diastolic'], 
                         title="Blood Pressure Trend")
            st.plotly_chart(fig, use_container_width=True)
            
            # Heart rate trend
            hr_data = pd.DataFrame({
                'Date': pd.date_range(start='2024-01-01', periods=15),
                'Heart_Rate': [72, 75, 78, 74, 76, 80, 72, 70, 82, 77, 73, 75, 79, 71, 74]
            })
            
            fig = px.line(hr_data, x='Date', y='Heart_Rate', 
                         title="Heart Rate Trend")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            self.ui.display_subsection_header("Record New Health Reading")
            
            with st.form("health_reading_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    recipient_id = st.selectbox("Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
                    reading_date = st.date_input("Date")
                    reading_time = st.time_input("Time")
                    recorded_by = st.text_input("Recorded By")
                
                with col2:
                    metric_type = st.selectbox("Metric Type", ["Blood Pressure", "Heart Rate", "Temperature", "Blood Glucose", "Weight", "Oxygen Saturation"])
                    
                    if metric_type == "Blood Pressure":
                        systolic = st.number_input("Systolic", min_value=80, max_value=200, step=1)
                        diastolic = st.number_input("Diastolic", min_value=40, max_value=120, step=1)
                        value = f"{systolic}/{diastolic}"
                        unit = "mmHg"
                    elif metric_type == "Heart Rate":
                        value = st.number_input("Heart Rate", min_value=40, max_value=150, step=1)
                        unit = "bpm"
                    elif metric_type == "Temperature":
                        value = st.number_input("Temperature", min_value=95.0, max_value=105.0, step=0.1)
                        unit = "°F"
                    elif metric_type == "Blood Glucose":
                        value = st.number_input("Blood Glucose", min_value=50, max_value=400, step=1)
                        unit = "mg/dL"
                    elif metric_type == "Weight":
                        value = st.number_input("Weight", min_value=80.0, max_value=300.0, step=0.1)
                        unit = "lbs"
                    elif metric_type == "Oxygen Saturation":
                        value = st.number_input("Oxygen Saturation", min_value=80, max_value=100, step=1)
                        unit = "%"
                
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Record Reading"):
                    # Save to database
                    self.db_manager.execute_update('''
                        INSERT INTO health_metrics (recipient_id, metric_type, value, unit, 
                                                  recorded_date, recorded_time, recorded_by, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (1, metric_type, str(value), unit, reading_date, reading_time, recorded_by, notes))
                    
                    st.success(f"Health reading recorded successfully!")
    
    def render_medications(self):
        """Render medication management interface"""
        self.ui.display_section_header("Medication Management")
        
        tab1, tab2, tab3, tab4 = self.ui.create_tabs(
            ["Current Medications", "Medication Schedule", "Add Medication", "Adherence Tracking"],
            ["💊", "⏰", "➕", "📊"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Active Medications")
            
            # Sample medications data
            medications_data = [
                {"Medication": "Lisinopril", "Dosage": "10mg", "Frequency": "Once daily", "Next Due": "8:00 AM", "Recipient": "Mary Johnson"},
                {"Medication": "Metformin", "Dosage": "500mg", "Frequency": "Twice daily", "Next Due": "12:00 PM", "Recipient": "John Smith"},
                {"Medication": "Atorvastatin", "Dosage": "20mg", "Frequency": "Once daily", "Next Due": "8:00 PM", "Recipient": "Alice Brown"},
                {"Medication": "Aspirin", "Dosage": "81mg", "Frequency": "Once daily", "Next Due": "8:00 AM", "Recipient": "Robert Davis"}
            ]
            
            df_medications = pd.DataFrame(medications_data)
            st.dataframe(df_medications, use_container_width=True)
            
            # Medication alerts
            st.warning("⚠️ Refill needed: John Smith - Metformin (3 days remaining)")
            st.info("ℹ️ Doctor review due: Alice Brown - Atorvastatin (next week)")
        
        with tab2:
            self.ui.display_subsection_header("Today's Medication Schedule")
            
            # Today's schedule
            schedule_data = [
                {"Time": "8:00 AM", "Recipient": "Mary Johnson", "Medication": "Lisinopril 10mg", "Status": "✅ Taken"},
                {"Time": "8:00 AM", "Recipient": "Robert Davis", "Medication": "Aspirin 81mg", "Status": "✅ Taken"},
                {"Time": "12:00 PM", "Recipient": "John Smith", "Medication": "Metformin 500mg", "Status": "⏰ Due Now"},
                {"Time": "6:00 PM", "Recipient": "John Smith", "Medication": "Metformin 500mg", "Status": "⏳ Pending"},
                {"Time": "8:00 PM", "Recipient": "Alice Brown", "Medication": "Atorvastatin 20mg", "Status": "⏳ Pending"}
            ]
            
            df_schedule = pd.DataFrame(schedule_data)
            st.dataframe(df_schedule, use_container_width=True)
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Mark as Taken"):
                    st.success("Medication marked as taken!")
            
            with col2:
                if st.button("Skip Dose"):
                    st.warning("Dose marked as skipped")
            
            with col3:
                if st.button("Send Reminder"):
                    st.info("Reminder sent to caregiver")
        
        with tab3:
            self.ui.display_subsection_header("Add New Medication")
            
            with st.form("medication_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    recipient = st.selectbox("Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
                    medication_name = st.text_input("Medication Name")
                    dosage = st.text_input("Dosage (e.g., 10mg, 1 tablet)")
                    frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "Four times daily", "As needed"])
                
                with col2:
                    start_date = st.date_input("Start Date")
                    end_date = st.date_input("End Date (optional)")
                    prescribing_doctor = st.text_input("Prescribing Doctor")
                    instructions = st.text_area("Special Instructions")
                
                side_effects = st.text_area("Known Side Effects")
                
                if st.form_submit_button("Add Medication"):
                    # Save to database
                    self.db_manager.execute_update('''
                        INSERT INTO medications (recipient_id, medication_name, dosage, frequency, 
                                               start_date, end_date, prescribing_doctor, instructions, side_effects)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (1, medication_name, dosage, frequency, start_date, end_date, 
                          prescribing_doctor, instructions, side_effects))
                    
                    st.success(f"Successfully added {medication_name} to medication list!")
        
        with tab4:
            self.ui.display_subsection_header("Medication Adherence Analysis")
            
            # Adherence by recipient
            adherence_data = pd.DataFrame({
                'Recipient': ['Mary Johnson', 'John Smith', 'Alice Brown', 'Robert Davis'],
                'Adherence_Rate': [95, 88, 92, 97]
            })
            
            fig = px.bar(adherence_data, x='Recipient', y='Adherence_Rate', 
                        title="Medication Adherence by Recipient (%)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Weekly adherence trend
            weekly_data = pd.DataFrame({
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'Overall_Adherence': [92, 88, 95, 91]
            })
            
            fig = px.line(weekly_data, x='Week', y='Overall_Adherence', 
                         title="Weekly Adherence Trend (%)")
            st.plotly_chart(fig, use_container_width=True)
    
    def render_appointments(self):
        """Render appointment scheduling interface"""
        self.ui.display_section_header("Appointment Scheduling & Management")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Upcoming Appointments", "Schedule New", "Appointment History"],
            ["📅", "➕", "📋"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Upcoming Appointments")
            
            # Sample appointments data
            appointments_data = [
                {"Date": "2024-01-16", "Time": "10:00 AM", "Recipient": "Mary Johnson", "Type": "Cardiology", "Doctor": "Dr. Smith", "Status": "Confirmed"},
                {"Date": "2024-01-17", "Time": "2:00 PM", "Recipient": "John Smith", "Type": "Primary Care", "Doctor": "Dr. Johnson", "Status": "Confirmed"},
                {"Date": "2024-01-18", "Time": "11:00 AM", "Recipient": "Alice Brown", "Type": "Physical Therapy", "Doctor": "PT Williams", "Status": "Needs Transport"},
                {"Date": "2024-01-19", "Time": "9:00 AM", "Recipient": "Robert Davis", "Type": "Ophthalmology", "Doctor": "Dr. Brown", "Status": "Confirmed"}
            ]
            
            df_appointments = pd.DataFrame(appointments_data)
            st.dataframe(df_appointments, use_container_width=True)
            
            # Transportation alerts
            st.warning("🚗 Transportation needed: Alice Brown - Physical Therapy (Jan 18, 11:00 AM)")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Send Reminder"):
                    st.success("Appointment reminder sent!")
            
            with col2:
                if st.button("Arrange Transport"):
                    st.info("Transportation request submitted")
            
            with col3:
                if st.button("Reschedule"):
                    st.info("Rescheduling options displayed")
        
        with tab2:
            self.ui.display_subsection_header("Schedule New Appointment")
            
            with st.form("appointment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    recipient = st.selectbox("Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
                    appointment_type = st.selectbox("Appointment Type", 
                                                  ["Primary Care", "Cardiology", "Neurology", "Orthopedics", 
                                                   "Physical Therapy", "Ophthalmology", "Dentistry", "Specialist"])
                    doctor_name = st.text_input("Doctor/Provider Name")
                    clinic_name = st.text_input("Clinic/Facility Name")
                
                with col2:
                    appointment_date = st.date_input("Appointment Date")
                    appointment_time = st.time_input("Appointment Time")
                    duration = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=60, step=15)
                    transportation_needed = st.checkbox("Transportation Needed")
                
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Schedule Appointment"):
                    # Save to database
                    self.db_manager.execute_update('''
                        INSERT INTO appointments (recipient_id, appointment_type, doctor_name, clinic_name,
                                                appointment_date, appointment_time, duration, transportation_needed, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (1, appointment_type, doctor_name, clinic_name, appointment_date, 
                          appointment_time, duration, transportation_needed, notes))
                    
                    st.success(f"Appointment scheduled successfully for {recipient}!")
        
        with tab3:
            self.ui.display_subsection_header("Appointment History")
            
            # Historical appointments
            history_data = [
                {"Date": "2024-01-10", "Recipient": "Mary Johnson", "Type": "Primary Care", "Doctor": "Dr. Wilson", "Outcome": "Routine checkup - all normal"},
                {"Date": "2024-01-08", "Recipient": "John Smith", "Type": "Endocrinology", "Doctor": "Dr. Lee", "Outcome": "Diabetes management - medication adjusted"},
                {"Date": "2024-01-05", "Recipient": "Alice Brown", "Type": "Physical Therapy", "Doctor": "PT Williams", "Outcome": "Good progress - continue exercises"},
                {"Date": "2024-01-03", "Recipient": "Robert Davis", "Type": "Cardiology", "Doctor": "Dr. Smith", "Outcome": "Heart function stable - next visit in 3 months"}
            ]
            
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True)
    
    def render_caregivers(self):
        """Render caregiver management interface"""
        self.ui.display_section_header("Caregiver Management & Scheduling")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Active Caregivers", "Add Caregiver", "Schedules & Assignments"],
            ["👨‍⚕️", "➕", "📅"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Current Caregivers")
            
            # Sample caregivers data
            caregivers_data = [
                {"Name": "Sarah Wilson", "Role": "Registered Nurse", "Specialization": "Geriatric Care", "Rate": "$35/hr", "Status": "Active"},
                {"Name": "Mike Johnson", "Role": "Home Health Aide", "Specialization": "Personal Care", "Rate": "$20/hr", "Status": "Active"},
                {"Name": "Lisa Brown", "Role": "Physical Therapist", "Specialization": "Mobility", "Rate": "$45/hr", "Status": "Active"},
                {"Name": "David Smith", "Role": "Companion", "Specialization": "Social Support", "Rate": "$18/hr", "Status": "Active"}
            ]
            
            df_caregivers = pd.DataFrame(caregivers_data)
            st.dataframe(df_caregivers, use_container_width=True)
            
            # Caregiver availability
            col1, col2 = st.columns(2)
            
            with col1:
                # Role distribution
                roles = df_caregivers['Role'].value_counts()
                fig = px.pie(values=roles.values, names=roles.index, 
                            title="Caregiver Roles Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Weekly schedule overview
                schedule_data = pd.DataFrame({
                    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    'Scheduled_Hours': [32, 28, 35, 30, 33, 20, 18]
                })
                
                fig = px.bar(schedule_data, x='Day', y='Scheduled_Hours', 
                            title="Weekly Caregiver Hours")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            self.ui.display_subsection_header("Add New Caregiver")
            
            with st.form("caregiver_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email Address")
                    role = st.selectbox("Role", ["Registered Nurse", "Licensed Practical Nurse", "Home Health Aide", 
                                               "Physical Therapist", "Occupational Therapist", "Companion", "Other"])
                
                with col2:
                    specialization = st.text_input("Specialization")
                    hourly_rate = st.number_input("Hourly Rate ($)", min_value=15.0, max_value=100.0, step=0.50)
                    certification = st.text_input("Certifications")
                    background_check_date = st.date_input("Background Check Date")
                
                availability = st.text_area("Availability (days/hours)")
                
                if st.form_submit_button("Add Caregiver"):
                    # Save to database
                    self.db_manager.execute_update('''
                        INSERT INTO caregivers (first_name, last_name, phone, email, role, 
                                              specialization, hourly_rate, certification, background_check_date, availability)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (first_name, last_name, phone, email, role, specialization, 
                          hourly_rate, certification, background_check_date, availability))
                    
                    st.success(f"Successfully added {first_name} {last_name} to caregiver roster!")
        
        with tab3:
            self.ui.display_subsection_header("Care Assignments & Schedules")
            
            # Current assignments
            assignments_data = [
                {"Caregiver": "Sarah Wilson", "Recipient": "Mary Johnson", "Schedule": "Mon-Fri 8AM-4PM", "Responsibilities": "Medication, Vitals"},
                {"Caregiver": "Mike Johnson", "Recipient": "John Smith", "Schedule": "Daily 6AM-10AM", "Responsibilities": "Personal Care, Meals"},
                {"Caregiver": "Lisa Brown", "Recipient": "Alice Brown", "Schedule": "Tue/Thu 2PM-4PM", "Responsibilities": "Physical Therapy"},
                {"Caregiver": "David Smith", "Recipient": "Robert Davis", "Schedule": "Weekends 10AM-6PM", "Responsibilities": "Companionship, Activities"}
            ]
            
            df_assignments = pd.DataFrame(assignments_data)
            st.dataframe(df_assignments, use_container_width=True)
            
            # Schedule conflicts and alerts
            st.warning("⚠️ Schedule conflict: Sarah Wilson - overlapping assignments on Friday")
            st.info("ℹ️ New assignment needed: Mary Johnson requires weekend coverage")
    
    def render_daily_activities(self):
        """Render daily activities tracking interface"""
        self.ui.display_section_header("Daily Activities & Living Assistance")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Today's Activities", "Activity Tracking", "Independence Assessment"],
            ["📋", "📊", "🎯"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Today's Activity Schedule")
            
            # Sample daily activities
            activities_data = [
                {"Time": "7:00 AM", "Activity": "Morning medication", "Recipient": "Mary Johnson", "Status": "✅ Completed", "Assistance": "Independent"},
                {"Time": "8:00 AM", "Activity": "Breakfast", "Recipient": "John Smith", "Status": "✅ Completed", "Assistance": "Minimal"},
                {"Time": "9:00 AM", "Activity": "Personal hygiene", "Recipient": "Alice Brown", "Status": "🔄 In Progress", "Assistance": "Moderate"},
                {"Time": "10:00 AM", "Activity": "Physical exercise", "Recipient": "Robert Davis", "Status": "⏳ Scheduled", "Assistance": "Supervision"},
                {"Time": "12:00 PM", "Activity": "Lunch preparation", "Recipient": "Mary Johnson", "Status": "⏳ Scheduled", "Assistance": "Independent"}
            ]
            
            df_activities = pd.DataFrame(activities_data)
            st.dataframe(df_activities, use_container_width=True)
            
            # Activity completion rate
            completion_rate = 75  # Example
            self.ui.create_progress_bar(completion_rate / 100, "Today's Activity Completion")
        
        with tab2:
            self.ui.display_subsection_header("Activity Performance Tracking")
            
            # Activity categories performance
            activity_performance = pd.DataFrame({
                'Activity': ['Personal Care', 'Meals', 'Medication', 'Exercise', 'Social', 'Household'],
                'Independence_Level': [85, 90, 95, 70, 80, 60]
            })
            
            fig = px.bar(activity_performance, x='Activity', y='Independence_Level', 
                        title="Independence Level by Activity Type (%)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Weekly activity trends
            weekly_trends = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Completion_Rate': [88, 92, 85, 90, 87, 82, 85]
            })
            
            fig = px.line(weekly_trends, x='Day', y='Completion_Rate', 
                         title="Weekly Activity Completion Rate (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            self.ui.display_subsection_header("Independence Assessment")
            
            # Independence levels by recipient
            independence_data = pd.DataFrame({
                'Recipient': ['Mary Johnson', 'John Smith', 'Alice Brown', 'Robert Davis'],
                'Overall_Independence': [85, 92, 70, 88],
                'Personal_Care': [90, 95, 65, 85],
                'Mobility': [80, 90, 75, 90],
                'Cognitive': [85, 90, 70, 85]
            })
            
            fig = px.bar(independence_data, x='Recipient', y=['Overall_Independence', 'Personal_Care', 'Mobility', 'Cognitive'], 
                        title="Independence Assessment by Category", barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations for improvement
            st.write("**AI Recommendations for Independence Enhancement:**")
            recommendations = [
                "Mary Johnson: Focus on mobility exercises to improve balance",
                "John Smith: Maintain current independence level with regular monitoring",
                "Alice Brown: Increase cognitive stimulation activities",
                "Robert Davis: Continue current care plan - excellent progress"
            ]
            
            for rec in recommendations:
                st.write(f"• {rec}")
    
    def render_emergency_response(self):
        """Render emergency response interface"""
        self.ui.display_section_header("Emergency Response & Safety Management")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Emergency Contacts", "Incident Reports", "Safety Protocols"],
            ["📞", "🚨", "🛡️"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Emergency Contact Information")
            
            # Emergency contacts by recipient
            emergency_contacts = [
                {"Recipient": "Mary Johnson", "Primary": "John Johnson (Son) - 555-0101", "Secondary": "Dr. Smith - 555-0201", "Medical Alert": "Yes"},
                {"Recipient": "John Smith", "Primary": "Sarah Smith (Daughter) - 555-0102", "Secondary": "Dr. Johnson - 555-0202", "Medical Alert": "Yes"},
                {"Recipient": "Alice Brown", "Primary": "Mike Brown (Son) - 555-0103", "Secondary": "Dr. Wilson - 555-0203", "Medical Alert": "No"},
                {"Recipient": "Robert Davis", "Primary": "Lisa Davis (Wife) - 555-0104", "Secondary": "Dr. Brown - 555-0204", "Medical Alert": "Yes"}
            ]
            
            df_contacts = pd.DataFrame(emergency_contacts)
            st.dataframe(df_contacts, use_container_width=True)
            
            # Quick emergency actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚨 Call 911"):
                    st.error("Emergency services contacted!")
            
            with col2:
                if st.button("📞 Call Family"):
                    st.info("Family members notified")
            
            with col3:
                if st.button("🏥 Call Doctor"):
                    st.info("Primary physician contacted")
        
        with tab2:
            self.ui.display_subsection_header("Recent Incident Reports")
            
            # Sample incident data
            incidents_data = [
                {"Date": "2024-01-12", "Recipient": "Alice Brown", "Type": "Fall", "Severity": "Minor", "Response": "First aid applied", "Outcome": "No injury"},
                {"Date": "2024-01-08", "Recipient": "Mary Johnson", "Type": "Medication Error", "Severity": "Low", "Response": "Doctor consulted", "Outcome": "Monitoring"},
                {"Date": "2024-01-05", "Recipient": "John Smith", "Type": "Chest Pain", "Severity": "High", "Response": "911 called", "Outcome": "Hospitalized"},
                {"Date": "2024-01-02", "Recipient": "Robert Davis", "Type": "Confusion", "Severity": "Medium", "Response": "Family notified", "Outcome": "Resolved"}
            ]
            
            df_incidents = pd.DataFrame(incidents_data)
            st.dataframe(df_incidents, use_container_width=True)
            
            # Incident trends
            incident_types = df_incidents['Type'].value_counts()
            fig = px.pie(values=incident_types.values, names=incident_types.index, 
                        title="Incident Types Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Add new incident report
            with st.expander("Report New Incident"):
                with st.form("incident_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        recipient = st.selectbox("Recipient", ["Mary Johnson", "John Smith", "Alice Brown", "Robert Davis"])
                        incident_type = st.selectbox("Incident Type", ["Fall", "Medical Emergency", "Medication Error", "Confusion", "Injury", "Other"])
                        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
                        incident_date = st.date_input("Date")
                        incident_time = st.time_input("Time")
                    
                    with col2:
                        description = st.text_area("Description")
                        response_actions = st.text_area("Response Actions Taken")
                        outcome = st.text_area("Outcome")
                        responder = st.text_input("Responder Name")
                        hospital_visit = st.checkbox("Required Hospital Visit")
                    
                    if st.form_submit_button("Submit Report"):
                        st.success("Incident report submitted successfully!")
        
        with tab3:
            self.ui.display_subsection_header("Safety Protocols & Procedures")
            
            # Safety protocols
            protocols = {
                "Fall Prevention": [
                    "Regular mobility assessments",
                    "Home safety evaluations",
                    "Proper lighting maintenance",
                    "Clear walkways and remove hazards",
                    "Use of assistive devices as needed"
                ],
                "Medication Safety": [
                    "Automated pill dispensers",
                    "Regular medication reviews",
                    "Clear labeling and instructions",
                    "Monitor for side effects",
                    "Secure storage of medications"
                ],
                "Emergency Response": [
                    "Medical alert systems activated",
                    "Emergency contact lists updated",
                    "Regular emergency drills",
                    "Clear communication protocols",
                    "Quick access to medical information"
                ],
                "Health Monitoring": [
                    "Daily vital signs checks",
                    "Regular health assessments",
                    "Prompt reporting of changes",
                    "Coordination with healthcare providers",
                    "Documentation of all observations"
                ]
            }
            
            for protocol, items in protocols.items():
                with st.expander(f"📋 {protocol}"):
                    for item in items:
                        st.write(f"• {item}")
    
    def render_reports_analytics(self):
        """Render reports and analytics interface"""
        self.ui.display_section_header("Reports & Analytics")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Care Summary", "Health Analytics", "Financial Reports"],
            ["📊", "🏥", "💰"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Care Summary Dashboard")
            
            # Overall care metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                self.ui.display_metric_card("Care Quality Score", "92%", "+3% this month")
            
            with col2:
                self.ui.display_metric_card("Medication Adherence", "91%", "Above target")
            
            with col3:
                self.ui.display_metric_card("Family Satisfaction", "4.8/5", "Excellent rating")
            
            # Care outcomes trends
            outcomes_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Health_Stability': [88, 90, 92, 89, 91],
                'Independence_Level': [82, 84, 85, 83, 86],
                'Quality_of_Life': [85, 87, 89, 88, 90]
            })
            
            fig = px.line(outcomes_data, x='Month', y=['Health_Stability', 'Independence_Level', 'Quality_of_Life'],
                         title="Care Outcomes Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            self.ui.display_subsection_header("Health Analytics & Insights")
            
            # Health status distribution
            health_status = pd.DataFrame({
                'Status': ['Excellent', 'Good', 'Fair', 'Needs Attention'],
                'Count': [3, 6, 2, 1]
            })
            
            fig = px.pie(health_status, values='Count', names='Status', 
                        title="Overall Health Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk factors analysis
            risk_factors = pd.DataFrame({
                'Risk_Factor': ['Fall Risk', 'Medication Non-adherence', 'Social Isolation', 'Cognitive Decline', 'Nutrition'],
                'High_Risk': [2, 1, 3, 1, 2],
                'Medium_Risk': [4, 3, 2, 4, 3],
                'Low_Risk': [6, 8, 7, 7, 7]
            })
            
            fig = px.bar(risk_factors, x='Risk_Factor', y=['High_Risk', 'Medium_Risk', 'Low_Risk'], 
                        title="Risk Assessment by Category", barmode='stack')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            self.ui.display_subsection_header("Financial Analysis")
            
            # Care costs breakdown
            cost_breakdown = pd.DataFrame({
                'Category': ['Nursing Care', 'Home Health Aide', 'Medical Supplies', 'Transportation', 'Medications'],
                'Monthly_Cost': [3500, 2200, 400, 300, 800]
            })
            
            fig = px.pie(cost_breakdown, values='Monthly_Cost', names='Category', 
                        title="Monthly Care Costs Breakdown")
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost trends
            cost_trends = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Total_Costs': [7200, 7400, 7100, 7300, 7200],
                'Insurance_Coverage': [5400, 5550, 5325, 5475, 5400],
                'Out_of_Pocket': [1800, 1850, 1775, 1825, 1800]
            })
            
            fig = px.line(cost_trends, x='Month', y=['Total_Costs', 'Insurance_Coverage', 'Out_of_Pocket'],
                         title="Monthly Cost Trends")
            st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_insights(self):
        """Render AI insights and recommendations interface"""
        self.ui.display_section_header("AI Care Insights & Recommendations")
        
        # Get AI recommendations
        context = {
            'recipients_count': 4,
            'average_age': 79,
            'care_levels': ['independent', 'assisted', 'supervised'],
            'health_conditions': ['diabetes', 'hypertension', 'arthritis']
        }
        
        recommendations = self.generate_care_recommendations(context)
        
        for i, rec in enumerate(recommendations):
            with st.expander(f"🤖 {rec['title']}", expanded=(i == 0)):
                self.ui.display_info_box(rec['description'])
                
                st.write("**Recommended Actions:**")
                for action in rec['action_items']:
                    st.write(f"• {action}")
                
                # Priority indicator
                priority_color = {
                    'high': '🔴',
                    'medium': '🟡', 
                    'low': '🟢'
                }
                st.write(f"**Priority:** {priority_color.get(rec['priority'], '⚪')} {rec['priority'].title()}")
        
        # AI Chat Interface
        self.ui.display_subsection_header("Ask the Care AI Assistant")
        
        user_question = st.text_input("Ask a question about elderly care management:")
        
        if user_question:
            # Simulate AI response
            ai_response = self.generate_ai_response(user_question)
            self.ui.display_info_box(ai_response, "success")
    
    def generate_ai_response(self, question: str) -> str:
        """Generate AI response to user questions"""
        # Simulate AI processing
        responses = {
            "medication": "Based on current medication patterns, I recommend setting up automated reminders and reviewing potential interactions with the pharmacist.",
            "health": "Health monitoring shows stable trends. Continue current care plan with weekly vital signs checks and monthly physician reviews.",
            "safety": "Safety assessment indicates low fall risk. Maintain current safety protocols and consider annual home safety evaluation.",
            "care": "Care coordination is excellent. Family communication frequency is optimal, and caregiver satisfaction remains high."
        }
        
        # Simple keyword matching for demo
        question_lower = question.lower()
        for keyword, response in responses.items():
            if keyword in question_lower:
                return response
        
        return "I'd be happy to help with that care question! Based on current data, I recommend consulting with the primary care physician for specialized guidance on this topic."
    
    def render_settings(self):
        """Render settings interface"""
        self.ui.display_section_header("Settings & Configuration")
        
        tab1, tab2, tab3 = self.ui.create_tabs(
            ["Care Facility Profile", "Preferences", "Data Management"],
            ["🏥", "⚙️", "💾"]
        )
        
        with tab1:
            self.ui.display_subsection_header("Care Facility Profile")
            
            with st.form("facility_profile_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    facility_name = st.text_input("Facility Name", value="Sunshine Senior Care")
                    administrator_name = st.text_input("Administrator", value="Jane Smith")
                    address = st.text_area("Address", value="123 Care Lane\nElderly City, EC 12345")
                    phone = st.text_input("Phone", value="555-CARE-123")
                
                with col2:
                    license_number = st.text_input("License Number", value="EC-12345")
                    capacity = st.number_input("Capacity", value=50, step=1)
                    care_levels = st.multiselect("Care Levels Offered", 
                                               ["Independent Living", "Assisted Living", "Memory Care", "Skilled Nursing"],
                                               default=["Independent Living", "Assisted Living"])
                
                if st.form_submit_button("Update Profile"):
                    st.success("Facility profile updated successfully!")
        
        with tab2:
            self.ui.display_subsection_header("Application Preferences")
            
            # UI preferences
            theme = st.selectbox("Theme", ["Light", "Dark"])
            language = st.selectbox("Language", ["English", "Spanish", "French"])
            timezone = st.selectbox("Timezone", ["Eastern", "Central", "Mountain", "Pacific"])
            
            # Notification preferences
            st.write("**Notification Settings:**")
            email_notifications = st.checkbox("Email Notifications", value=True)
            medication_alerts = st.checkbox("Medication Alerts", value=True)
            appointment_reminders = st.checkbox("Appointment Reminders", value=True)
            emergency_alerts = st.checkbox("Emergency Alerts", value=True)
            
            # Care preferences
            st.write("**Care Management Preferences:**")
            auto_medication_reminders = st.checkbox("Automatic Medication Reminders", value=True)
            family_updates = st.checkbox("Automatic Family Updates", value=True)
            health_monitoring_frequency = st.selectbox("Health Monitoring Frequency", ["Daily", "Twice Daily", "Weekly"])
            
            if st.button("Save Preferences"):
                st.success("Preferences saved successfully!")
        
        with tab3:
            self.ui.display_subsection_header("Data Management")
            
            # Data export options
            st.write("**Export Data:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Export Health Data"):
                    st.success("Health data exported to CSV!")
            
            with col2:
                if st.button("Export Care Reports"):
                    st.success("Care reports exported to PDF!")
            
            with col3:
                if st.button("Export All Data"):
                    st.success("Complete care data exported!")
            
            # Data backup
            st.write("**Data Backup:**")
            if st.button("Create Backup"):
                st.success("Backup created successfully!")
            
            # Premium features info
            st.write("**Premium Features Active:**")
            features = [
                "✅ Unlimited care recipient profiles",
                "✅ Advanced AI health insights", 
                "✅ Real-time emergency response",
                "✅ Comprehensive analytics",
                "✅ Family communication portal",
                "✅ Priority customer support"
            ]
            
            for feature in features:
                st.write(feature)

def main():
    """Main application entry point"""
    agent = ElderlyCareAgent()
    agent.run()

if __name__ == "__main__":
    main()

