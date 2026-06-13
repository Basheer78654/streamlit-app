# 🔧 Industrial Asset Predictive Maintenance Agent

**PS39 – Predictive Maintenance of Industrial Machinery**
IBM SkillsBuild | Edunet Foundation | AICTE 2026

---

## 📌 Problem Statement

Develop a predictive maintenance model for a fleet of industrial machines to anticipate failures before they occur. The model analyzes real-time sensor data and classifies the type of failure (Tool Wear, Heat Dissipation, Power Failure, Overstrain, Random Failures, or No Failure), enabling proactive maintenance and reducing downtime.

---

## 🚀 Live Demo

- **Streamlit Web App:** https://app-app-86cuhmm55zzarihythmpxo.streamlit.app/
- **GitHub Repo:** https://github.com/Basheer78654/streamlit-app

---

## 🛠️ Tech Stack

- **IBM watsonx.ai Studio** – Model training and deployment
- **AutoAI** – Automated pipeline generation (9 pipelines, best: Snap Random Forest Classifier)
- **IBM Cloud Object Storage** – Dataset hosting
- **IBM Granite** – LLM-based agent reasoning (Langflow)
- **Streamlit** – Interactive web application
- **Python (scikit-learn, pandas, requests)** – Data processing & API calls

---

## 📊 Dataset

- **Source:** [Kaggle – Machine Predictive Maintenance Classification](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)
- **Records:** 10,000 sensor readings
- **Features:** Type, Air temperature [K], Process temperature [K], Rotational speed [rpm], Torque [Nm], Tool wear [min]
- **Target:** Failure Type (6 classes — No Failure, Heat Dissipation Failure, Power Failure, Overstrain Failure, Tool Wear Failure, Random Failures)

---

## 🧠 Approach

1. **Data Preprocessing** – Label encoding for categorical fields, feature scaling
2. **AutoAI Experiment** – IBM watsonx.ai AutoAI generated and ranked 9 ML pipelines
3. **Best Model** – Snap Random Forest Classifier (Accuracy: 0.755, F1: 0.817)
4. **Deployment** – Online REST API endpoint on IBM watsonx.ai
5. **Rule-Based Override** – Domain-knowledge rules (temperature differential, power output, tool wear limits, torque thresholds) correct ML bias caused by class imbalance
6. **Web App** – Streamlit dashboard for real-time inference and diagnostic reporting

---

## 📁 Repository Contents

```
├── predictive_maintenance_app.py   # Streamlit application
├── requirements.txt                 # Python dependencies
├── predictive_maintenance.csv       # Dataset
└── README.md                        # This file
```

---

## ⚙️ Running Locally

```bash
pip install -r requirements.txt
streamlit run predictive_maintenance_app.py
```

---

## 🔍 How It Works

1. User enters live machine sensor readings (Type, temperatures, speed, torque, tool wear)
2. App authenticates with IBM IAM and sends data to the deployed watsonx.ai model
3. ML model returns a prediction + probability distribution across all 6 failure classes
4. A rule-based engine cross-checks the result against known failure thresholds
5. Final verdict is displayed with priority level and step-by-step mitigation actions

---

## 📈 Results

- AutoAI generated 9 pipelines; Snap Random Forest Classifier ranked #1
- Model deployed as a live, publicly accessible REST endpoint
- Rule-based override improves detection of minority failure classes affected by dataset imbalance (96.5% No Failure vs 3.5% failures)

---

## 🔮 Future Scope

- Apply SMOTE for balanced minority-class training
- Direct IoT sensor integration (MQTT / PLC)
- Expand to additional machine types (CNC, hydraulic presses)
- Automated maintenance ticketing integration with ERP systems

---

## 👤 Author

**Mohammad Basheer Shabbir Shareef**
Nawab Shah Alam Khan College of Engineering and Technology
WhatsApp: +91 7981841214
