import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Serverless Architecture Simulator", layout="wide")
st.title("☁️ Serverless Architecture Design for Scalable Applications")
st.caption("🔄 Auto-scaling • Pay-per-use • Cloud-native Simulation")

# Sidebar Inputs
st.sidebar.header("🛠️ Simulation Controls")
invocations = st.sidebar.slider("Invocations per Hour", 100, 50000, 1000, step=500)
avg_duration = st.sidebar.slider("Execution Time per Request (ms)", 100, 3000, 500, step=100)
memory_allocated = st.sidebar.slider("Memory Allocated per Function (MB)", 128, 3008, 512, step=128)

# Cost Estimation (Simulated AWS Lambda Pricing)
invocation_cost_per_million = 0.20
compute_cost_per_gb_sec = 0.0000166667

gb_seconds = (memory_allocated / 1024) * (avg_duration / 1000) * invocations
compute_cost = gb_seconds * compute_cost_per_gb_sec
invocation_cost = (invocations / 1_000_000) * invocation_cost_per_million
total_cost = compute_cost + invocation_cost

# Simulated 24h Traffic Pattern
hours = np.arange(0, 24)
traffic_pattern = np.sin(np.pi * hours / 12)**2
scaled_invocations = invocations * traffic_pattern
latency_p50 = np.random.normal(loc=avg_duration, scale=50, size=24)
latency_p95 = latency_p50 + np.random.normal(loc=150, scale=20, size=24)
latency_p99 = latency_p95 + np.random.normal(loc=100, scale=15, size=24)
concurrency = (scaled_invocations * (avg_duration / 1000)) / 60

# 1. Load Chart
st.subheader("📊 Load Scaling Over 24 Hours")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(hours, scaled_invocations, label="Invocations", color="royalblue")
ax1.set_xlabel("Hour")
ax1.set_ylabel("Function Calls")
ax1.set_title("Invocation Pattern")
ax1.grid(True)
st.pyplot(fig1)

# 2. Latency Chart
st.subheader("📈 Latency Trends (p50, p95, p99)")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(hours, latency_p50, label="p50", color="green")
ax2.plot(hours, latency_p95, label="p95", color="orange")
ax2.plot(hours, latency_p99, label="p99", color="red")
ax2.set_xlabel("Hour")
ax2.set_ylabel("Latency (ms)")
ax2.set_title("Simulated Latency Percentiles")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# 3. Cost Breakdown
st.subheader("💵 Cost Distribution")
service_labels = ['Compute (Lambda)', 'Invocation Cost', 'Logging & Monitoring', 'Storage']
service_costs = [compute_cost, invocation_cost, 0.02 * total_cost, 0.05 * total_cost]
fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.pie(service_costs, labels=service_labels, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)

# 4. Concurrency Heatmap
st.subheader("🔥 Concurrency Simulation")
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.bar(hours, concurrency, color="purple")
ax4.set_xlabel("Hour")
ax4.set_ylabel("Concurrent Executions")
ax4.set_title("Function Concurrency over Time")
ax4.grid(True)
st.pyplot(fig4)

# 5. Architecture Flow (visual layout in markdown)
st.subheader("🧭 Serverless Architecture Flow")
st.markdown("""
**Architecture Flow:**

""")

# IAM Users
st.subheader("🧑‍💻 IAM Users")
users_df = pd.DataFrame([
    {"User ID": "admin_user", "Role": "Admin", "Permissions": "FullAccess", "MFA Enabled": True},
    {"User ID": "devops_engineer", "Role": "DevOps", "Permissions": "Deploy, Monitor", "MFA Enabled": True},
    {"User ID": "api_gateway_user", "Role": "API Trigger", "Permissions": "Invoke", "MFA Enabled": False},
    {"User ID": "analyst_user", "Role": "Viewer", "Permissions": "ReadOnly", "MFA Enabled": True}
])
st.dataframe(users_df, use_container_width=True)

# Lambda Functions
st.subheader("🚀 Serverless Functions")
functions_df = pd.DataFrame([
    {"Function": "authHandler", "Region": "us-east-1", "Trigger": "API Gateway", "Last Modified": "2025-04-20"},
    {"Function": "paymentProcessor", "Region": "us-west-2", "Trigger": "Pub/Sub", "Last Modified": "2025-04-19"},
    {"Function": "dataIngestor", "Region": "asia-south1", "Trigger": "S3 Event", "Last Modified": "2025-04-18"},
    {"Function": "analyticsJob", "Region": "europe-west3", "Trigger": "Scheduler", "Last Modified": "2025-04-17"},
])
st.dataframe(functions_df, use_container_width=True)

# Public Endpoint
st.subheader("🔗 Public Endpoint")
st.code("https://api.scalableapps.dev/v1/auth", language="bash")

# Logs
st.subheader("📄 Simulated Logs")
with st.expander("Show Logs"):
    st.text("""
[14:01:55] authHandler invoked (cold start)
[14:02:01] authHandler returned 200 OK (342 ms)
[14:03:21] authHandler returned 401 Unauthorized (312 ms)
[14:04:05] paymentProcessor triggered by event (185 ms)
[14:04:06] paymentProcessor returned 200 OK
[14:05:40] dataIngestor triggered by upload
[14:05:41] dataIngestor returned 202 Accepted (499 ms)
    """)

# Summary Metrics
st.subheader("📊 Summary Metrics")
cold_starts = np.random.randint(1, 5)
errors = np.random.randint(0, 3)
concurrency_peak = int(concurrency.max())

col1, col2, col3 = st.columns(3)
col1.metric("Cold Starts", f"{cold_starts}x")
col2.metric("Errors (24h)", f"{errors}")
col3.metric("Peak Concurrency", f"{concurrency_peak} funcs/sec")
