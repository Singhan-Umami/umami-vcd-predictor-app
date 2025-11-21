import streamlit as st
import requests
import json

# Configuration
API_URL = "https://xrcvtc46eywluh4dj2adh5mzqq0vpruo.lambda-url.ap-southeast-2.on.aws/predict"

st.set_page_config(page_title="UMAMI VCD Predictor", layout="wide")

st.title("🧪 UMAMI VCD Predictor")
st.markdown("Enter the experiment parameters below to predict VCD and growth rates.")

# Create tabs for different categories of inputs
tab1, tab2, tab3, tab4 = st.tabs(["Media Components", "Process Parameters", "Culture Status", "Model Parameters"])

with tab1:
    st.header("Media & Supplements")
    col1, col2, col3 = st.columns(3)
    with col1:
        fbs = st.number_input("FBS (%)", value=12.0)
        ps = st.number_input("P/S (%)", value=1.0)
        cell_boost_5 = st.number_input("Cell Boost 5 (%)", value=3.0)
        cell_boost_6 = st.number_input("Cell Boost 6 (%)", value=2.5)
        yeast_extract = st.number_input("Yeast Extract (%)", value=1.2)
    with col2:
        insulin = st.number_input("Insulin (X)", value=2.0)
        transferrin = st.number_input("Transferrin (X)", value=2.0)
        sodium_selenite = st.number_input("Sodium Selenite (X)", value=2.0)
        sodium_bicarbonate = st.number_input("Sodium Bicarbonate (%)", value=3.0)
        its = st.number_input("ITS", value=2.0)
    with col3:
        bfgf = st.number_input("bFGF (ng/ml)", value=40.0)
        ascorbic_acid = st.number_input("Ascorbic acid (X)", value=2.0)
        lipid_mix = st.number_input("Lipid mix (X)", value=2.0)
        
    st.subheader("Feed Factors")
    c1, c2, c3 = st.columns(3)
    with c1:
        factor1 = st.number_input("Factor 1 (Cell Boost 5)", value=3.0)
    with c2:
        factor2 = st.number_input("Factor 2 (Cell Boost 6)", value=2.5)
    with c3:
        factor3 = st.number_input("Factor 3 (Yeast Extract)", value=1.2)

with tab2:
    st.header("Process Conditions")
    col1, col2 = st.columns(2)
    with col1:
        ph = st.number_input("pH Setpoint", value=7.1)
        temp = st.number_input("Temperature (°C)", value=37.0)
        agitation = st.number_input("Agitation Speed (RPM)", value=140.0)
        do = st.number_input("DO (%)", value=55.0)
    with col2:
        working_vol = st.number_input("Working Volume (ml)", value=1800.0)
        media_vol = st.number_input("Media Volume (ml)", value=1800.0)
        air = st.number_input("Air (sl/hr)", value=1.2)
        o2 = st.number_input("O2 (sl/hr)", value=0.55)
        co2 = st.number_input("CO2 (sl/hr)", value=0.28)

    st.subheader("Operations")
    c1, c2, c3 = st.columns(3)
    with c1:
        feed = st.number_input("Feed", value=0)
    with c2:
        media_changed = st.number_input("Media Changed", value=0)
    with c3:
        harvest = st.number_input("Harvest", value=0)

with tab3:
    st.header("Current Culture Status")
    col1, col2 = st.columns(2)
    with col1:
        culture_day = st.number_input("Culture Day", value=3)
        culture_hours = st.number_input("Culture Hours", value=72)
        cycle = st.number_input("Cycle", value=1)
        scale_up = st.number_input("Scale Up Size (ml)", value=2000.0)
    with col2:
        total_cell_density = st.number_input("Total Cell Density (M cells/ml)", value=4.2)
        viability = st.number_input("% Viability", value=97.5)
        cell_diameter = st.number_input("Cell Diameter (µm)", value=17.0)
        biomass = st.number_input("Cell Biomass (g/L)", value=0.52)
        doubling_time = st.number_input("Doubling Time (hrs)", value=16.0)

    st.subheader("Historical VCD (Lags)")
    c1, c2, c3 = st.columns(3)
    with c1:
        lag1 = st.number_input("VCD Lag 1", value=3.9)
    with c2:
        lag2 = st.number_input("VCD Lag 2", value=3.5)
    with c3:
        lag3 = st.number_input("VCD Lag 3", value=3.0)

with tab4:
    st.header("Advanced Parameters")
    st.info("These are internal model parameters (Gompertz & Fourier).")
    col1, col2 = st.columns(2)
    with col1:
        g_vcd = st.number_input("Gompertz VCD", value=4.8)
        g_vmax = st.number_input("Gompertz Vmax", value=7.5)
        g_mu = st.number_input("Gompertz mu_max", value=0.55)
        g_lag = st.number_input("Gompertz lag", value=5.0)
        g_k = st.number_input("Gompertz k_decline", value=0.01)
        g_peak = st.number_input("Gompertz t_peak", value=40.0)
        exp_frac = st.number_input("Exp Frac", value=0.90)
    with col2:
        f_sin1 = st.number_input("Fourier Sin K1", value=0.5)
        f_cos1 = st.number_input("Fourier Cos K1", value=0.3)
        f_sin2 = st.number_input("Fourier Sin K2", value=0.25)
        f_cos2 = st.number_input("Fourier Cos K2", value=0.15)
        f_sin3 = st.number_input("Fourier Sin K3", value=0.12)
        f_cos3 = st.number_input("Fourier Cos K3", value=0.07)

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
        "Culture Hours": culture_hours,
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

st.markdown("---")
if st.button("🚀 Predict VCD", type="primary", use_container_width=True):
    with st.spinner("Calling AWS Lambda Model..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                
                st.success("Prediction Successful!")
                
                # --- Improved Result Display ---
                
                # 1. Key Metrics
                st.markdown("### 📊 Results")
                col1, col2, col3, col4 = st.columns(4)
                
                today_vcd = result.get('today_vcd', 0)
                day1_vcd = result.get('forecast', {}).get('day1', 0)
                day2_vcd = result.get('forecast', {}).get('day2', 0)
                day1_growth = result.get('growth_rate_percent', {}).get('day1', 0)
                
                col1.metric("Today's VCD", f"{today_vcd:.4f}", "M cells/ml")
                col2.metric("Day 1 Forecast", f"{day1_vcd:.4f}", f"{day1_vcd - today_vcd:.4f}")
                col3.metric("Day 2 Forecast", f"{day2_vcd:.4f}", f"{day2_vcd - day1_vcd:.4f}")
                col4.metric("Growth Rate (D1)", f"{day1_growth:.2f}%")

                st.markdown("---")

                # 2. Visualizations
                import plotly.graph_objects as go
                
                # Prepare Data
                days = ["Today", "Day +1", "Day +2"]
                vcd_values = [
                    today_vcd,
                    result.get('forecast', {}).get('day1', 0),
                    result.get('forecast', {}).get('day2', 0)
                ]
                
                # Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=days, y=vcd_values, mode='lines+markers+text',
                                         text=[f"{v:.2f}" for v in vcd_values], textposition="top center",
                                         line=dict(color='#00CC96', width=3),
                                         marker=dict(size=10)))
                fig.update_layout(title="VCD Forecast Trend", yaxis_title="VCD (M cells/ml)", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                # 3. Raw Data (Hidden)
                with st.expander("View Raw JSON Response"):
                    st.json(result)

            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
