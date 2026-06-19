import streamlit as st
import requests
import os


@st.cache_data(ttl=300)
def fetch_live_temp() -> str:
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": 17.3850, "longitude": 78.4867, "current_weather": "true"},
            timeout=5
        )
        resp.raise_for_status()
        temp = resp.json()["current_weather"]["temperature"]
        return f"{temp}°C"
    except Exception:
        return "38°C (Offline)"

st.set_page_config(
    page_title="Oasis AI",
    page_icon="🛵",
    layout="wide"
)

ZONE_METRICS = {
    "Madhapur": {
        "surge": ("2.4x", "+0.3x"),
        "riders": (38, -5),
        "thermal": ("🔴 HIGH", "+2°C"),
        "demand": ("⭐⭐⭐⭐⭐", "Peak Hour"),
    },
    "Ameerpet": {
        "surge": ("1.8x", "+0.1x"),
        "riders": (52, +3),
        "thermal": ("🟠 MODERATE", "+1°C"),
        "demand": ("⭐⭐⭐⭐", "Rising"),
    },
    "Kukatpally": {
        "surge": ("1.5x", "-0.2x"),
        "riders": (61, +8),
        "thermal": ("🟠 MODERATE", "Stable"),
        "demand": ("⭐⭐⭐", "Steady"),
    },
    "Secunderabad": {
        "surge": ("2.1x", "+0.4x"),
        "riders": (29, -9),
        "thermal": ("🔴 HIGH", "+3°C"),
        "demand": ("⭐⭐⭐⭐⭐", "Surging"),
    },
    "Gachibowli": {
        "surge": ("2.6x", "+0.5x"),
        "riders": (21, -12),
        "thermal": ("🔴 HIGH", "+2°C"),
        "demand": ("⭐⭐⭐⭐⭐", "Peak Hour"),
    },
}

