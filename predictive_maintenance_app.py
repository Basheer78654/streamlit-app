import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="Industrial Predictive Maintenance",
    layout="wide",
    page_icon="🔧"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a1a2e, #16213e, #0f3460);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .healthy {
        background: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .failure {
        background: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔧 Industrial Asset Predictive Maintenance Agent</h1>
    <h3>Powered by IBM watsonx.ai AutoAI & IBM Granite Framework</h3>
    <p>PS39 - Mechanical Engineering | IBM SkillsBuild | Edunet Foundation</p>
</div>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.header("⚙️ Machine Sensor Input Panel")
st.sidebar.markdown("---")

machine_type_label = st.sidebar.selectbox(
    "🏭 Machine Grade (Type)",
    options=["L", "M", "H"],
    help="L=Low, M=Medium, H=High quality variants"
)

st.sidebar.markdown("### 🌡️ Temperature Parameters")
air_temp = st.sidebar.number_input(
    "Air Temperature [K]",
    min_value=290.0,
    max_value=330.0,
    value=298.1,
    step=0.1,
    help="Normal range: 295K - 305K"
)

process_temp = st.sidebar.number_input(
    "Process Temperature [K]",
    min_value=290.0,
    max_value=340.0,
    value=308.6,
    step=0.1,
    help="Normal range: 305K - 315K"
)

st.sidebar.markdown("### ⚡ Mechanical Parameters")
rotational_speed = st.sidebar.number_input(
    "Rotational Speed [rpm]",
    min_value=500,
    max_value=3000,
    value=1551,
    step=1,
    help="Normal range: 1200 - 2000 rpm"
)

torque = st.sidebar.number_input(
    "Torque [Nm]",
    min_value=0.0,
    max_value=100.0,
    value=42.8,
    step=0.1,
    help="Normal range: 20 - 60 Nm"
)

tool_wear = st.sidebar.number_input(
    "Tool Wear Time [min]",
    min_value=0,
    max_value=300,
    value=0,
    step=1,
    help="Normal range: 0 - 200 min"
)

# ----------------- LIVE SENSOR DASHBOARD -----------------
st.subheader("📊 Live Sensor Dashboard")

col1, col2, col3, col4, col5, col6 = st.columns(6)

temp_diff = round(process_temp - air_temp, 1)
power_watts = round(rotational_speed * torque * (2 * 3.14159 / 60), 1)

with col1:
    st.metric("Machine Type", machine_type_label)
with col2:
    delta_air = "⚠️ HIGH" if air_temp > 308 else "✅ OK"
    st.metric("Air Temp", f"{air_temp} K", delta_air)
with col3:
    delta_proc = "⚠️ HIGH" if process_temp > 313 else "✅ OK"
    st.metric("Process Temp", f"{process_temp} K", delta_proc)
with col4:
    delta_speed = "⚠️ HIGH" if rotational_speed > 2000 else "✅ OK"
    st.metric("Speed", f"{rotational_speed} rpm", delta_speed)
with col5:
    delta_torque = "⚠️ HIGH" if torque > 60 else "✅ OK"
    st.metric("Torque", f"{torque} Nm", delta_torque)
with col6:
    delta_wear = "⚠️ HIGH" if tool_wear > 200 else "✅ OK"
    st.metric("Tool Wear", f"{tool_wear} min", delta_wear)

# Derived metrics
st.markdown("---")
col7, col8, col9 = st.columns(3)
with col7:
    if temp_diff < 0:
        st.metric("Temp Difference", f"{temp_diff} K", "🚨 ABNORMAL - Air > Process!")
    elif temp_diff < 8.6:
        st.metric("Temp Difference", f"{temp_diff} K", "⚠️ LOW - Risk Zone")
    else:
        st.metric("Temp Difference", f"{temp_diff} K", "✅ Normal")
with col8:
    if power_watts > 9000:
        st.metric("Power Output", f"{power_watts} W", "🚨 CRITICAL OVERLOAD")
    elif power_watts > 7000:
        st.metric("Power Output", f"{power_watts} W", "⚠️ HIGH - Monitor")
    else:
        st.metric("Power Output", f"{power_watts} W", "✅ Normal")
with col9:
    wear_limit = {"L": 200, "M": 220, "H": 240}
    limit = wear_limit[machine_type_label]
    if tool_wear > limit:
        st.metric("Wear Status", f"{tool_wear}/{limit} min", "🚨 LIMIT EXCEEDED")
    else:
        st.metric("Wear Status", f"{tool_wear}/{limit} min", "✅ Within Limit")

st.markdown("---")

# ----------------- RULE-BASED FAILURE DETECTION -----------------
def check_rule_based_failure(air_temp, process_temp, rotational_speed, torque, tool_wear, machine_type_label):
    temp_diff = process_temp - air_temp
    power = rotational_speed * torque * (2 * 3.14159 / 60)
    wear_limits = {"L": 200, "M": 220, "H": 240}

    # Abnormal: Air temp higher than process temp
    if temp_diff < 0:
        return "Heat Dissipation Failure", "Air temperature exceeds process temperature — severe thermal anomaly detected."

    # Heat Dissipation Failure
    if temp_diff < 8.6 and rotational_speed < 1380:
        return "Heat Dissipation Failure", "Temperature differential too small under low-speed operations."

    # Power Failure
    if power > 9000:
        return "Power Failure", f"Power output {round(power)}W exceeds safe limit of 9000W."

    # Tool Wear Failure
    if tool_wear > wear_limits[machine_type_label]:
        return "Tool Wear Failure", f"Tool wear {tool_wear} min exceeds {machine_type_label}-grade limit of {wear_limits[machine_type_label]} min."

    # Overstrain Failure
    if torque > 60 and tool_wear > 180:
        return "Overstrain Failure", "High torque combined with excessive tool wear indicates mechanical overstrain."

    # Extreme temperature
    if air_temp > 315 or process_temp > 320:
        return "Heat Dissipation Failure", "Operating temperatures critically exceeded safe thermal limits."

    return None, None

# ----------------- RUN DIAGNOSIS BUTTON -----------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_button = st.button("🚀 Run Anomaly Diagnosis Engine", use_container_width=True)

if run_button:
    with st.spinner("🔄 Authenticating with IBM IAM and running inference..."):
        try:
            # 1. Get IAM Token
            API_KEY = st.secrets["IBM_API_KEY"]
            token_url = 'https://iam.cloud.ibm.com/identity/token'
            token_data = {
                "apikey": API_KEY,
                "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            }
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            mltoken = token_response.json()["access_token"]

            # Type mapping
            type_mapping = {"L": 0, "M": 1, "H": 2}
            machine_type_numeric = type_mapping[machine_type_label]

            # 2. Build payload
            payload_scoring = {
                "input_data": [{
                    "fields": [
                        "UDI", "Product ID", "Type",
                        "Air temperature [K]", "Process temperature [K]",
                        "Rotational speed [rpm]", "Torque [Nm]",
                        "Tool wear [min]", "Target"
                    ],
                    "values": [[
                        1, "c_1", machine_type_numeric,
                        float(air_temp), float(process_temp),
                        int(rotational_speed), float(torque),
                        int(tool_wear), 0
                    ]]
                }]
            }

            # 3. Call deployment
            scoring_url = 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/019e9688-5608-769b-ba9c-90063c7bced3/predictions?version=2021-05-01'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {mltoken}'
            }
            response_scoring = requests.post(scoring_url, json=payload_scoring, headers=headers)

            if response_scoring.status_code != 200:
                st.error(f"IBM API Error: {response_scoring.status_code}")
                st.json(response_scoring.json())
            else:
                result = response_scoring.json()
                ml_prediction = str(result['predictions'][0]['values'][0][0]).strip()
                probabilities = result['predictions'][0]['values'][0][1]
                ml_confidence = round(max(probabilities) * 100, 2)

                # 4. Rule-based override
                rule_prediction, rule_reason = check_rule_based_failure(
                    air_temp, process_temp, rotational_speed,
                    torque, tool_wear, machine_type_label
                )

                if rule_prediction:
                    final_prediction = rule_prediction
                    detection_method = "🔬 Rule-Based Override"
                    detection_reason = rule_reason
                else:
                    final_prediction = ml_prediction
                    detection_method = "🤖 ML Model (AutoAI Random Forest)"
                    detection_reason = f"Model confidence: {ml_confidence}%"

                # ----------------- RESULTS DISPLAY -----------------
                st.subheader("🎯 Diagnostic Report Verdict")

                # Detection info
                st.info(f"**Detection Method:** {detection_method} | **Reason:** {detection_reason}")

                if final_prediction == "No Failure":
                    st.markdown(f"""
                    <div class="healthy">
                        <h2>🟢 SYSTEM HEALTHY</h2>
                        <p>Machine is operating within all nominal parameters.</p>
                        <p><b>ML Confidence:</b> {ml_confidence}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    # Priority mapping
                    priority_map = {
                        "Tool Wear Failure": ("🔴 HIGH", "Immediate shutdown required"),
                        "Heat Dissipation Failure": ("🔴 HIGH", "Immediate cooling action required"),
                        "Power Failure": ("🟡 MEDIUM", "Schedule urgent maintenance"),
                        "Overstrain Failure": ("🔴 HIGH", "Reduce load immediately"),
                        "Random Failures": ("🟡 MEDIUM", "Manual inspection needed")
                    }
                    priority, action = priority_map.get(final_prediction, ("🟡 MEDIUM", "Inspect machine"))

                    st.markdown(f"""
                    <div class="failure">
                        <h2>🚨 ANOMALY DETECTED</h2>
                        <h3>Failure Type: {final_prediction}</h3>
                        <p><b>Priority:</b> {priority}</p>
                        <p><b>Immediate Action:</b> {action}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Mitigation steps
                    st.markdown("### ⚠️ Step-by-Step Mitigation Protocol:")
                    mitigation = {
                        "Tool Wear Failure": [
                            "🛑 Step 1: Immediately halt production spindle operation",
                            "🔧 Step 2: Replace tool insert bit with new cutting element",
                            "📋 Step 3: Run calibration cycle before resuming",
                            "📝 Step 4: Log replacement in maintenance system"
                        ],
                        "Heat Dissipation Failure": [
                            "🛑 Step 1: Reduce cyclic load by minimum 20%",
                            "🌡️ Step 2: Check thermal lubrication fluid levels",
                            "💧 Step 3: Flush and replace coolant configuration",
                            "🔍 Step 4: Inspect cooling fans and heat exchangers"
                        ],
                        "Power Failure": [
                            "⚡ Step 1: Check incoming electrical voltage lines",
                            "📊 Step 2: Inspect current draw on control panel",
                            "🔧 Step 3: Verify motor drive parameters",
                            "📞 Step 4: Contact electrical maintenance team"
                        ],
                        "Overstrain Failure": [
                            "🛑 Step 1: Reduce torque load immediately",
                            "⚙️ Step 2: Recalibrate operational rotational speed",
                            "🔍 Step 3: Inspect mechanical joints and bearings",
                            "📋 Step 4: Schedule full mechanical inspection within 24hrs"
                        ]
                    }

                    steps = mitigation.get(final_prediction, ["👉 Request manual field technician inspection"])
                    for step in steps:
                        st.write(step)

                # Probability chart
                st.markdown("### 📊 Failure Probability Distribution")
                failure_labels = [
                    "Heat Dissipation",
                    "No Failure",
                    "Overstrain",
                    "Power Failure",
                    "Tool Wear",
                    "Random Failure"
                ]
                prob_dict = {
                    failure_labels[i]: round(abs(probabilities[i]) * 100, 4)
                    for i in range(len(probabilities))
                }
                st.bar_chart(prob_dict)

                # Debug JSON
                with st.expander("🔧 Debug: Raw API JSON Response"):
                    st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("❌ Network Error: Cannot reach IBM Cloud. Check internet connection.")
        except KeyError as e:
            st.error(f"❌ Missing field in response: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:gray;">
    <b>IBM SkillsBuild University Engagement | Edunet Foundation | AICTE 2026</b><br>
    PS39 - Predictive Maintenance of Industrial Machinery<br>
    Built with IBM watsonx.ai AutoAI + IBM Granite + Langflow + Streamlit
</div>
""", unsafe_allow_html=True)