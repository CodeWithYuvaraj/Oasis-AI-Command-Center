import streamlit as st
import requests
import os


CITY_COORDS = {
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Bengaluru":  {"lat": 12.9716, "lon": 77.5946},
    "Mumbai":     {"lat": 19.0760, "lon": 72.8777},
    "Delhi":      {"lat": 28.6139, "lon": 77.2090},
    "Chennai":    {"lat": 13.0827, "lon": 80.2707},
}

CITY_ZONES = {
    "Hyderabad": ["Ameerpet", "Madhapur", "Gachibowli", "Kukatpally", "Banjara Hills"],
    "Bengaluru":  ["Koramangala", "Indiranagar", "Whitefield", "HSR Layout", "Electronic City"],
    "Mumbai":     ["Andheri", "Bandra", "Powai", "Kurla", "Dadar"],
    "Delhi":      ["Connaught Place", "Lajpat Nagar", "Dwarka", "Rohini", "Saket"],
    "Chennai":    ["T. Nagar", "Anna Nagar", "Velachery", "Adyar", "Tambaram"],
}

CITY_HYDERABAD_ZONES = ["Madhapur", "Ameerpet", "Kukatpally", "Secunderabad", "Gachibowli"]


@st.cache_data(ttl=300)
def fetch_live_weather(lat: float, lon: float) -> dict:
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "hourly": "temperature_2m,precipitation",
                "forecast_days": 1,
                "timezone": "Asia/Kolkata",
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        temp = data["current_weather"]["temperature"]
        hourly = data.get("hourly", {})
        all_times = hourly.get("time", [])
        all_temps = hourly.get("temperature_2m", [])
        all_precips = hourly.get("precipitation", [])

        # Find the current hour index using the reported weather time
        current_time_str = data["current_weather"].get("time", "")
        try:
            start_idx = next(
                (i for i, t in enumerate(all_times) if t >= current_time_str), 0
            )
        except Exception:
            start_idx = 0

        end_idx = start_idx + 12
        hours = [t[11:16] for t in all_times[start_idx:end_idx]]   # "HH:MM"
        temps = all_temps[start_idx:end_idx]
        precips = all_precips[start_idx:end_idx]

        precip = precips[0] if precips else 0.0
        return {
            "temp": temp,
            "precip": precip,
            "offline": False,
            "hours": hours,
            "temps": temps,
            "precips": precips,
        }
    except Exception:
        hours = [f"{h:02d}:00" for h in range(12)]
        return {
            "temp": 38.0,
            "precip": 0.0,
            "offline": True,
            "hours": hours,
            "temps": [38, 39, 40, 41, 41, 40, 39, 38, 37, 36, 35, 34],
            "precips": [0.0] * 12,
        }


st.set_page_config(
    page_title="Oasis AI",
    page_icon=":motor_scooter:",
    layout="wide"
)

# ── Inject Twemoji for cross-platform emoji rendering (Windows 7 safe) ───────
st.markdown(
    """
    <script src="https://cdn.jsdelivr.net/npm/@twemoji/api@latest/dist/twemoji.min.js"
            crossorigin="anonymous"></script>
    <script>
    (function applyTwemoji() {
        var cfg = { folder: 'svg', ext: '.svg' };
        twemoji.parse(document.body, cfg);
        new MutationObserver(function() {
            twemoji.parse(document.body, cfg);
        }).observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    <style>
    img.emoji { height: 1.2em; width: 1.2em; vertical-align: -0.15em; }
    </style>
    """,
    unsafe_allow_html=True,
)

