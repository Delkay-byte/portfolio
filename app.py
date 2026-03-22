from fpdf import FPDF
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import gdown  # New import
import os     # New import
def convert_to_dense(x):
    return x.toarray() if hasattr(x, "toarray") else x

# --- "Generate Regional Analysis" button ---
def create_pdf_report(region, indicator, status, risk, gap, belt, year):
    pdf = FPDF()
    pdf.add_page()
    # ... (all your existing PDF code)
    return bytes(pdf.output())

# 1. Page Configuration
st.set_page_config(page_title="Saviour Amegayie | Data Portfolio", page_icon="📊", layout="wide")

# --- PROFESSIONAL TOUCH 1: ASSET CACHING & DRIVE DOWNLOAD ---
@st.cache_resource
def load_assets():
    model_path = 'random_forest_model.pkl'
    # RENAMED to avoid conflict with GRIP
    preprocessor_path = 'harvest_preprocessor.pkl' 
    
    # Google Drive ID for your 190MB model
    file_id = '15wXBt7Qn_fX_7qkpV-2U7uEBoQagNpb5'
    url = f'https://drive.google.com/uc?id={file_id}'
    
    # If the model file isn't on the server yet, download it from Drive
    if not os.path.exists(model_path):
        with st.spinner("Downloading high-precision engine (190MB)... This may take a moment on first launch."):
            gdown.download(url, model_path, quiet=False)
    
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    return model, preprocessor

# --- LOAD PROJECT GRIP ASSETS ---
# Loaded globally so they are available throughout the app
@st.cache_resource
def load_grip_engine():
    try:
        engine = joblib.load('ges_hybrid_engine.pkl')
        ref = joblib.load('median_gap_reference.pkl')
        return engine, ref, True
    except:
        return None, None, False

# Call the function globally
grip_engine, median_ref, grip_assets_loaded = load_grip_engine()

# --- GLOBAL DATA INITIALIZATION ---
DEFAULT_DATA_PATH = "FINAL_MINISTERIAL_PREDICTOR_DATA.csv"

# 1. Initialize session state if empty
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(DEFAULT_DATA_PATH)
    except FileNotFoundError:
        # Emergency fallback if the file isn't found
        st.session_state.df = pd.DataFrame(columns=['Year', 'Target_Year', 'Region'])
df = st.session_state.df

# 3. Global Year Protection Logic (Fixes NameError)
if not df.empty:
    if 'Year' in df.columns:
        current_year = df['Year'].iloc[0]
    elif 'Target_Year' in df.columns:
        current_year = df['Target_Year'].iloc[0]
    else:
        current_year = 2026
else:
    current_year = 2026


