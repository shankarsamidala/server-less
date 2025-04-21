import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page setup
st.set_page_config(page_title="📬 Serverless Feedback App", layout="wide")
st.title("📬 Serverless Feedback Collector")
st.caption("Simulating a serverless app with Lambda-style feedback processing and metrics")

# Session initialization
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []
if "lambda_logs" not in st.session_state:
    st.session_state.lambda_logs = []

# Sidebar – IAM roles
st.sidebar.header("🔐 IAM Role Configuration")
iam_roles = ["lambda-basic-execution", "cloudwatch-logs", "dynamodb-access", "s3-readonly"]
selected_roles = st.sidebar.multiselect("Attach IAM Roles", iam_roles, default=iam_roles[:2])

# -------------------------------
# Metrics Section
# -------------------------------
st.markdown("### 📊 Serverless Function Metrics")
col1, col2, col3 = st.columns(3)

total_requests = len(st.session_state.lambda_logs)
avg_memory = int(
    sum(log["Memory Used (MB)"] for log in st.session_state.lambda_logs) / total_requests
) if total_requests else 0
feedback_count = len(st.session_state.feedback_data)

col1.metric("📥 Total Requests", total_requests)
col2.metric("🧠 Avg Memory Used", f"{avg_memory} MB")
col3.metric("💬 Feedback Entries", feedback_count)

# -------------------------------
# Feedback Form
# -------------------------------
st.markdown("### 📝 Submit Your Feedback")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback", height=150)
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if name and feedback:
            st.success("✅ Feedback submitted successfully!")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.feedback_data.append({
                "Name": name,
                "Feedback": feedback,
                "Timestamp": timestamp
            })

            # Simulated log
            log_levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
            st.session_state.lambda_logs.insert(0, {
                "Time": timestamp,
                "Request ID": f"req-{random.randint(10000, 99999)}",
                "Execution Time (ms)": random.randint(150, 1000),
                "Memory Used (MB)": random.choice([128, 256, 512]),
                "IAM Role": random.choice(selected_roles if selected_roles else ["lambda-basic-execution"]),
                "Log Level": random.choice(log_levels)
            })
        else:
            st.error("❌ Please fill out all fields before submitting.")

# -------------------------------
# Display Feedback
# -------------------------------
if st.session_state.feedback_data:
    st.markdown("### 💬 Submitted Feedback")
    feedback_df = pd.DataFrame(st.session_state.feedback_data)
    st.dataframe(feedback_df, use_container_width=True)
else:
    st.info("No feedback submitted yet.")

# -------------------------------
# Simulated Logs Table
# -------------------------------
if st.session_state.lambda_logs:
    st.markdown("### 🪵 Lambda Function Logs")
    logs_df = pd.DataFrame(st.session_state.lambda_logs)
    st.dataframe(logs_df, use_container_width=True)
else:
    st.info("No invocation logs yet.")

# -------------------------------
# Architecture Summary
# -------------------------------
st.markdown("### 🧠 Architecture Overview")
st.markdown("""
This demo simulates a basic **Serverless Web App Architecture**:

🔁 **Frontend**: A simple form where users submit feedback  
🚪 **API Gateway (Simulated)**: Form submission acts as API entry  
⚙️ **AWS Lambda (Simulated)**: Serverless function handles logic  
🧠 **IAM Roles**: Control access to resources like logs or storage  
📦 **DynamoDB (Simulated)**: Session stores feedback entries  
📜 **CloudWatch Logs**: Simulated request logs per invocation

---

This is a minimal, scalable setup to mimic how serverless feedback apps work in production.
""")