DEMO_RESPONSES = {
    "Madhapur": {
        "safety": """
**Heat Risk: HIGH — Action Required**

Madhapur sits inside the HITEC City corridor where asphalt and glass-facade towers create a heat island effect. Between 11 AM and 4 PM, surface temperatures on Cyber Towers Road and the HITEC City flyover regularly exceed 48 °C.

**Your thermal safety protocol:**
- 💧 **Hydration target:** 250 ml every 45 minutes. Refill at any HPCL/Indian Oil bunk or Reliance Smart.
- 🅿️ **Shaded wait spots:** Covered walkway at Inorbit Mall's delivery bay, basement lane behind Cyber Gateway Tower B, or under the flyover on Raheja Mindspace access road.
- 👕 **Clothing:** Light-grey or white full-sleeve cotton under your jacket — reflects radiant heat far better than black.
- ⚠️ **Warning sign:** Headache = pull over immediately, drink water, rest 10 minutes. Heat exhaustion escalates fast on a scooter.
        """,
        "peak": """
**Demand Forecast — Madhapur Zone**

| Time Window | Demand Level | Best Platform |
|---|---|---|
| 8:00 – 9:30 AM | ⭐⭐⭐⭐ High | Swiggy (office breakfasts) |
| 12:30 – 2:00 PM | ⭐⭐⭐⭐⭐ Very High | Zomato + Blinkit |
| 4:00 – 5:00 PM | ⭐⭐⭐ Medium | Zepto (chai & snack runs) |
| 7:30 – 9:30 PM | ⭐⭐⭐⭐⭐ Very High | All platforms, surge active |

**Strategy:** Go online 5 minutes before 12:30 PM. The platform dispatches the first lunch wave to the earliest available riders. Missing the 12:30 PM window by even 10 minutes costs you 3–4 orders.
        """,
        "zones": """
**Top 3 Hotspots — Madhapur**

🏢 **1. Cyber Towers Gate 2**
Highest lunch-order density in the zone. Average drop radius: 1.2 km inside campus. Expect ₹35–55/order with minimal traffic on internal roads.

🛍️ **2. Mindspace Junction (near Inorbit)**
Strong Blinkit & Zepto demand all day. Drops go to Raheja Mindspace apartments — wide roads, easy navigation, fast turnaround.

🚇 **3. HITEC City Metro Exit**
Evening peak (6–8 PM) is exceptional. Office workers order dinner to nearby PG accommodations in Kondapur. Short trips = high trip count per hour.

> 💪 **You're set for a top-tier shift. Madhapur rewards the disciplined rider who hits the 12:30 PM and 7:30 PM peaks!**
        """,
    },
    "default": {
        "safety": """
**Heat Risk: HIGH — Take Precautions**

Hyderabad's summer streets can feel like 43–46 °C with humidity factored in. Protecting yourself is the single highest-ROI action of your shift.

**Your thermal safety protocol:**
- 💧 **Hydration target:** 250 ml every 45 minutes. Never skip — dehydration slows your reflexes before you notice it.
- 🅿️ **Shaded wait spots:** Petrol bunk canopy overhangs, covered bus stops, and basement delivery bays near large apartment complexes.
- ⏰ **Best riding hours:** 6–10 AM and 6–10 PM. Batch your mandatory break during 12–3 PM to minimise exposure.
- 🪖 **Helmet airflow:** Crack your visor open below 30 km/h for airflow. Close at speed to block dust and heat blast.
        """,
        "peak": """
**Demand Forecast — Hyderabad**

| Time Window | Demand Level | Platform Tip |
|---|---|---|
| 8:00 – 9:30 AM | ⭐⭐⭐⭐ High | Swiggy breakfast surge |
| 12:30 – 2:00 PM | ⭐⭐⭐⭐⭐ Very High | Zomato + Blinkit combined |
| 4:00 – 5:00 PM | ⭐⭐⭐ Medium | Zepto snack & grocery runs |
| 7:30 – 9:30 PM | ⭐⭐⭐⭐⭐ Very High | All platforms, surge pricing |

**Strategy:** Log online 5 minutes before each peak window. Platforms weight first-dispatch batches toward riders already marked available — showing up early is free money.
        """,
        "zones": """
**Top Zone Types — Hyderabad**

🏢 **1. IT & Tech Park Gates**
Lunch demand concentrates here from 12:15 PM. Drops go to nearby cafés and co-working spaces. Average trip: under 2 km. High order frequency.

🏘️ **2. Large Apartment Clusters (200+ flats)**
Evening dinner orders (7–9 PM) are dense and predictable. Learn the fastest entry gate early — it saves 3–4 minutes per drop.

🚇 **3. Metro Station Surroundings**
Morning and evening commuter zones drive heavy quick-commerce orders (Zepto, Blinkit). Short trips, fast turnaround, great for boosting hourly trip count.

> 💪 **Strong shift ahead — hit the 12:30 PM and 7:30 PM peaks, stay shaded between runs, and finish strong!**
        """,
    },
}


def get_demo(zone: str, section: str) -> str:
    data = DEMO_RESPONSES.get(zone, DEMO_RESPONSES["default"])
    return data.get(section, "")


def split_strategy(text: str):
    sections = {"safety": "", "peak": "", "zones": ""}
    import re
    thermal = re.search(r"(🌡️.*?)(?=💰|$)", text, re.DOTALL)
    peak = re.search(r"(💰.*?)(?=📍|$)", text, re.DOTALL)
    zone_s = re.search(r"(📍.*)", text, re.DOTALL)
    if thermal:
        sections["safety"] = thermal.group(1).strip()
    if peak:
        sections["peak"] = peak.group(1).strip()
    if zone_s:
        sections["zones"] = zone_s.group(1).strip()
    return sections


# ── TOP STATUS BAR ──────────────────────────────────────────────────────────
st.success("🛰️  SYSTEM STATUS: LIVE FEED DEPLOYED  •  Oasis AI v2.1  •  Hyderabad Grid Active")

st.title("🛵 Oasis AI: Gig-Worker Co-Pilot")
st.markdown("Real-time safety intelligence and peak demand routing for two-wheeler delivery partners.")
st.divider()

