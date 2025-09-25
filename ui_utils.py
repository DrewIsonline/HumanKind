import streamlit as st
import plotly.express as px

class UIComponents:
    @staticmethod
    def setup_page_config():
        st.set_page_config(
            page_title="HumanKind",
            page_icon="🤝",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    @staticmethod
    def load_custom_css():
        """Load external branding.css for consistent styling"""
        try:
            with open("branding.css") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("⚠️ branding.css not found. Default Streamlit styles applied.")

    @staticmethod
    def display_header(title: str, subtitle: str = ""):
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<h3>{subtitle}</h3>", unsafe_allow_html=True)

    @staticmethod
    def display_section_header(title: str):
        st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)

    @staticmethod
    def display_info_box(message: str, box_type: str = "info"):
        """Reusable styled info/success/error boxes"""
        css_class = {
            "info": "info-box",
            "success": "success-box",
            "error": "error-box"
        }.get(box_type, "info-box")

        st.markdown(f"<div class='{css_class}'>{message}</div>", unsafe_allow_html=True)


class DataVisualization:
    @staticmethod
    def line_chart(df, x: str, y: str, title: str):
        fig = px.line(df, x=x, y=y, title=title, markers=True)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f9f9f9"),
            title=dict(font=dict(size=20, color="#FF9900"))
        )
        return fig


class FormComponents:
    @staticmethod
    def input_text(label: str, key: str = None):
        return st.text_input(label, key=key)

    @staticmethod
    def input_number(label: str, key: str = None, min_val: int = 0, max_val: int = 100):
        return st.number_input(label, min_value=min_val, max_value=max_val, key=key)

    @staticmethod
    def input_textarea(label: str, key: str = None):
        return st.text_area(label, key=key)

    @staticmethod
    def submit_button(label: str, key: str = None):
        return st.button(label, key=key)