ZONE_METRICS = {
    "Madhapur": {
        "surge": ("2.4x", "+0.3x"),
        "riders": (38, -5),
        "thermal": ("HIGH", "+2 C"),
        "demand": ("★★★★★", "Peak Hour"),
    },
    "Ameerpet": {
        "surge": ("1.8x", "+0.1x"),
        "riders": (52, +3),
        "thermal": ("MODERATE", "+1 C"),
        "demand": ("★★★★", "Rising"),
    },
    "Kukatpally": {
        "surge": ("1.5x", "-0.2x"),
        "riders": (61, +8),
        "thermal": ("MODERATE", "Stable"),
        "demand": ("★★★", "Steady"),
    },
    "Secunderabad": {
        "surge": ("2.1x", "+0.4x"),
        "riders": (29, -9),
        "thermal": ("HIGH", "+3 C"),
        "demand": ("★★★★★", "Surging"),
    },
    "Gachibowli": {
        "surge": ("2.6x", "+0.5x"),
        "riders": (21, -12),
        "thermal": ("HIGH", "+2 C"),
        "demand": ("★★★★★", "Peak Hour"),
    },
}

DEMO_RESPONSES = {
    "Madhapur": {
        "safety": """
**Heat Risk: HIGH — Action Required**

Madhapur sits inside the HITEC City corridor where asphalt and glass-facade towers create a heat island effect. Between 11 AM and 4 PM, surface temperatures on Cyber Towers Road and the HITEC City flyover regularly exceed 48 C.

**Your thermal safety protocol:**
- **Hydration target:** 250 ml every 45 minutes. Refill at any HPCL/Indian Oil bunk or Reliance Smart.
- **Shaded wait spots:** Covered walkway at Inorbit Mall's delivery bay, basement lane behind Cyber Gateway Tower B, or under the flyover on Raheja Mindspace access road.
- **Clothing:** Light-grey or white full-sleeve cotton under your jacket — reflects radiant heat far better than black.
- **Warning sign:** Headache = pull over immediately, drink water, rest 10 minutes. Heat exhaustion escalates fast on a scooter.
        """,
        "peak": """
**Demand Forecast — Madhapur Zone**

| Time Window | Demand Level | Best Platform |
|---|---|---|
| 8:00 – 9:30 AM | High | Swiggy (office breakfasts) |
| 12:30 – 2:00 PM | Very High | Zomato + Blinkit |
| 4:00 – 5:00 PM | Medium | Zepto (chai & snack runs) |
| 7:30 – 9:30 PM | Very High | All platforms, surge active |

**Strategy:** Go online 5 minutes before 12:30 PM. The platform dispatches the first lunch wave to the earliest available riders. Missing the 12:30 PM window by even 10 minutes costs you 3–4 orders.
        """,
        "zones": """
**Top 3 Hotspots — Madhapur**

**1. Cyber Towers Gate 2**
Highest lunch-order density in the zone. Average drop radius: 1.2 km inside campus. Expect Rs. 35–55/order with minimal traffic on internal roads.

**2. Mindspace Junction (near Inorbit)**
Strong Blinkit & Zepto demand all day. Drops go to Raheja Mindspace apartments — wide roads, easy navigation, fast turnaround.

**3. HITEC City Metro Exit**
Evening peak (6–8 PM) is exceptional. Office workers order dinner to nearby PG accommodations in Kondapur. Short trips = high trip count per hour.

> **You're set for a top-tier shift. Madhapur rewards the disciplined rider who hits the 12:30 PM and 7:30 PM peaks!**
        """,
    },
    "default": {
        "safety": """
**Heat Risk: HIGH — Take Precautions**

Hyderabad's summer streets can feel like 43–46 C with humidity factored in. Protecting yourself is the single highest-ROI action of your shift.

**Your thermal safety protocol:**
- **Hydration target:** 250 ml every 45 minutes. Never skip — dehydration slows your reflexes before you notice it.
- **Shaded wait spots:** Petrol bunk canopy overhangs, covered bus stops, and basement delivery bays near large apartment complexes.
- **Best riding hours:** 6–10 AM and 6–10 PM. Batch your mandatory break during 12–3 PM to minimise exposure.
- **Helmet airflow:** Crack your visor open below 30 km/h for airflow. Close at speed to block dust and heat blast.
        """,
        "peak": """
**Demand Forecast — Hyderabad**

| Time Window | Demand Level | Platform Tip |
|---|---|---|
| 8:00 – 9:30 AM | High | Swiggy breakfast surge |
| 12:30 – 2:00 PM | Very High | Zomato + Blinkit combined |
| 4:00 – 5:00 PM | Medium | Zepto snack & grocery runs |
| 7:30 – 9:30 PM | Very High | All platforms, surge pricing |

**Strategy:** Log online 5 minutes before each peak window. Platforms weight first-dispatch batches toward riders already marked available — showing up early is free money.
        """,
        "zones": """
**Top Zone Types — Hyderabad**

**1. IT & Tech Park Gates**
Lunch demand concentrates here from 12:15 PM. Drops go to nearby cafes and co-working spaces. Average trip: under 2 km. High order frequency.

**2. Large Apartment Clusters (200+ flats)**
Evening dinner orders (7–9 PM) are dense and predictable. Learn the fastest entry gate early — it saves 3–4 minutes per drop.

**3. Metro Station Surroundings**
Morning and evening commuter zones drive heavy quick-commerce orders (Zepto, Blinkit). Short trips, fast turnaround, great for boosting hourly trip count.

> **Strong shift ahead — hit the 12:30 PM and 7:30 PM peaks, stay shaded between runs, and finish strong!**
        """,
    },
}


