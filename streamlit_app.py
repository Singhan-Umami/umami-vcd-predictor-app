import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuration
API_URL = "https://xrcvtc46eywluh4dj2adh5mzqq0vpruo.lambda-url.ap-southeast-2.on.aws/predict"

st.set_page_config(
    page_title="UMAMI VCD Predictor",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #FF2B2B;
        border-color: #FF2B2B;
    }
    h1 {
        color: #FAFAFA;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #E0E0E0;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #404040;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Advanced Settings
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=80)
    st.title("Model Configuration")
    st.markdown("Adjust advanced model parameters here.")
    
    with st.expander("🧪 Advanced Model Params", expanded=False):
        g_vcd = st.number_input("Gompertz VCD", value=4.8)
        g_vmax = st.number_input("Gompertz Vmax", value=7.5)
        g_mu = st.number_input("Gompertz mu_max", value=0.55)
        g_lag = st.number_input("Gompertz lag", value=5.0)
        g_k = st.number_input("Gompertz k_decline", value=0.01)
        g_peak = st.number_input("Gompertz t_peak", value=40.0)
        exp_frac = st.number_input("Exp Frac", value=0.90)
        
        st.markdown("---")
        f_sin1 = st.number_input("Fourier Sin K1", value=0.5)
        f_cos1 = st.number_input("Fourier Cos K1", value=0.3)
        f_sin2 = st.number_input("Fourier Sin K2", value=0.25)
        f_cos2 = st.number_input("Fourier Cos K2", value=0.15)
        f_sin3 = st.number_input("Fourier Sin K3", value=0.12)
        f_cos3 = st.number_input("Fourier Cos K3", value=0.07)

# Main Content
st.title("🧬 UMAMI VCD Predictor")
st.markdown("### AI-Powered Bioprocess Forecasting")
st.markdown("Enter your experiment parameters to generate real-time VCD predictions and growth forecasts.")

# Input Form
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🧪 Media Components")
        fbs = st.slider("FBS (%)", 0.0, 20.0, 12.0)
        ps = st.number_input("P/S (%)", value=1.0)
        cell_boost_5 = st.number_input("Cell Boost 5 (%)", value=3.0)
        cell_boost_6 = st.number_input("Cell Boost 6 (%)", value=2.5)
        yeast_extract = st.number_input("Yeast Extract (%)", value=1.2)
        
    with col2:
        st.subheader("⚙️ Process Params")
        ph = st.slider("pH Setpoint", 6.0, 8.0, 7.1, 0.1)
        temp = st.number_input("Temperature (°C)", value=37.0)
        agitation = st.slider("Agitation (RPM)", 0, 300, 140)
        do = st.slider("DO (%)", 0, 100, 55)
        working_vol = st.number_input("Working Vol (ml)", value=1800.0)

    with col3:
        st.subheader("📊 Culture Status")
        total_cell_density = st.number_input("Total Cell Density", value=4.2)
        viability = st.slider("Viability (%)", 0.0, 100.0, 97.5)
        culture_day = st.number_input("Culture Day", value=3)
        lag1 = st.number_input("VCD Lag 1", value=3.9)
        lag2 = st.number_input("VCD Lag 2", value=3.5)
        lag3 = st.number_input("VCD Lag 3", value=3.0)

    # Hidden/Default inputs (to keep UI clean, but needed for API)
    # We use default values for these less common inputs
    insulin = 2.0
    transferrin = 2.0
    sodium_selenite = 2.0
    sodium_bicarbonate = 3.0
    its = 2.0
    bfgf = 40.0
    ascorbic_acid = 2.0
    lipid_mix = 2.0
    factor1 = 3.0
    factor2 = 2.5
    factor3 = 1.2
    feed = 0
    media_changed = 0
    harvest = 0
    cycle = 1
    scale_up = 2000.0
    cell_diameter = 17.0
    biomass = 0.52
    doubling_time = 16.0
    air = 1.2
    o2 = 0.55
    co2 = 0.28
    media_vol = 1800.0

    st.markdown("---")
    submitted = st.form_submit_button("🚀 Run Prediction Model")

