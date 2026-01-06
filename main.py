import streamlit as st
import requests
from prediction_helper import predict

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    layout="wide"
)

# --------------------------------------------------
# PROFESSIONAL CORPORATE CSS
# --------------------------------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
html, body {
    font-family: 'Inter', sans-serif;
    background-color: #f8f9fb;
    color: #1f2937;
}

/* Headings */
h1 {
    font-size: 32px;
    font-weight: 600;
    color: #111827;
}
h2, h3, h4 {
    color: #111827;
    font-weight: 600;
}

/* Section container */
.section-card {
    background-color: #ffffff;
    padding: 24px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    margin-top: 20px;
}

/* Labels */
.stMarkdown strong {
    font-size: 13px;
    color: #374151;
}

/* Inputs */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 6px;
    border: 1px solid #d1d5db;
}

/* Button */
.stButton > button {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    border-radius: 6px;
    height: 44px;
    width: 100%;
    font-size: 15px;
}

/* Result boxes */
.success-box {
    background-color: #ecfdf5;
    padding: 16px;
    border-radius: 6px;
    border: 1px solid #a7f3d0;
    color: #065f46;
}

.warning-box {
    background-color: #fffbeb;
    padding: 16px;
    border-radius: 6px;
    border: 1px solid #fde68a;
    color: #92400e;
}

.error-box {
    background-color: #fef2f2;
    padding: 16px;
    border-radius: 6px;
    border: 1px solid #fecaca;
    color: #991b1b;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("Health Insurance Premium Predictor")
st.markdown(
    "Estimate insurance premium based on personal, medical, and employment information."
)
st.markdown("---")

# --------------------------------------------------
# FORM
# --------------------------------------------------
with st.form("prediction_form"):

    def section(title):
        st.markdown(
            f"<div class='section-card'><h4>{title}</h4>",
            unsafe_allow_html=True
        )

    # ================= PERSONAL =================
    section("Personal Details")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Age**")
        age = st.number_input("Age", 18, 100, label_visibility="collapsed")

    with c2:
        st.markdown("**Number of Dependents**")
        dependents = st.number_input("Dependents", 0, 5, label_visibility="collapsed")

    with c3:
        st.markdown("**Annual Income (Lakhs)**")
        income_lakhs = st.number_input("Income", 0, 100, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= MEDICAL =================
    section("Medical Details")
    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown("**Genetical Risk (0–5)**")
        genetical_risk = st.number_input("Risk", 0, 5, label_visibility="collapsed")

    with c5:
        st.markdown("**BMI Category**")
        bmi_category = st.selectbox(
            "BMI",
            ["Underweight", "Normal", "Overweight", "Obesity"],
            label_visibility="collapsed"
        )

    with c6:
        st.markdown("**Smoking Status**")
        smoking_status = st.selectbox(
            "Smoking",
            ["No Smoking", "Occasional", "Regular"],
            label_visibility="collapsed"
        )

    c7, c8, c9 = st.columns(3)

    with c7:
        st.markdown("**Gender**")
        gender = st.selectbox("Gender", ["Male", "Female"], label_visibility="collapsed")

    with c8:
        st.markdown("**Marital Status**")
        marital_status = st.selectbox(
            "Marital", ["Unmarried", "Married"], label_visibility="collapsed"
        )

    with c9:
        st.markdown("**Medical History**")
        medical_history = st.selectbox(
            "History",
            [
                "No Disease",
                "Diabetes",
                "High blood pressure",
                "Heart disease",
                "Thyroid",
                "Diabetes & High blood pressure",
                "Diabetes & Heart disease",
                "Diabetes & Thyroid",
                "High blood pressure & Heart disease"
            ],
            label_visibility="collapsed"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= EMPLOYMENT =================
    section("Employment & Insurance")
    c10, c11, c12 = st.columns(3)

    with c10:
        st.markdown("**Insurance Plan**")
        insurance_plan = st.selectbox(
            "Plan", ["Bronze", "Silver", "Gold"], label_visibility="collapsed"
        )

    with c11:
        st.markdown("**Employment Status**")
        employment_status = st.selectbox(
            "Employment",
            ["Salaried", "Self-Employed", "Freelancer"],
            label_visibility="collapsed"
        )

    with c12:
        st.markdown("**Region**")
        region = st.selectbox(
            "Region",
            ["Northeast", "Northwest", "Southeast", "Southwest"],
            label_visibility="collapsed"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    submit = st.form_submit_button("Predict Premium")

# --------------------------------------------------
# PREDICTION RESULT
# --------------------------------------------------
if submit:
    input_dict = {
        "Age": age,
        "Number of Dependents": dependents,
        "Income in Lakhs": income_lakhs,
        "Genetical Risk": genetical_risk,
        "Insurance Plan": insurance_plan,
        "Employment Status": employment_status,
        "Gender": gender,
        "Maritial Status": marital_status,
        "BMI Category": bmi_category,
        "Smoking status": smoking_status,
        "Region": region,
        "Medical History": medical_history
    }

    prediction = predict(input_dict)

    st.markdown("---")
    st.subheader("Prediction Result")

    st.markdown(
        f"""
        <div class="section-card">
            <strong>Predicted Annual Premium (₹)</strong>
            <h2 style="margin-top:8px;">{prediction:,.0f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Health Assessment")

    health_score = 10
    if smoking_status == "Regular":
        health_score -= 4
    elif smoking_status == "Occasional":
        health_score -= 2

    if bmi_category in ["Overweight", "Obesity"]:
        health_score -= 2

    if medical_history != "No Disease":
        health_score -= 3

    if genetical_risk >= 3:
        health_score -= 2

    if health_score >= 8:
        st.markdown(
            "<div class='success-box'>Health risk appears low.</div>",
            unsafe_allow_html=True
        )
    elif 5 <= health_score < 8:
        st.markdown(
            "<div class='warning-box'>Moderate health risk detected.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='error-box'>High health risk detected. Medical consultation recommended.</div>",
            unsafe_allow_html=True
        )
