import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from typing import List

# ==============================================
# HumanKind UI Utilities
# Modernized Streamlit components with branding
# ==============================================

class UIComponents:
    """Reusable UI components for HumanKind"""

    @staticmethod
    def setup_page_config():
        st.set_page_config(
            page_title="HumanKind",
            page_icon="assets/humankind_logo.png",  # hardcoded logo as favicon
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Sidebar branding
        st.sidebar.image("assets/humankind_logo.png", use_container_width=True)
        st.sidebar.markdown("### HumanKind\nAI Care. Human First.")

    @staticmethod
    def load_custom_css():
        """Inject HumanKind branding styles"""
        css = """
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(90deg, #FF9900, #4DB6AC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.8rem;
            font-weight: bold;
            color: #2C3E50;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #4DB6AC;
            padding-bottom: 0.5rem;
        }
        .info-box {
            background: #f0f8ff;
            padding: 1.2rem;
            border-radius: 10px;
            border-left: 5px solid #FF9900;
            margin: 1rem 0;
        }
        .error-box {
            background: #fff5f5;
            padding: 1.2rem;
            border-radius: 10px;
            border-left: 5px solid #f44336;
            margin: 1rem 0;
        }
        .primary-button {
            background: linear-gradient(45deg, #FF9900, #4DB6AC);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def display_header(title: str, subtitle: str = None):
        st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
        if subtitle:
            st.markdown(f'<div style="text-align:center;color:#666;font-size:1.2rem;">{subtitle}</div>', unsafe_allow_html=True)

    @staticmethod
    def display_section_header(title: str):
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

    @staticmethod
    def display_info_box(message: str, box_type: str = "info"):
        css_class = "info-box" if box_type == "info" else "error-box"
        st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)

class DataVisualization:
    """Charts for HumanKind"""

    @staticmethod
    def line_chart(data: pd.DataFrame, x: str, y: str, title: str = "Line Chart"):
        fig = px.line(data, x=x, y=y, title=title, color_discrete_sequence=["#FF9900"])
        return fig

    @staticmethod
    def bar_chart(data: pd.DataFrame, x: str, y: str, title: str = "Bar Chart"):
        fig = px.bar(data, x=x, y=y, title=title, color_discrete_sequence=["#4DB6AC"])
        return fig

class FormComponents:
    """Form fields for HumanKind"""

    @staticmethod
    def input_text(label: str, key: str):
        return st.text_input(label, key=key)

    @staticmethod
    def input_textarea(label: str, key: str):
        return st.text_area(label, key=key)

    @staticmethod
    def input_number(label: str, key: str, min_val=0, max_val=100, step=1):
        return st.number_input(label, key=key, min_value=min_val, max_value=max_val, step=step)

    @staticmethod
    def submit_button(label: str, key: str = None):
        return st.button(label, key=key)

class FileManager:
    """File utilities for HumanKind"""

    @staticmethod
    def save_uploaded_file(uploaded_file, save_path: str) -> bool:
        try:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return True
        except Exception as e:
            st.error(f"⚠️ Oops — could not save file: {e}")
            return False

    @staticmethod
    def export_dataframe_to_csv(df: pd.DataFrame, filename: str = "data.csv"):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

    @staticmethod
    def export_dataframe_to_excel(df: pd.DataFrame, filename: str = "data.xlsx"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        b64 = base64.b64encode(output.getvalue()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel</a>'
        st.markdown(href, unsafe_allow_html=True)