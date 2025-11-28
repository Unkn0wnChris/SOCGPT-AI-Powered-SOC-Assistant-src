import streamlit as st
from src.ollama_client import ollama_query
from src.persona import Analyst_Persona
from src.summarizer import summarize_alert
from src.triage import triage_alert
from src.remediation import suggest_remediation
from src.mitre_mapper import MITRE_Mapping

# Streamlit UI Config
st.set_page_config(page_title="SOCGPT", layout="wide")
st.title("🔍 SOC AI-Powered Assistant")

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "logs" not in st.session_state:
    st.session_state.logs = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    Persona = st.selectbox("Select Analyst Persona", list(Analyst_Persona.keys()))
    st.markdown("📁 Upload Log File")
    uploaded_file = st.file_uploader("Choose log file", type=["txt", "log", "json"])

# Parsing logs
if uploaded_file:
    file_contents = uploaded_file.read().decode().splitlines()
    st.session_state.logs = file_contents

    st.subheader("📄 Uploaded Logs")
    for log in st.session_state.logs:
        st.code(log)

# AI log analysis
if st.session_state.logs:
    st.subheader("🧠 AI Log Analysis")

    for log in st.session_state.logs:
        with st.expander(f"📌 Log: {log[:80]}..."):
            st.write("📍 **Summary**")
            st.write(summarize_alert(log))

            st.write("🚨 **Severity Triage**")
            st.write(triage_alert(log))

            st.write("🎯 **MITRE ATT&CK Mapping**")
            mitre_result = MITRE_Mapping(log)
            st.write(mitre_result)

            if mitre_result != "No MITRE ATT&CK technique identified":
                for technique in mitre_result.split(","):
                    tech_id = technique.split(":")[0].strip()
                    st.markdown(f"- 🔗 [View {tech_id} on MITRE](https://attack.mitre.org/techniques/{tech_id})")

            st.write("🛡️ **Recommended Remediation**")
            remediation_text = suggest_remediation(log)
            st.write(remediation_text)


# Chatbot
st.subheader("💬 SOC GPT Chatbot")
user_message = st.text_input("Ask a question about the logs, SOC procedures, or investigation:")

if user_message:
    mitre_summary = [MITRE_Mapping(l) for l in st.session_state.logs]
    persona_prompt = Analyst_Persona[Persona]

    full_prompt = f"""
{persona_prompt}

You are assisting in a SOC investigation.
Logs:
{st.session_state.logs}

Mapped MITRE Techniques:
{mitre_summary}

User question:
{user_message}
"""
    ai_response = ollama_query(full_prompt)

    st.session_state.chat_history.append(("You", user_message))
    st.session_state.chat_history.append(("SOCGPT", ai_response))

# Display Chat History
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
