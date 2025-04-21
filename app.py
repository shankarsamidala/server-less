import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Set page config
st.set_page_config(page_title="📬 Serverless Feedback App", layout="wide")

# Initialize session state
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []
if "lambda_logs" not in st.session_state:
    st.session_state.lambda_logs = []

# Title and subtitle
st.title("📬 Serverless Feedback Collector")
st.caption("Simulating a serverless web app with Lambda logs, IAM roles, and feedback storage")

# -------------------------------
# IAM Roles (simulated)
# -------------------------------
st.sidebar.header("🔐 IAM Role Configuration")
iam_roles = ["lambda-basic-execution", "cloudwatch-logs", "dynamodb-access", "s3-readonly"]
selected_roles = st.sidebar.multiselect("Attach IAM Roles", iam_roles, default=iam_roles[:2])

# -------------------------------
# Feedback Form
# -------------------------------
st.markdown("### 📝 Submit Feedback")
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

            # Simulated Lambda log
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
    df = pd.DataFrame(st.session_state.feedback_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No feedback submitted yet.")

# -------------------------------
# Display Simulated Lambda Logs
# -------------------------------
if st.session_state.lambda_logs:
    st.markdown("### 🪵 Lambda Invocation Logs")
    logs_df = pd.DataFrame(st.session_state.lambda_logs)
    st.dataframe(logs_df, use_container_width=True)
else:
    st.info("No invocation logs yet.")

# -------------------------------
# Explanation
# -------------------------------
st.markdown("### 🧠 Serverless Architecture Explanation")
st.info("""
- 🧾 Form acts as **API Gateway**
- ⚙️ Button press simulates **Lambda execution**
- 🗃️ Feedback is stored like a **DynamoDB table**
- 🔐 IAM roles simulate secure access
- 🪵 Logs mimic **CloudWatch logs**
""")