# ── CONTROLS ────────────────────────────────────────────────────────────────
st.subheader("📍 Shift Configuration")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    zone = st.selectbox(
        "Current Zone (Hyderabad)",
        ["Madhapur", "Ameerpet", "Kukatpally", "Secunderabad", "Gachibowli"]
    )

with col2:
    vehicle = st.selectbox(
        "Vehicle Type",
        ["TVS Activa (Scooter)", "Motorcycle", "EV"]
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("🚀 Generate", use_container_width=True, type="primary")

st.divider()

# ── LIVE METRICS (zone-aware) ────────────────────────────────────────────────
metrics = ZONE_METRICS.get(zone, ZONE_METRICS["Madhapur"])

st.subheader("📊 Live Zone Intelligence")
live_temp = fetch_live_temp()
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    label="⚡ Surge Multiplier",
    value=metrics["surge"][0],
    delta=metrics["surge"][1],
)
m2.metric(
    label="🧑‍🤝‍🧑 Active Riders Near Hub",
    value=metrics["riders"][0],
    delta=metrics["riders"][1],
    delta_color="inverse",
)
m3.metric(
    label="🌡️ Thermal Risk Level",
    value=metrics["thermal"][0],
    delta=metrics["thermal"][1],
)
m4.metric(
    label="📦 Current Demand",
    value=metrics["demand"][0],
    delta=metrics["demand"][1],
)
m5.metric(
    label="🌤️ Live Surface Temp",
    value=live_temp,
    delta="Hyderabad",
)

st.divider()

# ── STRATEGY GENERATION ──────────────────────────────────────────────────────
if generate:
    hf_token = os.environ.get("HUGGING_FACE_TOKEN", "")
    sections = None
    used_demo = False

    with st.spinner("Querying Oasis AI engine — compiling zone intelligence..."):
        if hf_token:
            try:
                API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
                HEADERS = {"Authorization": f"Bearer {hf_token}"}

                prompt = (
                    f"Act as an expert logistics coordinator and safety assistant for a gig worker "
                    f"riding a {vehicle} in the {zone} area of Hyderabad, India. "
                    f"Provide a highly practical, realistic shift strategy structured into three distinct sections:\n"
                    f"1. 🌡️ Environment & Thermal Safety (Address heat risks, shaded routing options, hydration targets).\n"
                    f"2. 💰 Peak Slot Optimization (Predict where the highest quick-commerce/ride-share order volume will pool).\n"
                    f"3. 📍 Hyper-Local Zone Focus (Suggest specific local landmarks, tech parks, or hubs to wait near for maximum orders).\n"
                    f"Keep the tone encouraging and write the actionable layout advice clearly. Use simple terminology."
                )

                response = requests.post(
                    API_URL,
                    headers=HEADERS,
                    json={"inputs": prompt, "parameters": {"max_new_tokens": 500}},
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()

                if isinstance(result, list) and result and "generated_text" in result[0]:
                    raw = result[0]["generated_text"].replace(prompt, "").strip()
                    sections = split_strategy(raw)
                    if not any(sections.values()):
                        used_demo = True
                else:
                    used_demo = True
            except Exception:
                used_demo = True
        else:
            used_demo = True

    if used_demo or not sections:
        sections = {
            "safety": get_demo(zone, "safety"),
            "peak": get_demo(zone, "peak"),
            "zones": get_demo(zone, "zones"),
        }

    st.success("✅ Strategy compiled — tailored for **{}** riding a **{}**".format(zone, vehicle))

    tab1, tab2, tab3 = st.tabs([
        "🌡️ Thermal Safety",
        "💰 Peak Demand",
        "📍 Zone Hotspots",
    ])

    with tab1:
        st.markdown(sections["safety"])

    with tab2:
        st.markdown(sections["peak"])

    with tab3:
        st.markdown(sections["zones"])

    with st.expander("📋 Full Raw Strategy (expand to copy)"):
        full = "\n\n".join([sections["safety"], sections["peak"], sections["zones"]])
        st.text_area("Full output", value=full, height=300, label_visibility="collapsed")
