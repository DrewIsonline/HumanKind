import streamlit as st
import pandas as pd

from ui_utils import UIComponents, DataVisualization, FormComponents, FileManager
from humankind_agent import HumanKindAgent

# ==============================================
# HumanKind App (v2)
# Streamlit entrypoint using HumanKindAgent logic
# ==============================================

def main():
    # Setup page and branding
    UIComponents.setup_page_config()
    UIComponents.load_custom_css()
    UIComponents.display_header("Welcome to HumanKind", "AI Care. Human First.")

    # Initialize agent
    agent = HumanKindAgent()

    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigate",
        [
            "Home",
            "Care Recipients",
            "Medications",
            "Appointments",
            "Visualization",
            "AI Assistant"
        ]
    )

    # --- Home Page ---
    if page == "Home":
        UIComponents.display_section_header("About HumanKind")
        UIComponents.display_info_box(
            "HumanKind is your AI-powered elderly care assistant, designed to support families, caregivers, and seniors with compassion and technology."
        )
        st.write("Capabilities:")
        for cap in agent.get_agent_capabilities():
            st.markdown(f"✅ {cap}")

    # --- Care Recipients ---
    elif page == "Care Recipients":
        UIComponents.display_section_header("Care Recipients")
        name = FormComponents.input_text("Recipient Name", key="recipient_name")
        age = FormComponents.input_number("Age", key="recipient_age", min_val=0, max_val=120)
        if FormComponents.submit_button("Add Recipient", key="add_recipient"):
            result = agent.process_user_input({
                "action": "add_recipient",
                "data": {"name": name, "age": age}
            })
            UIComponents.display_info_box(result["message"], "error" if result["status"] == "error" else "info")

    # --- Medications ---
    elif page == "Medications":
        UIComponents.display_section_header("Medications")
        med_name = FormComponents.input_text("Medication Name", key="med_name")
        dosage = FormComponents.input_text("Dosage", key="med_dosage")
        if FormComponents.submit_button("Add Medication", key="add_med"):
            result = agent.process_user_input({
                "action": "add_medication",
                "data": {"name": med_name, "dosage": dosage}
            })
            UIComponents.display_info_box(result["message"], "error" if result["status"] == "error" else "info")

    # --- Appointments ---
    elif page == "Appointments":
        UIComponents.display_section_header("Appointments")
        st.info("Appointment scheduling will be added in future versions.")

    # --- Visualization ---
    elif page == "Visualization":
        UIComponents.display_section_header("Visualization")
        data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "Mood": [7, 6, 8, 5, 9]
        })
        st.write("Sample data:", data)
        fig = DataVisualization.line_chart(data, x="Day", y="Mood", title="Mood Tracker")
        st.plotly_chart(fig, use_container_width=True)

    # --- AI Assistant ---
    elif page == "AI Assistant":
        UIComponents.display_section_header("AI Assistant")
        user_prompt = FormComponents.input_textarea("Ask HumanKind anything:", key="ai_prompt")
        if FormComponents.submit_button("Get Response", key="ai_btn"):
            response = agent.generate_ai_response(user_prompt)
            UIComponents.display_info_box(response)

if __name__ == "__main__":
    main()
