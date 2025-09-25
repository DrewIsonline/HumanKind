# HumanKind — AI Elderly Care Assistant

HumanKind is your AI-powered elderly care coordination system, designed to support families, caregivers, and seniors with compassion and technology.

## ✨ Features
- ✅ Health monitoring and vital signs tracking  
- ✅ Medication management and reminders  
- ✅ Appointment scheduling and coordination  
- ✅ Caregiver management and scheduling  
- ✅ Emergency contact management  
- ✅ Daily activity tracking  
- ✅ AI-powered care recommendations  

## 🚀 Quick Start
1. Clone the repository:
```bash
git clone https://github.com/your-username/HumanKind.git
cd HumanKind
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run humankind_app.py
```

## 📂 Project Structure
```
HumanKind/
 ├── humankind_app.py        # Streamlit entrypoint (UI pages)
 ├── humankind_agent.py      # Logic layer (subclass of BaseAgent)
 ├── base_agent.py           # Framework/abstract class
 ├── ui_utils.py             # Branded UI toolkit
 ├── requirements.txt        # Dependencies
 ├── README.md               # Project documentation
 ├── LICENSE                 # License terms
 ├── .gitignore              # GitHub ignore rules
 └── assets/
      └── humankind_logo.png # Logo (favicon + sidebar)
```

## 📌 Notes
- Built with [Streamlit](https://streamlit.io/) for a simple, web-based interface.  
- Modular design: `HumanKindAgent` handles logic, while `humankind_app.py` handles the UI.  
- Extendable: add new analytics or features by expanding `humankind_agent.py` and `ui_utils.py`.  

---
Built with ❤️ by Drew — *AI Care. Human First.*