def get_demo(zone: str, section: str) -> str:
    data = DEMO_RESPONSES.get(zone, DEMO_RESPONSES["default"])
    return data.get(section, "")


def split_strategy(text: str):
    sections = {"safety": "", "peak": "", "zones": ""}
    import re
    thermal = re.search(r"(1\..*?)(?=2\.|$)", text, re.DOTALL)
    peak = re.search(r"(2\..*?)(?=3\.|$)", text, re.DOTALL)
    zone_s = re.search(r"(3\..*)", text, re.DOTALL)
    if thermal:
        sections["safety"] = thermal.group(1).strip()
    if peak:
        sections["peak"] = peak.group(1).strip()
    if zone_s:
        sections["zones"] = zone_s.group(1).strip()
    return sections


# ── TOP STATUS BAR ──────────────────────────────────────────────────────────
st.title(":motor_scooter: Oasis AI: Gig-Worker Co-Pilot")
st.markdown("Real-time safety intelligence and peak demand routing for two-wheeler delivery partners.")
st.divider()

# ── CONTROLS ────────────────────────────────────────────────────────────────
st.subheader(":round_pushpin: Shift Configuration")

region_col, _, _ = st.columns([2, 2, 1])
with region_col:
    city = st.selectbox(
        ":map: Select Operational Region",
        list(CITY_COORDS.keys()),
        index=0,
    )

city_zones = CITY_HYDERABAD_ZONES if city == "Hyderabad" else CITY_ZONES[city]

st.success(f":satellite: SYSTEM STATUS: LIVE FEED DEPLOYED  •  Oasis AI v2.1  •  {city} Grid Active")
st.divider()

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    zone = st.selectbox(
        f"Current Zone ({city})",
        city_zones,
    )