if submitted:
    # Construct Payload
    payload = {
        "input": {
            "Experiment_ID": "Streamlit_User",
            "FBS (%)": fbs,
            "P/S(%)": ps,
            "Cell Boost 5 (%)": cell_boost_5,
            "Cell Boost 6 (%)": cell_boost_6,
            "Yeast Extract (%)": yeast_extract,
            "Insulin (X)": insulin,
            "Transferrin (X)": transferrin,
            "Sodium Selenite (X)": sodium_selenite,
            "Sodium Bicarbonate(%)": sodium_bicarbonate,
            "ITS": its,
            "bFGF (ng/ml)": bfgf,
            "Ascorbic acid (X)": ascorbic_acid,
            "Lipid mix (X)": lipid_mix,
            "Factor 1 as feed 1: Cell Boost 5 /%": factor1,
            "Factor 2 as feed 2: Cell Boost 6 /%": factor2,
            "Factor 3 as feed 3: Yeast Extract /%": factor3,
            "Feed": feed,
            "Media Changed": media_changed,
            "Total Cell density (million cells/ml) at the respective day": total_cell_density,
            "% Viability": viability,
            "Cell diameter (µm)": cell_diameter,
            "Cell Biomass (g/L)": biomass,
            "Culture Day": culture_day,
            "Culture Hours": culture_day * 24,
            "scale_up_size(ml)": scale_up,
            "Harvest": harvest,
            "Cycle": cycle,
            "pH setpoint": ph,
            "Temperature setpoint(°C)": temp,
            "Agitation speed(RPM)": agitation,
            "DO (%)": do,
            "Working Volume(ml)": working_vol,
            "Doubling time(hrs.)": doubling_time,
            "Air(sl/hr)": air,
            "O2(sl/hr)": o2,
            "CO2(sl/hr)": co2,
            "Media volume(ml)": media_vol,
            "Gompertz_VCD": g_vcd,
            "Gompertz_Vmax": g_vmax,
            "Gompertz_mu_max": g_mu,
            "Gompertz_lag": g_lag,
            "Gompertz_k_decline": g_k,
            "Gompertz_t_peak": g_peak,
            "exp_frac": exp_frac,
            "fourier_sin_k1": f_sin1,
            "fourier_cos_k1": f_cos1,
            "fourier_sin_k2": f_sin2,
            "fourier_cos_k2": f_cos2,
            "fourier_sin_k3": f_sin3,
            "fourier_cos_k3": f_cos3,
            "Viable cell density (million cells/ml) at the respective day_lag1": lag1,
            "Viable cell density (million cells/ml) at the respective day_lag2": lag2,
            "Viable cell density (million cells/ml) at the respective day_lag3": lag3
        }
    }

    with st.spinner("🤖 Analyzing Bio-Process Parameters..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                
                # --- RESULTS SECTION ---
                st.markdown("## 📊 Prediction Results")
                
                # 1. Key Metrics Row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown('<div class="metric-card"><h3>Today\'s VCD</h3><h1 style="color: #4CAF50;">{:.4f}</h1><p>Million cells/ml</p></div>'.format(result.get('today_vcd', 0)), unsafe_allow_html=True)
                with m2:
                    st.markdown('<div class="metric-card"><h3>Day 1 Forecast</h3><h1 style="color: #2196F3;">{:.4f}</h1><p>Million cells/ml</p></div>'.format(result.get('forecast', {}).get('day1', 0)), unsafe_allow_html=True)
                with m3:
                    st.markdown('<div class="metric-card"><h3>Growth Rate</h3><h1 style="color: #FF9800;">{:.2f}%</h1><p>Day 1</p></div>'.format(result.get('growth_rate_percent', {}).get('day1', 0)), unsafe_allow_html=True)

                st.markdown("---")

                # 2. Charts Row
                c1, c2 = st.columns(2)
                
                # Prepare Data for Charts
                days = ["Today", "Day +1", "Day +2"]
                vcd_values = [
                    result.get('today_vcd', 0),
                    result.get('forecast', {}).get('day1', 0),
                    result.get('forecast', {}).get('day2', 0)
                ]
                growth_values = [
                    0, # Today baseline
                    result.get('growth_rate_percent', {}).get('day1', 0),
                    result.get('growth_rate_percent', {}).get('day2', 0)
                ]

                with c1:
                    fig_vcd = go.Figure()
                    fig_vcd.add_trace(go.Scatter(x=days, y=vcd_values, mode='lines+markers+text', 
                                                 text=[f"{v:.2f}" for v in vcd_values], textposition="top center",
                                                 line=dict(color='#4CAF50', width=4), marker=dict(size=10)))
                    fig_vcd.update_layout(title="📈 VCD Forecast Trend", template="plotly_dark", yaxis_title="VCD (M cells/ml)")
                    st.plotly_chart(fig_vcd, use_container_width=True)

                with c2:
                    fig_growth = px.bar(x=days[1:], y=growth_values[1:], 
                                        labels={'x': 'Day', 'y': 'Growth Rate (%)'},
                                        title="🚀 Growth Rate Projection", template="plotly_dark", color_discrete_sequence=['#FF9800'])
                    st.plotly_chart(fig_growth, use_container_width=True)

                # 3. JSON Expander
                with st.expander("🔍 View Raw API Response"):
                    st.json(result)

            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"⚠️ Connection Error: {e}")
