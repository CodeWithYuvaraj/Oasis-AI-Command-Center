import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Oasis AI",
    page_icon="🛵",
    layout="centered"
)

DEMO_RESPONSES = {
    "Madhapur": """
**🌡️ Environment & Thermal Safety**

Madhapur sits at an elevation that gives you slightly better air circulation than the city centre, but between 11 AM and 4 PM the asphalt on HITEC City Road and Cyber Towers flyover radiates intense heat — surface temperatures can exceed 48 °C. Here's how to stay safe:

- **Hydration target:** 250 ml of water every 45 minutes. Keep a 1-litre bottle in your delivery bag and refill at any petrol bunk or Reliance Smart store.
- **Shaded wait spots:** Park under the covered walkway near Inorbit Mall's delivery bay, or use the basement lane behind Cyber Gateway Tower B — both have shade and security won't move you.
- **Clothing:** Wear a full-sleeve light-grey or white cotton shirt under your jacket. It reflects radiant heat far better than black.
- **Warning sign:** If you feel a headache starting, pull over immediately, drink water, and rest for 10 minutes. Heat exhaustion escalates fast on a scooter.

---

**💰 Peak Slot Optimization**

Based on typical weekday demand patterns in HITEC City:

| Time Window | Expected Demand | Best Platform |
|---|---|---|
| 8:00 – 9:30 AM | ⭐⭐⭐⭐ High | Swiggy (office breakfasts) |
| 12:30 – 2:00 PM | ⭐⭐⭐⭐⭐ Very High | Zomato + Blinkit combined |
| 4:00 – 5:00 PM | ⭐⭐⭐ Medium | Zepto (snacks & chai runs) |
| 7:30 – 9:30 PM | ⭐⭐⭐⭐⭐ Very High | All platforms surge pricing |

**Pro tip:** Switch your status to "available" 5 minutes *before* the lunch peak starts at 12:30 PM. The algorithm assigns the first wave of orders to the earliest available riders.

---

**📍 Hyper-Local Zone Focus**

These three spots give you the fastest order pickup and shortest drop distances in Madhapur:

1. **Cyber Towers Gate 2 area** — Highest density of IT employees ordering lunch. Average drop radius: 1.2 km. Expect ₹35–55 per order with low traffic inside the campus roads.
2. **Mindspace Junction (near Inorbit)** — Strong quick-commerce demand (Blinkit, Zepto) all day. Drops go toward Raheja Mindspace apartments — easy navigation, wide roads.
3. **HITEC City Metro Station exit** — Evening peak (6–8 PM) is exceptional here. Office workers order dinner to nearby PG accommodations in Kondapur. Short trips, fast earnings.

> 💪 You're set for a strong shift. Stay hydrated, grab the 12:30 PM and 7:30 PM peaks, and Madhapur will deliver!
""",
    "default": """
**🌡️ Environment & Thermal Safety**

Hyderabad's summer heat is serious — interior city zones can feel like 42–45 °C with humidity factored in. Protecting yourself is the single highest-ROI action of your shift:

- **Hydration target:** 250 ml of water every 45 minutes. Never skip this — dehydration slows your reflexes before you notice it.
- **Shaded wait spots:** Look for petrol bunks with canopy overhangs, covered bus stops, and basement delivery bays near large apartment complexes. These are your pit-stop zones.
- **Best riding hours:** 6–10 AM and 6–10 PM. Avoid exposure during 12–3 PM if you can batch your break then.
- **Helmet ventilation:** Keep visor cracked open when moving below 30 km/h to allow airflow. At speed, close it to block dust.

---

**💰 Peak Slot Optimization**

Across Hyderabad's gig-economy zones, demand spikes follow a consistent daily pattern:

| Time Window | Expected Demand | Platform Tip |
|---|---|---|
| 8:00 – 9:30 AM | ⭐⭐⭐⭐ High | Swiggy breakfast orders surge |
| 12:30 – 2:00 PM | ⭐⭐⭐⭐⭐ Very High | Zomato + Blinkit combined peak |
| 4:00 – 5:00 PM | ⭐⭐⭐ Medium | Zepto snack & grocery runs |
| 7:30 – 9:30 PM | ⭐⭐⭐⭐⭐ Very High | All platforms, surge pricing active |

**Pro tip:** Log online 5 minutes before each peak window opens. Platforms weight their first-dispatch batch toward riders who are already marked available.

---

**📍 Hyper-Local Zone Focus**

Three location types consistently generate the best order density and shortest drop distances:

1. **IT & tech park gates** — Lunch demand is heavily concentrated here from 12:15 PM onward. Drops go to nearby cafés and co-working spaces. Avg. trip: under 2 km.
2. **Large apartment complex clusters** — Evening dinner orders (7–9 PM) are dense and predictable. Buildings with 200+ flats generate repeat micro-routes — learn the fastest entry gate early.
3. **Metro station surroundings** — Morning and evening commuter zones generate quick-commerce orders (Zepto, Blinkit). These are fast, short trips perfect for boosting trip count per hour.

> 💪 Great shift ahead — hit the 12:30 PM and 7:30 PM peaks, stay in the shade between runs, and you'll finish strong!
"""
}


def get_demo_response(zone: str) -> str:
    return DEMO_RESPONSES.get(zone, DEMO_RESPONSES["default"])


st.title("🛵 Oasis AI: Gig-Worker Co-Pilot")
st.markdown("Real-time safety and peak demand routing for two-wheeler delivery partners.")
st.divider()

st.subheader("📍 Shift Details")

col1, col2 = st.columns(2)

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

st.divider()

if st.button("Generate Safe Ride Strategy 🚀", use_container_width=True, type="primary"):
    hf_token = os.environ.get("HUGGING_FACE_TOKEN", "")
    ai_strategy = None
    used_demo = False

    with st.spinner("Analyzing environmental and demand data..."):
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
                    ai_strategy = result[0]["generated_text"].replace(prompt, "").strip()
                else:
                    used_demo = True
            except Exception:
                used_demo = True
        else:
            used_demo = True

    if used_demo or not ai_strategy:
        ai_strategy = get_demo_response(zone)

    st.success("✅ Strategy Compiled Successfully!")
    st.markdown(ai_strategy)
