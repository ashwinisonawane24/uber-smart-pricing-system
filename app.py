import streamlit as st
import pickle
import pandas as pd

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Uber Smart Pricing",
    page_icon="🚗",
    layout="centered"
)

# ================================
# LOAD MODELS
# ================================
@st.cache_resource
def load_models():
    with open("demand_model_small.pkl", "rb") as f:
        demand_model = pickle.load(f)
    with open("fare_model_small.pkl", "rb") as f:
        fare_model = pickle.load(f)
    return demand_model, fare_model

demand_model, fare_model = load_models()

# ================================
# HELPER FUNCTIONS
# ================================
def get_surge(demand):
    if demand < 50:
        return 0.9, "💚 Discount Pricing"
    elif demand < 80:
        return 1.0, "🔵 Normal Pricing"
    elif demand < 120:
        return 1.2, "🟡 Mild Surge"
    elif demand < 160:
        return 1.5, "🟠 Surge Pricing"
    else:
        return 2.0, "🔴 Peak Surge!"

day_map = {
    "Monday"   : 0,
    "Tuesday"  : 1,
    "Wednesday": 2,
    "Thursday" : 3,
    "Friday"   : 4,
    "Saturday" : 5,
    "Sunday"   : 6
}

# ================================
# APP HEADER
# ================================
st.title("🚗 Uber Smart Pricing System")
st.markdown("**Powered by Machine Learning**")
st.markdown(
    "Analyzing 200,000 real Uber rides")
st.markdown("---")

# ================================
# SIDEBAR
# ================================
with st.sidebar:
    st.header("📌 About")
    st.markdown("""
    This app predicts:
    - 🚦 Ride Demand
    - 💰 Base Fare
    - ⚡ Surge Multiplier
    - 🎯 Smart Price

    **Built by:** Ashwini Sonawane

    **Key Finding:**
    Non-peak fare ($11.63) >
    Peak fare ($11.05)
    = $98,000 revenue opportunity!

    **Dataset:**
    200,000 real Uber rides

    **Models Used:**
    Random Forest (ML)
    """)

# ================================
# INPUT SECTION
# ================================
st.header("📥 Enter Ride Details")

col1, col2 = st.columns(2)

with col1:
    hour = st.selectbox(
        "🕐 Hour of Day",
        options=list(range(24)),
        format_func=lambda x:
            f"{x:02d}:00",
        index=19
    )
    day = st.selectbox(
        "📅 Day of Week",
        options=list(day_map.keys()),
        index=4
    )

with col2:
    passengers = st.slider(
        "👥 Passengers",
        min_value=1,
        max_value=6,
        value=1
    )
    month = st.selectbox(
        "📆 Month",
        options=list(range(1, 13)),
        format_func=lambda x: [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ][x-1],
        index=9
    )

# Auto detect peak and weekend
is_peak = 1 if (7 <= hour <= 10 or
                16 <= hour <= 20) else 0
is_weekend = 1 if day in [
    "Saturday", "Sunday"] else 0
day_num = day_map[day]

# Show auto detected values
col3, col4 = st.columns(2)
with col3:
    if is_peak:
        st.info("⚡ Peak Hour!")
    else:
        st.info("😴 Non Peak Hour")
with col4:
    if is_weekend:
        st.info("🎉 Weekend!")
    else:
        st.info("💼 Weekday")

# ================================
# PREDICT BUTTON
# ================================
st.markdown("---")
predict = st.button(
    "🔍 Predict Price & Demand",
    use_container_width=True,
    type="primary"
)

# ================================
# RESULTS
# ================================
if predict:

    # Prepare demand input
    demand_input = pd.DataFrame({
        "hour"           : [hour],
        "passenger_count": [passengers],
        "is_peak_hour"   : [is_peak],
        "is_weekend"     : [is_weekend],
        "month"          : [month],
        "day_num"        : [day_num]
    })

    # Prepare fare input
    fare_input = pd.DataFrame({
        "hour"           : [hour],
        "passenger_count": [passengers],
        "is_peak_hour"   : [is_peak],
        "is_weekend"     : [is_weekend],
        "month"          : [month],
        "day_num"        : [day_num]
    })

    # Get predictions
    demand = demand_model.predict(
        demand_input)[0]
    fare = fare_model.predict(
        fare_input)[0]

    # Calculate surge and smart price
    multiplier, category = get_surge(demand)
    smart_price = round(fare * multiplier, 2)

    # --------------------------------
    # SHOW RESULTS
    # --------------------------------
    st.markdown("---")
    st.header("📊 Prediction Results")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "🚦 Demand",
            f"{int(demand):,}",
            "rides/hour"
        )
    with col6:
        st.metric(
            "💰 Base Fare",
            f"${fare:.2f}"
        )
    with col7:
        st.metric(
            "⚡ Surge",
            f"{multiplier}x"
        )
    with col8:
        st.metric(
            "🎯 Smart Price",
            f"${smart_price:.2f}"
        )

    # Pricing strategy
    st.markdown("---")
    st.subheader("💡 Pricing Strategy")
    st.success(f"**{category}**")

    if multiplier < 1.0:
        st.info(
            "📉 Low demand — "
            "discount applied "
            "to attract riders!")
    elif multiplier == 1.0:
        st.info(
            "✅ Normal demand — "
            "standard pricing!")
    elif multiplier <= 1.2:
        st.warning(
            "📈 Moderate demand — "
            "mild surge active!")
    elif multiplier <= 1.5:
        st.warning(
            "🔥 High demand — "
            "surge pricing active!")
    else:
        st.error(
            "🚨 Peak demand — "
            "maximum surge! "
            "Deploy more drivers!")

    # Revenue impact
    st.markdown("---")
    st.subheader("💰 Revenue Impact")

    base_rev = int(demand * fare)
    smart_rev = int(demand * smart_price)
    extra = smart_rev - base_rev

    col9, col10, col11 = st.columns(3)
    with col9:
        st.metric(
            "Base Revenue",
            f"${base_rev:,}"
        )
    with col10:
        st.metric(
            "Smart Revenue",
            f"${smart_rev:,}"
        )
    with col11:
        st.metric(
            "Extra Earned",
            f"${extra:,}",
            "from smart pricing"
        )

    # Summary table
    st.markdown("---")
    st.subheader("📋 Summary")
    st.markdown(f"""
| Detail | Value |
|--------|-------|
| Hour | {hour:02d}:00 |
| Day | {day} |
| Passengers | {passengers} |
| Peak Hour | {"Yes ⚡" if is_peak else "No"} |
| Weekend | {"Yes 🎉" if is_weekend else "No"} |
| Demand | {int(demand):,} rides |
| Base Fare | ${fare:.2f} |
| Surge | {multiplier}x |
| **Smart Price** | **${smart_price:.2f}** |
| **Strategy** | **{category}** |
    """)

# ================================
# FOOTER
# ================================
st.markdown("---")
st.markdown("""
<div style='text-align:center'>
<p>Built by <b>Ashwini Sonawane</b> |
200,000 Uber rides analyzed |
<a href='https://github.com/ashwinisonawane24/
uber-smart-pricing-system'>
GitHub</a>
</p>
</div>
""", unsafe_allow_html=True)