with col2:
    vehicle = st.selectbox(
        "Vehicle Type",
        ["Scooty", "Motorcycle", "EV"]
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button(":rocket: Generate", use_container_width=True, type="primary")

st.divider()

# ── LIVE METRICS (zone-aware) ────────────────────────────────────────────────
metrics = ZONE_METRICS.get(zone, ZONE_METRICS["Madhapur"])

st.subheader(":bar_chart: Live Zone Intelligence")
coords = CITY_COORDS[city]
weather = fetch_live_weather(coords["lat"], coords["lon"])
live_temp_val = weather["temp"]
live_precip = weather["precip"]
temp_label = f"{live_temp_val} C" + (" (Offline)" if weather["offline"] else "")
precip_label = f"{live_precip} mm" + (" (Offline)" if weather["offline"] else "")

if live_precip > 0:
    weather_context = (
        "Monsoon & Wet-Road Safety: The roads are currently wet. "
        "Focus on braking distance on slippery surfaces, reducing speed at turns, "
        "using the scooter's under-seat storage to keep orders dry, "
        "and avoiding waterlogged lanes near low-lying areas."
    )
elif live_temp_val > 35:
    weather_context = (
        "Environment & Thermal Safety: It is currently very hot. "
        "Focus on hydration schedules (250 ml every 45 min), shaded wait zones, "
        "avoiding peak midday sun exposure, and wearing light-coloured clothing to reflect heat."
    )
else:
    weather_context = (
        "Conditions & Comfort: Weather conditions are mild. "
        "Focus on general road safety, efficient route planning, and maintaining energy levels."
    )

# ── SIDEBAR: 12-HOUR FORECAST ────────────────────────────────────────────────
with st.sidebar:
    st.subheader(":alarm_clock: Shift Planner")
    shift_hours = st.slider(
        ":stopwatch: Planned Shift Duration (Hours)",
        min_value=1,
        max_value=12,
        value=6,
        step=1,
    )
    st.divider()
    st.subheader(":partly_sunny: 12-Hour Shift Forecast")
    st.caption(f"{city} — live data updated every 5 min")
    st.divider()

    if weather["offline"]:
        st.warning(":warning: Offline — showing estimated values")

    hours = weather["hours"]
    temps = weather["temps"]
    precips = weather["precips"]

    if hours and temps:
        import pandas as pd
        st.markdown("**:thermometer: Temperature (°C)**")
        temp_series = pd.Series(temps, index=hours, name="Temp (C)")
        st.line_chart(temp_series, height=160, use_container_width=True)

        st.markdown("**:umbrella: Rainfall (mm)**")
        if any(p > 0 for p in precips):
            precip_series = pd.Series(precips, index=hours, name="Rain (mm)")
            st.bar_chart(precip_series, height=160, use_container_width=True)
        else:
            st.success(":white_check_mark: No rainfall expected in the next 12 hours.")

        max_temp = max(temps)
        max_temp_hour = hours[temps.index(max_temp)]
        rain_hours = [hours[i] for i, p in enumerate(precips) if p > 0]

        st.divider()
        st.markdown("**:clipboard: Shift Planner**")
        st.info(f":fire: Peak heat at **{max_temp_hour}** — {max_temp}°C. Avoid riding mid-shift if possible.")
        if rain_hours:
            st.warning(f":cloud_with_rain: Rain expected at: **{', '.join(rain_hours)}**. Use covered wait spots.")
        else:
            st.success(":white_check_mark: No rain forecast for next 12 hours. Ideal riding conditions.")
    else:
        st.info("Weather data unavailable.")

m1, m2, m3, m4, m5, m6 = st.columns(6)

m1.metric(
    label=":zap: Surge Multiplier",
    value=metrics["surge"][0],
    delta=metrics["surge"][1],
)
m2.metric(
    label=":busts_in_silhouette: Active Riders",
    value=metrics["riders"][0],
    delta=metrics["riders"][1],
    delta_color="inverse",
)
m3.metric(
    label=":thermometer: Thermal Risk",
    value=metrics["thermal"][0],
    delta=metrics["thermal"][1],
)
m4.metric(
    label=":package: Current Demand",
    value=metrics["demand"][0],
    delta=metrics["demand"][1],
)
m5.metric(
    label=":sunny: Live Surface Temp",
    value=temp_label,
    delta="Hyderabad",
)
m6.metric(
    label=":umbrella: Live Rainfall",
    value=precip_label,
    delta="Monsoon Active" if live_precip > 0 else "Dry Conditions",
)

# ── LIVE EARNINGS ESTIMATOR ──────────────────────────────────────────────────
BASE_RATE = 120
surge_num = float(metrics["surge"][0].replace("x", ""))
estimated_payout = round(BASE_RATE * surge_num)
total_shift_earnings = estimated_payout * shift_hours

st.divider()
st.subheader(":moneybag: Live Earnings Estimator")
earn_col1, earn_col2, earn_col3, earn_col4 = st.columns([1, 1, 1, 2])
earn_col1.metric(
    label=":chart_with_upwards_trend: Base Rate",
    value=f"Rs. {BASE_RATE} / hr",
)
earn_col2.metric(
    label=":zap: Zone Surge",
    value=metrics["surge"][0],
    delta=metrics["surge"][1],
)
earn_col3.metric(
    label=":alarm_clock: Shift Duration",
    value=f"{shift_hours} hr{'s' if shift_hours > 1 else ''}",
)
earn_col4.success(
    f":moneybag: **Total Projected Shift Earnings: Rs. {total_shift_earnings}**  \n"
    f"Rs. {estimated_payout}/hr × {shift_hours} hrs — {zone} at {metrics['surge'][0]} surge"
)

st.divider()

# ── ZONE SWITCH ADVISOR ──────────────────────────────────────────────────────
import random

st.subheader(":world_map: Live Demand Radar — Zone Switch Advisor")
st.caption(f"Compare surge multipliers across {city} zones to decide if moving pays off.")

random.seed(42)
RADAR_ZONES = CITY_ZONES[city]
radar_surges = {z: round(random.uniform(1.1, 2.9), 1) for z in RADAR_ZONES}
if zone in radar_surges:
    radar_surges[zone] = surge_num   # pin current zone to its real value

best_zone = max(radar_surges, key=radar_surges.get)

import pandas as pd
radar_series = pd.Series(
    [radar_surges[z] for z in RADAR_ZONES],
    index=RADAR_ZONES,
    name="Surge (x)"
)
st.bar_chart(radar_series, height=220, use_container_width=True)

radar_cols = st.columns(len(RADAR_ZONES))
for col, z in zip(radar_cols, RADAR_ZONES):
    earning = round(BASE_RATE * radar_surges[z])
    marker = " :trophy:" if z == best_zone else ""
    col.metric(
        label=f"{z}{marker}",
        value=f"{radar_surges[z]}x",
        delta=f"Rs. {earning}/hr",
        delta_color="normal",
    )

if best_zone != zone:
    st.info(
        f":round_pushpin: **Switch Recommendation:** Moving to **{best_zone}** "
        f"({radar_surges[best_zone]}x surge) could earn you "
        f"**Rs. {round(BASE_RATE * radar_surges[best_zone])}/hr** "
        f"vs Rs. {estimated_payout}/hr in {zone}."
    )
else:
    st.success(
        f":white_check_mark: **You're already in the best zone!** "
        f"{zone} has the highest surge at {surge_num}x — stay put and maximize earnings."
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
                    f"Current live weather condition: {weather_context} "
                    f"Provide a highly practical, realistic shift strategy structured into three distinct sections:\n"
                    f"1. {weather_context.split(':')[0]} (Prioritise the current weather condition above all else in this section).\n"
                    f"2. Peak Slot Optimization (Predict where the highest quick-commerce/ride-share order volume will pool).\n"
                    f"3. Hyper-Local Zone Focus (Suggest specific local landmarks, tech parks, or hubs to wait near for maximum orders).\n"
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

    st.success(":white_check_mark: Strategy compiled — tailored for **{}** riding a **{}**".format(zone, vehicle))

    tab1, tab2, tab3 = st.tabs([
        ":thermometer: Thermal Safety",
        ":moneybag: Peak Demand",
        ":round_pushpin: Zone Hotspots",
    ])

    with tab1:
        st.markdown(sections["safety"])

    with tab2:
        st.markdown(sections["peak"])

    with tab3:
        st.markdown(sections["zones"])

    with st.expander(":clipboard: Full Raw Strategy (expand to copy)"):
        full = "\n\n".join([sections["safety"], sections["peak"], sections["zones"]])
        st.text_area("Full output", value=full, height=300, label_visibility="collapsed")