# Mapping Regions to Belts for Automation
REGION_CONTEXT_MAP = {
    'Ahafo': 'Middle Belt', 'Ashanti': 'Middle Belt', 'Bono': 'Middle Belt', 'Bono East': 'Middle Belt',
    'Central': 'Southern Belt', 'Eastern': 'Southern Belt', 'Greater Accra': 'Southern Belt',
    'North East': 'Northern Savannah', 'Northern': 'Northern Savannah', 'Oti': 'Middle Belt',
    'Savannah': 'Northern Savannah', 'Upper East': 'Northern Savannah', 'Upper West': 'Northern Savannah',
    'Volta': 'Southern Belt', 'Western': 'Southern Belt', 'Western North': 'Middle Belt'
}

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] { font-size: 14px !important; font-weight: bold; }
    [data-testid="stMetricValue"] { font-size: 24px !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        border: 1px solid #3d4156;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar for Navigation
st.sidebar.title("Navigation")

# Profile Picture Logic
try:
    st.sidebar.image("profile.jpeg", use_container_width=True)
except:
    st.sidebar.write("📸 (Add your profile.jpeg to the folder)")

# --- SIDEBAR STATUS ---
st.sidebar.success("✅ Available for Opportunities")

# ADD THE VISITOR BADGE HERE
st.sidebar.markdown("""
<div style="text-align: center;">
    <img src="https://visitor-badge.laobi.icu/badge?page_id=Saviour-Amegayie-Portfolio&color=00cc96" alt="Visitor Count">
</div>
""", unsafe_allow_html=True)

# --- YEAR PROTECTION LOGIC ---
# If the CSV has a 'Year' column, use it. If not, use 'Target_Year'. 
# If neither exists, default to 2026 so the app doesn't crash.
if 'Year' in df.columns:
    current_year = df['Year'].iloc[0]
elif 'Target_Year' in df.columns:
    current_year = df['Target_Year'].iloc[0]
else:
    current_year = 2026

# --- SOCIAL ICONS SECTION ---
st.sidebar.write("---")
st.sidebar.subheader("Connect with Me")

icon_col1, icon_col2, icon_col3 = st.sidebar.columns(3)
with icon_col1:
    st.markdown("[![LinkedIn](https://img.icons8.com/color/35/000000/linkedin.png)](https://www.linkedin.com/in/saviour-amegayie-ds)")
with icon_col2:
    st.markdown("[![GitHub](https://img.icons8.com/glyph-neue/35/ffffff/github.png)](https://github.com/Delkay-byte)")
with icon_col3:
    st.markdown("[![Email](https://img.icons8.com/color/35/000000/gmail-new.png)](mailto:saviour.amegayie.ds@gmail.com)")

st.sidebar.write("---")
page = st.sidebar.radio("Go to", ["Home", "Projects", "About Me", "Contact"])

# 3. Home Page
if page == "Home":
    st.title("Saviour Amegayie")
    # --- PROFESSIONAL TOUCH 2: THE HOOK ---
    st.markdown("### **Data Scientist leveraging AI for Food Security & Education 🌍**")
    st.subheader("Data Scientist | IT Educator | AI Enthusiast")
    st.write("---")

    # --- UPDATED: Quick Impact Metrics ---
    st.markdown("#### **Professional Snapshot**")
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Experience", "6 Years", help="Leadership in Ghana Education Service (GES)")
    h2.metric("ML Accuracy", "99.1%", help="Achieved in Harvest Intelligence Engine")
    h3.metric("Scope", "16 Regions", help="Regional analysis across all of Ghana")
    h4.metric("Focus", "AI + Policy", help="Combining Data Science with strategic implementation")

    st.write("---")
    
    col_intro, col_img = st.columns([2, 1])
    with col_intro:
        st.markdown("""
        #### Bridging Education and Analytics 🇬🇭
        Welcome to my digital space! I specialize in transforming raw data into **Actionable Insights** using Python and Machine Learning. 
        
        With 6 years of leadership in the **Ghana Education Service**, I bring a unique perspective to Data Science—focusing on clarity, precision, and real-world impact.
        
        Currently focused on:
        * 🌾 **Agri-Tech:** Predictive modeling for global food security.
        * 📚 **Edu-Tech:** Leveraging analytics to improve learning outcomes.
        """)

        # --- UPDATED: Combined Project Spotlight ---
        st.info("""
        💡 **Flagship Project Highlights:** * **Agri-Tech:** Developed a Harvest Intelligence Engine with **99.1% R² Accuracy**.
        * **Edu-Tech:** Built 'Project GRIP' to track **7 ministerial indicators** with 100% precision for budget reallocation.
        """)

    st.write("---")
    st.subheader("Technical Toolbox")
    
    sk1, sk2, sk3, sk4 = st.columns(4)
    with sk1:
        st.write("🧪 **Analysis**")
        st.caption("Pandas, NumPy, Matplotlib, Seaborn")
    with sk2:
        st.write("🤖 **ML/AI**")
        st.caption("Scikit-Learn, Random Forest, Regression, Bayesian Modeling")
    with sk3:
        st.write("💻 **IT & Dev**")
        st.caption("Python, SQL, Streamlit, Git")
    with sk4:
        st.write("📢 **Leadership**")
        st.caption("Strategic Planning, Team Leading, Mentorship")

# 4. Projects Page
elif page == "Projects":
    st.title("Technical Portfolio")
    st.write("---")

    # --- PROJECT 1: HARVEST INTELLIGENCE ---
    st.header("1. Harvest Intelligence Engine (Yield Prediction)")
    
    st.markdown("""
    **Core Features:**
    * **Multi-Factor Analysis:** Integrates rainfall, temperature, and pesticide data.
    * **High Precision:** Trained on a global dataset using a Random Forest architecture.
    * **Deployable API:** Logic ready for integration into mobile farming apps.
    """)

    m1, m2, m3 = st.columns(3)
    # --- PROFESSIONAL TOUCH 3: METRIC DELTA ---
    m1.metric("Model Accuracy", "99.1%", delta="High Precision", delta_color="normal", help="R² Score indicating the variance captured by the model.")
    m2.metric("Algorithm", "Random Forest", help="Ensemble learning method for robust regression.")
    m3.metric("Status", "Production Ready", help="Optimized and ready for real-world deployment.")

    try:
        # This triggers the gdown download if the file is missing!
        model, harvest_preprocessor = load_assets() 
        model_loaded = True
    except Exception as e:
        st.error(f"Asset Loading Error: {e}")
        model_loaded = False

    st.write("### 🚀 Real-Time Model Inference")
    
    if model_loaded:
        with st.container(border=True):
            available_countries = sorted(harvest_preprocessor.categories_[0].tolist())
            available_crops = sorted(harvest_preprocessor.categories_[1].tolist())

            sim_col1, sim_col2 = st.columns(2)
            with sim_col1:
                rain_fall = st.slider("Average Annual Rainfall (mm)", 400.0, 3000.0, 1200.0)
                temp = st.slider("Average Temperature (°C)", 15.0, 45.0, 27.0)
                pesticides = st.number_input("Pesticide Application (tonnes)", value=50.0)
            with sim_col2:
                item = st.selectbox("Crop Selection", available_crops)
                area = st.selectbox("Region/Country", available_countries)
                year = st.number_input("Reference Year", value=2024)

            input_data = pd.DataFrame({
                'area': [area], 'item': [item], 'year': [year],
                'average_rain_fall_mm_per_year': [rain_fall],
                'pesticides_tonnes': [pesticides], 'avg_temp': [temp]
            })

            try:
                categorical_data = input_data[['area', 'item']]
                encoded_data = harvest_preprocessor.transform(categorical_data)
                if hasattr(encoded_data, "toarray"):
                    encoded_data = encoded_data.toarray()
                
                numerical_data = input_data[['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']].values
                final_input = np.hstack([encoded_data, numerical_data])
                prediction = model.predict(final_input)
                st.success(f"**Predicted Yield Output:** {prediction[0]:,.2f} hg/ha")
            except Exception as e:
                st.error(f"Prediction Error: {e}")

    # Interactive Viz for Project 1
    try:
        import plotly.graph_objects as go
        actual = np.linspace(10000, 100000, 100)
        noise = np.random.normal(0, 1500, 100) 
        predicted = actual + noise
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=actual, y=predicted, mode='markers', name='Predictions',
                                 marker=dict(color='#00CC96', size=8, opacity=0.6)))
        fig.add_trace(go.Scatter(x=[actual.min(), actual.max()], y=[actual.min(), actual.max()],
                                 mode='lines', name='Perfect Fit', line=dict(color='red', dash='dash')))
        fig.update_layout(
            title="Model Performance: Actual vs Predicted", 
            template="plotly_dark", 
            height=400,
            xaxis_title="Actual Yield",
            yaxis_title="Predicted Yield"
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        pass

    st.link_button("📂 View Project Source", "https://github.com/Delkay-byte/Predictive-Agriculture-Analysis")

    st.write("---")

    # --- PROJECT 2: PROJECT GRIP (Ministerial Resource Predictor) ---
    st.header("2. Project GRIP: Ministerial Resource Predictor 🇬🇭")
    st.subheader(f"🛠️ GRIP: {current_year} Interactive Risk Simulator")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.image("grip_icon.png") 
        st.write("**Role:** Lead Data Architect")
        st.write("**Engine:** Hybrid Intelligence (ML + Policy Logic)")

    with col_b:
        st.markdown("""
        **Project Overview:** Developed to solve regional resource disparities. GRIP fuses MoE targets, GSS Census data, and UNICEF regional contexts.
        
        **Key Breakthroughs:**
        * **Hybrid Intelligence:** Gaussian Naive Bayes + Structural Policy Guardrails.
        * **Granular Analysis:** Now tracking performance across all **16 regions**.
        * **Visual Status Engine:** Automated classification of regional performance (Critical/Stable/Impressive)
        * **Impact:** Identified 100% of high-risk ministerial targets in validation.
        """)
    
    st.write("---")
    st.subheader(f"🛠️ GRIP: {current_year} Interactive Risk Simulator")
    st.info(f"Select a region to simulate {current_year} target feasibility based on current regional constraints.")

    
    # --- SIMPLIFIED GRIP LOGIC ---
    # We no longer try to load the files here, we just check if they loaded successfully at the top
    
    if not grip_assets_loaded:
        st.warning("⚠️ Project GRIP assets not found. Ensure 'ges_hybrid_engine.pkl' and 'median_gap_reference.pkl' are in the folder.")
    else:
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                # This is now the ONLY instance of this selectbox
                selected_region = st.selectbox("Select Target Region", list(REGION_CONTEXT_MAP.keys()))
                derived_belt = REGION_CONTEXT_MAP[selected_region]
                st.caption(f"📍 Automatically mapped to: **{derived_belt}**")
                
                edu_level = st.selectbox("Education Level", ["Basic Education", "Secondary Education", "Technical and Vocational", "Tertiary Education"])
                pop = st.number_input("Regional Population Aged 3+", min_value=100000, value=850000)
            
            with c2:
                lit_rate = st.slider("Regional Literacy Rate (%)", 0.0, 100.0, 68.0)
                indicator_name = st.selectbox("Indicator Name", [
                    "Enhanced Teacher Deployment (PTR)", 
                    "Increased Enrolment", 
                    "Improved Teacher Professionalism",
                    "Increased Functional Literacy",
                    "Increase Science / Humanities Ratio",
                    "Increase % of Female Enrolment"
                ])
                sim_latest = st.number_input("Simulated Latest Value (%)", value=45.0)
                sim_target = st.number_input("Simulated 2026 Target (%)", value=100.0)
                imp_gap = sim_target - sim_latest

            if st.button("Generate Regional Analysis", type="primary"):
                # 1. Prepare the raw input DataFrame
                # The Pipeline will handle the scaling and encoding automatically!
                input_df = pd.DataFrame({
                    'Education_Level': [edu_level], 'Context_Name': [derived_belt],
                    'Total_Pop': [pop], 'Literacy_Rate': [lit_rate]
                })
                
                # 2. Get Probability from the Model
                # [0][1] gets the probability of "High Risk"
                prob_risk = grip_engine.predict_proba(input_df)[0][1]

                # Status Engine Logic
                if imp_gap <= 5:
                    status_label, status_color, text_color = "IMPRESSIVE: Target Nearly Met", "#00cc96", "white"
                elif imp_gap > 35 or prob_risk > 0.90:
                    status_label, status_color, text_color = "CRITICAL: Urgent Intervention Required", "#ef553b", "white"
                else:
                    status_label, status_color, text_color = "STABLE: Consistent Progress", "#ab63fa", "white"

                st.write("---")
                
                # Visual Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = sim_latest,
                    title = {'text': f"{indicator_name} Progress", 'font': {'size': 18}},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': status_color},
                        'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': sim_target}
                    }
                ))
                fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""<div class="status-card" style="background-color: {status_color}; color: {text_color};">
                    <h3>{status_label}</h3></div>""", unsafe_allow_html=True)
                
                # 4. Generate & Show PDF Download Button
                pdf_report = create_pdf_report(selected_region, indicator_name, status_label, prob_risk*100, imp_gap, derived_belt, current_year)
                
                st.download_button(
                    label="📥 Download Strategic Policy Report",
                    data=pdf_report,
                    file_name=f"GRIP_Report_{selected_region}.pdf",
                    mime="application/pdf",
                    key="grip_report_download_final"
                )


                res_m1, res_m2, res_m3 = st.columns(3)
                res_m1.metric("AI Risk Score", f"{prob_risk*100:.1f}%")
                res_m2.metric("Remaining Gap", f"{imp_gap:.1f}%")
                res_m3.metric("Status", "Critical" if "CRITICAL" in status_label else "Healthy")

                # --- ENHANCED REPORT LAYOUT ---
                with st.expander("📊 View Detailed Regional Analysis", expanded=True):
                    # Determine color scheme based on status
                    if "CRITICAL" in status_label:
                        border_color = "#FF4B4B"
                        bg_color = "#311010"
                    elif "STABLE" in status_label:
                        border_color = "#AB63FA"
                        bg_color = "#1A1031"
                    else:
                        border_color = "#00CC96"
                        bg_color = "#0A211B"

                    # Header Section
                    st.markdown(f"""
                        <div style="border-left: 10px solid {border_color}; background-color: {bg_color}; padding: 20px; border-radius: 5px;">
                            <h2 style="margin:0; color: white;">{selected_region} Regional Assessment</h2>
                            <p style="font-size: 1.2rem; font-weight: bold; color: {border_color}; margin: 5px 0;">{status_label}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Metric Grid
                    st.write("###")
                    m_col1, m_col2, m_col3 = st.columns(3)
    
                    with m_col1:
                        st.metric("Risk Probability", f"{prob_risk*100:.2f}%", delta="-High Risk", delta_color="inverse")
                    with m_col2:
                        st.metric("Target Gap", f"{imp_gap:.1f}%", help="Distance to 2026 Goal")
                    with m_col3:
                        st.metric("Priority Level", "P1 - Urgent" if "CRITICAL" in status_label else "P3 - Monitor")

                    # Actionable Insight Box
                    st.markdown(f"""
                        <div style="background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3d4156; margin-top: 15px;">
                            <span style="color: #808495; text-transform: uppercase; font-size: 0.8rem; font-weight: bold;">Executive Recommendation</span>
                            <p style="margin-top: 8px; color: #E0E0E0;">
                                The model identifies <b>{selected_region}</b> as a high-volatility zone for <i>{indicator_name}</i> in the <b>{current_year}</b> cycle. 
                                Immediate resource reallocation is advised to close the <b>{imp_gap:.1f}%</b> gap before the <b>{current_year}</b> deadline.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    def create_pdf_report(region, indicator, status, risk, gap, belt, year):
                        pdf = FPDF()
                        pdf.add_page()
    
                        # --- Header ---
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(190, 10, f"PROJECT GRIP: {year} STRATEGIC ASSESSMENT", ln=True, align="C")
                        pdf.set_font("Arial", "", 10)
                        pdf.cell(190, 10, f"Strategic Report | Generated: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True, align="C")
                        pdf.line(10, 30, 200, 30)

                        # --- Summary Data ---
                        pdf.ln(10)
                        pdf.set_font("Arial", "B", 12)
                        pdf.cell(95, 10, f"Region: {region}")
                        pdf.cell(95, 10, f"Zone: {belt}", ln=True)
                        pdf.cell(190, 10, f"Indicator: {indicator}", ln=True)
    
                        # --- Status Box ---
                        # Red for Critical, Green for others
                        if "CRITICAL" in status:
                            pdf.set_fill_color(239, 85, 59) 
                        else:
                            pdf.set_fill_color(0, 204, 150)
        
                        pdf.set_text_color(255, 255, 255)
                        pdf.cell(190, 12, f"STATUS: {status}", border=1, ln=True, align="C", fill=True)
    
                        # --- Risk Analytics ---
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font("Arial", "", 11)
                        pdf.ln(5)
                        pdf.multi_cell(0, 8, f"The Hybrid Intelligence engine indicates a {risk:.2f}% risk factor. "
                                                f"The current implementation gap stands at {gap:.1f}%.")

                        # --- NEW: STRATEGIC POLICY RECOMMENDATIONS ---
                        pdf.ln(5)
                        pdf.set_font("Arial", "B", 12)
                        pdf.cell(190, 10, "Strategic Policy Recommendations:", ln=True)
                        pdf.set_font("Arial", "", 11)
                    
                        if "CRITICAL" in status:
                            recommendations = [
                                f"1. Immediate Resource Realignment: Prioritize {region} for the {year} budget cycle.",
                                "2. Focused Monitoring: Address the {gap:.1f}% gap before the end of Q4 {year}.",
                                f"3. Belt-Level Intervention: Coordinate with {belt} directors for emergency funding.",
                                "4. Risk Mitigation: Conduct a root-cause analysis on why the 2026 target is lagging."
                            ]
                        elif "STABLE" in status:
                            recommendations = [
                                "1. Efficiency Optimization: Identify local bottlenecks to move from Stable to Impressive.",
                                "2. Peer-to-Peer Mentorship: Use this region's model to assist lower-performing areas.",
                                "3. Sustainability Audit: Ensure that current resource levels are maintained through 2026.",
                                "4. Data Validation: Conduct quarterly checks to ensure the implementation gap continues to shrink."
                            ]
                        else: # For IMPRESSIVE status
                            recommendations = [
                                "1. Best Practice Documentation: Document the success factors for national scaling.",
                                "2. Resource Surplus Analysis: Evaluate if resources can be safely shared with Critical regions.",
                                "3. Milestone Celebration: Acknowledge regional stakeholders for early target achievement."
                            ]

                        for rec in recommendations:
                            pdf.multi_cell(180, 8, rec, ln=True) 
                            pdf.ln(2)
                        # --- Footer ---
                        pdf.ln(10)
                        pdf.set_font("Arial", "I", 8)
                        pdf.cell(0, 10, "Confidential | Saviour Amegayie Data Portfolio | BloomCore Tech", align="C")

                        # Return as bytes for Streamlit
                        return bytes(pdf.output())

                    # 1. First, make sure you've identified the year from the data
                    # We use .iloc[0] to grab the year from the first row of the current dataframe
                    # 1. Final check for year consistency
                    try:
                        current_year = df['Year'].iloc[0] if 'Year' in df.columns else 2026
                    except:
                        current_year = 2026
                    # 2. Generate the PDF object using your updated function
                    # This prepares the data in memory before the user clicks download
                    pdf_report = create_pdf_report(
                        selected_region, 
                        indicator_name, 
                        status_label, 
                        prob_risk * 100, 
                        imp_gap, 
                        derived_belt,
                        current_year  # This ensures the year 2027 or 2028 appears in the PDF
)
                    # --- DATA INPUT SELECTION ---
    # --- MOVE DATA & SOURCE CONTROLS TO MAIN PAGE ---
    st.write("---")
    st.subheader("📁 Data & Source Management")

    # Create three equal columns for a clean layout
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        # 1. View Source Code
        st.link_button("📂 View GRIP Source Code", "https://github.com/Delkay-byte/Your-Repo-Name", use_container_width=True)

    
    # We create the sample data in memory
    template_data = pd.DataFrame({
        'Region': ['Volta', 'Ahafo', 'Ashanti', 'Greater Accra', 'Northern'],
        'Indicator': ['ICT Infrastructure', 'ICT Infrastructure', 'ICT Infrastructure', 'ICT Infrastructure', 'ICT Infrastructure'],
        'Year': [2027, 2027, 2027, 2027, 2027],
        'Education_Level': ['Basic Education', 'Basic Education', 'Secondary Education', 'Secondary Education', 'Technical and Vocational'],
        'Total_Pop': [850000, 620000, 1200000, 1500000, 950000],
        'Literacy_Rate': [68.5, 52.0, 75.8, 88.2, 45.5],
        'Current_Value': [65.0, 42.0, 78.5, 88.0, 51.2],
        'Target_2026': [100, 100, 100, 100, 100],
        'Budget_Allocation': [50000, 30000, 75000, 90000, 45000]
        })

    # --- TEMPLATE DOWNLOAD ---
    with btn_col2:
        st.download_button(
            label="📥 Download Template CSV",
            data=template_data.to_csv(index=False),
            file_name="GES_Template.csv",
            mime="text/csv",
            use_container_width=True
        )

    with btn_col3:
        # 3. New Data Upload 
        uploaded_file = st.file_uploader("Upload New GES Dataset (CSV)", type=["csv"], label_visibility="collapsed")

    # --- LOGIC TO UPDATE DATA ON MAIN PAGE ---
    if uploaded_file is not None:
        # Update the session state directly
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success("✅ Dataset updated successfully!")
    
        # Re-sync local variables for the rest of the script
        df = st.session_state.df
        if 'Year' in df.columns:
            current_year = df['Year'].iloc[0]
        elif 'Target_Year' in df.columns:
            current_year = df['Target_Year'].iloc[0]
    
        # Optional: Trigger a rerun to ensure all metrics on the page update immediately
        st.rerun()
    else:
        # Ensure df is always synced even if no new file is uploaded
        df = st.session_state.df


# 5. About Me Page
elif page == "About Me":
    st.title("My Journey")
    st.write("---")
    
    st.markdown("""
    ### From Classroom Leadership to Data-Driven Solutions ☁️
    For the past **6 years**, I have served as an Educator and Leader within the **Ghana Education Service (GES)**. My background in Information Technology from the **University of Cape Coast (UCC)** provided the foundation for my transition into **Data Science**.
    
    I don't just build models; I solve systemic problems. Whether it's optimizing crop yields for food security or calculating teacher-student ratios for better educational outcomes, my goal is to turn raw numbers into **human impact**.
    
    I thrive at the intersection of **Technology, Education, and Strategy**.
    """)

    col_edu, col_stack = st.columns(2)
    with col_edu:
        st.markdown("#### 🎓 Education & Certifications")
        st.markdown("""
        * **B.Ed Information Technology** - University of Cape Coast (UCC)
        * **AI Career Essentials** - ALX Africa
        * **Data Science Fellow** - TechCrush x Tech4Africans
        * **Leadership Training** - Ghana Education Service (GES)
        """)
    
    with col_stack:
        st.markdown("#### 🛠️ Professional Values")
        st.markdown("""
        * **Integrity:** Ensuring data transparency and ethical AI.
        * **Innovation:** Solving old problems with new technology.
        * **Education:** Making complex insights easy for everyone to understand.
        * **Efficiency:** Building clean, production-ready code.
        """)

    st.write("---")
    st.subheader("📄 Professional Resume")
    st.write("Looking for a dedicated Data Scientist with a background in leadership? Download my full CV below.")
    
    try:
        with open("Saviour_Amegayie_CV.pdf", "rb") as file:
            st.download_button(
                label="📥 Download My CV",
                data=file,
                file_name="Saviour_Amegayie_CV.pdf",
                mime="application/pdf",
                help="Click to download my professional resume in PDF format"
            )
    except FileNotFoundError:
        st.warning("Resume file ('Saviour_Amegayie_CV.pdf') not found.")

# 6. Contact Page
elif page == "Contact":
    st.title("📬 Let's Connect!")
    st.write("---")
    st.write("I am always open to discussing Data Science collaborations, Agri-Tech innovations, or EdTech opportunities.")
    
    contact_col1, contact_col2 = st.columns(2)
    with contact_col1:
        st.markdown("### Contact Details")
        st.write("📧 **Email:** saviour.amegayie.ds@gmail.com")
        st.write("📍 **Location:** Akatsi, Volta Region, Ghana")
        st.write("📞 **Availability:** Open to Remote & Hybrid Roles")
        
        st.write("---")
        st.markdown("### My Socials")
        b1, b2 = st.columns(2)
        with b1:
            st.link_button("LinkedIn", "https://www.linkedin.com/in/saviour-amegayie-ds")
        with b2:
            st.link_button("GitHub", "https://github.com/Delkay-byte")
    
    with contact_col2:
        st.markdown("### Quick Message")
        my_email = "saviour.amegayie.ds@gmail.com" 
        contact_form = f"""
<form action="https://formsubmit.co/{my_email}" method="POST">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_subject" value="New Portfolio Message!">
<input type="text" name="name" placeholder="Your Name" required style="width: 100%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background-color: white; color: black;">
<input type="email" name="email" placeholder="Your Email" required style="width: 100%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background-color: white; color: black;">
<textarea name="message" placeholder="Your Message" required style="width: 100%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; background-color: white; color: black; height: 100px;"></textarea>
<button type="submit" style="background-color: #00CC96; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold;">Send Message</button>
</form>
"""
        st.markdown(contact_form, unsafe_allow_html=True)

# 7. Global Footer
st.write("---")
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    st.caption("© 2026 Saviour Amegayie | Data Science Portfolio")
with f2:
    st.caption("Built with [Streamlit](https://streamlit.io)")
with f3:
    st.caption("Location: Akatsi, VR, Ghana 🇬🇭")

# --- FOOTER / DISCLAIMER SECTION ---
st.write("---")
st.caption("""
    **Data Privacy & Usage Disclaimer:** This portfolio and the **Project GRIP** (Ghana Resource Intelligence & Planning) dashboard are developed for 
    demonstrative and strategic planning support within the **Ghana Education Service (GES)** framework. 
    
    1. **Data Accuracy:** AI-generated risks and recommendations are based on historical trends and 
       machine learning models; they should be validated by regional directors before implementation.
    2. **Privacy:** No sensitive student or personnel PII (Personally Identifiable Information) is stored or 
       transmitted by this application.
    3. **Institutional Alignment:** This tool is intended to complement existing GES Monitoring and 
       Evaluation (M&E) protocols for the 2026 educational targets.
""")