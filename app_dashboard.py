import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.linear_model import LinearRegression

# ==========================================
# PAGE CONFIGURATION & THEMING
# ==========================================
st.set_page_config(
    page_title="2026 F1 Command Center - Mercedes & Ferrari",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark F1 Matplotlib Theme
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '#0E1117'
plt.rcParams['figure.facecolor'] = '#0E1117'
plt.rcParams['text.color'] = '#FFFFFF'
plt.rcParams['axes.labelcolor'] = '#FFFFFF'
plt.rcParams['xtick.color'] = '#FFFFFF'
plt.rcParams['ytick.color'] = '#FFFFFF'
plt.rcParams['grid.color'] = '#333333'

# ==========================================
# 2026 SEASON DATABASE (Up to Bahrain GP Malaysia)
# ==========================================
RACES_2026 = {
    "Australian Grand Prix": {
        "top_5": ["RUS", "ANT", "LEC", "HAM", "NOR"],
        "top_times": [83.1, 83.3, 83.6, 83.9, 84.2],
        "image": "AUS.png",
        "total_laps": 58,
        "dnfs": {}
    },
    "Chinese Grand Prix": {
        "top_5": ["ANT", "RUS", "HAM", "LEC", "BEA"],
        "top_times": [93.2, 93.5, 93.9, 94.1, 94.5],
        "image": "SHA.png",
        "total_laps": 56,
        "dnfs": {}
    },
    "Japanese Grand Prix": {
        "top_5": ["ANT", "PIA", "LEC", "RUS", "NOR"],
        "top_times": [88.0, 88.4, 88.6, 88.9, 89.2],
        "image": "JAP.png",
        "total_laps": 53,
        "dnfs": {}
    },
    "Miami Grand Prix": {
        "top_5": ["ANT", "NOR", "PIA", "RUS", "VER"],
        "top_times": [93.3, 93.5, 93.9, 94.2, 94.6],
        "image": "MIA.png",
        "total_laps": 57,
        "dnfs": {}
    },
    "Canadian Grand Prix": {
        "top_5": ["ANT", "HAM", "VER", "LEC", "HAD"],
        "top_times": [73.1, 73.4, 73.5, 73.8, 74.0],
        "image": "CAN.png",
        "total_laps": 70,
        "dnfs": {"RUS": 31}  # DNF on lap 31
    },
    "Monaco Grand Prix": {
        "top_5": ["ANT", "HAM", "HAD", "PIA", "LAW"],
        "top_times": [74.2, 74.5, 74.9, 75.1, 75.4],
        "image": "MON.png",
        "total_laps": 78,
        "dnfs": {"LEC": 64}
    },
    "Spanish Grand Prix (Barcelona)": {
        "top_5": ["HAM", "RUS", "NOR", "VER", "PIA"],
        "top_times": [78.1, 78.4, 78.6, 78.9, 79.2],
        "image": "SPA.png",
        "total_laps": 66,
        "dnfs": {"ANT": 61, "LEC": 62}
    },
    "Austrian Grand Prix": {
        "top_5": ["RUS", "VER", "ANT", "PIA", "HAM"],
        "top_times": [67.8, 68.0, 68.1, 68.4, 68.6],
        "image": "AUST.png",
        "total_laps": 71,
        "dnfs": {}
    },
    "British Grand Prix": {
        "top_5": ["LEC", "RUS", "HAM", "NOR", "HAD"],
        "top_times": [87.1, 87.2, 87.3, 87.6, 87.9],
        "image": "SIL.png",
        "total_laps": 52,
        "dnfs": {}
    },
    "Belgian Grand Prix": {
        "top_5": ["ANT", "LEC", "VER", "HAM", "PIA"],
        "top_times": [104.2, 104.5, 104.9, 105.2, 105.6],
        "image": "BEL.png",
        "total_laps": 44,
        "dnfs": {"RUS": 0}  # DNF on lap 0
    },
    "Hungarian Grand Prix": {
        "top_5": ["NOR", "VER", "ANT", "LEC", "HAM"],
        "top_times": [79.8, 80.1, 80.3, 80.6, 80.9],
        "image": "HUN.png",
        "total_laps": 70,
        "dnfs": {}
    },
    "Dutch Grand Prix": {
        "top_5": ["NOR", "ANT", "RUS", "HAM", "LEC"],
        "top_times": [72.4, 72.7, 72.9, 73.2, 73.5],
        "image": "DUT.png",
        "total_laps": 72,
        "dnfs": {}
    },
    "Italian Grand Prix (Monza)": {
        "top_5": ["ANT", "RUS", "VER", "NOR", "PIA"],
        "top_times": [81.1, 81.3, 81.6, 81.8, 82.2],
        "image": "ITA.png",
        "total_laps": 53,
        "dnfs": {"LEC": 1}
    },
    "Azerbaijan Grand Prix": {
        "top_5": ["RUS", "VER", "HAD", "LEC", "ANT"],
        "top_times": [98.0, 98.2, 98.8, 99.1, 99.5],
        "image": "BAK.png",
        "total_laps": 51,
        "dnfs": {}
    },
    "Bahrain Grand Prix (Malaysia)": {
        "top_5": ["VER", "ANT", "HAM", "LEC", "HAD"],
        "top_times": [94.8, 95.1, 95.4, 95.7, 96.0],
        "image": "MAL.png",
        "total_laps": 56,
        "dnfs": {"RUS": 50}  # Russell retired on Lap 50 due to Power Unit failure
    }
}

DRIVER_PROFILES = {
    "ANT": {"name": "K. Antonelli", "team": "Mercedes", "color": "#00D2BE"},
    "RUS": {"name": "G. Russell", "team": "Mercedes", "color": "#62FFF0"},
    "LEC": {"name": "C. Leclerc", "team": "Ferrari", "color": "#E80020"},
    "HAM": {"name": "L. Hamilton", "team": "Ferrari", "color": "#FF4D66"}
}

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("🏁 F1 Strategy Engine")
st.sidebar.subheader("2026 Season Analysis")

selected_race_name = st.sidebar.selectbox("Select 2026 Grand Prix", list(RACES_2026.keys()))
race_data = RACES_2026[selected_race_name]

# Stable track-specific pseudo-random seed
track_seed = abs(hash(selected_race_name)) % (2**32)
np.random.seed(track_seed)

tab_overview, tab_car_deepdive = st.tabs(["📊 Race Strategy Overview", "🏎️ Constructors Deep-Dive (4 Drivers)"])

# ==========================================
# TAB 1: RACE STRATEGY OVERVIEW
# ==========================================
with tab_overview:
    st.header(f"Strategy Overview: {selected_race_name}")
    st.caption("Pace distribution, tire deacy and the track layout.")
    
    col1, col2, col3 = st.columns([1.2, 1.3, 1.1])
    
    # 1. Pace Distribution Boxplot
    with col1:
        st.subheader("Top 5 Pace Distribution")
        fig1, ax1 = plt.subplots(figsize=(4.5, 4.2))
        
        top_5_drivers = race_data["top_5"]
        base_times = race_data["top_times"]
        
        box_data = [np.random.normal(b, 0.4 + idx*0.12, 40) for idx, b in enumerate(base_times)]
        
        bp = ax1.boxplot(box_data, patch_artist=True, tick_labels=top_5_drivers)
        colors = ['#E10600', '#00D2BE', '#FF8000', '#3671C6', '#229971']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
            
        ax1.set_ylabel("Lap Time (s)")
        ax1.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig1)

    # 2. Tyre Wear Scatterplot with Linear Regression
    with col2:
        st.subheader("Tyre Wear Linear Regression")
        fig2, ax2 = plt.subplots(figsize=(4.8, 4.2))
        
        laps = np.arange(1, 26).reshape(-1, 1)
        colors = ['#E10600', '#00D2BE', '#FF8000', '#3671C6', '#229971']
        
        for idx, (drv, base_t) in enumerate(zip(top_5_drivers, base_times)):
            decay_rate = 0.04 + idx * 0.03 + np.random.uniform(0.01, 0.03)
            noisy_laptimes = base_t + decay_rate * laps.ravel() + np.random.normal(0, 0.25, len(laps))
            
            model = LinearRegression()
            model.fit(laps, noisy_laptimes)
            predicted_laptimes = model.predict(laps)
            
            ax2.scatter(laps, noisy_laptimes, color=colors[idx], s=14, alpha=0.5)
            ax2.plot(laps, predicted_laptimes, color=colors[idx], label=f"{drv} ({model.coef_[0]:.3f}s/lap)", linewidth=1.8)
            
        ax2.set_xlabel("Tire Age (Laps)")
        ax2.set_ylabel("Lap Time (s)")
        ax2.legend(loc="upper left", fontsize=7)
        ax2.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig2)

    # 3. External Screenshot Track Layout Renderer
    with col3:
        st.subheader("Track Layout")
        img_filename = race_data["image"]
        img_path = os.path.join("assets", "tracks", img_filename)
        
        if os.path.exists(img_path):
            image = Image.open(img_path)
            st.image(image, caption=f"Layout: {selected_race_name}", use_container_width=True)
        else:
            st.warning(f"Image not found at path: `{img_path}`")

# ==========================================
# TAB 2: CONSTRUCTORS DEEP-DIVE
# ==========================================
with tab_car_deepdive:
    st.header(f"Multi-Driver Telemetry: {selected_race_name}")
    st.caption("Telemetry comparison across **Mercedes** (K. Antonelli & G. Russell) and **Ferrari** (C. Leclerc & L. Hamilton)")
    
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)
    
    # --------------------------------------
    # QUADRANT 1: TRACK & DRIVER RESPONSIVE SPEED ANALYSIS
    # --------------------------------------
    with row1_c1:
        st.markdown("### 1. SPEED ANALYSIS (SECTOR-WISE)")
        fig_spd, ax_spd = plt.subplots(figsize=(5.5, 2.8))
        dist = np.linspace(0, 100, 300)
        
        # Dynamically modulate cornering frequency and top speed per track layout
        track_freq = (track_seed % 5) + 3
        base_top_speed = 280 + (track_seed % 40)
        
        spd_ant = base_top_speed - 90 * (np.sin(dist / track_freq)**2) + 2 * np.cos(dist / 2)
        spd_rus = base_top_speed - 2 - 88 * (np.sin(dist / track_freq)**2) - 1.5 * np.sin(dist / 3)
        spd_lec = base_top_speed + 3 - 93 * (np.sin(dist / track_freq)**2) + 1.8 * np.sin(dist / 2)
        spd_ham = base_top_speed - 4 - 86 * (np.sin(dist / track_freq)**2) - 2 * np.cos(dist / 3)
        
        ax_spd.plot(dist, spd_ant, color=DRIVER_PROFILES["ANT"]["color"], label="ANT (Merc)", linewidth=1.5)
        ax_spd.plot(dist, spd_rus, color=DRIVER_PROFILES["RUS"]["color"], label="RUS (Merc)", linewidth=1.5, linestyle="--")
        ax_spd.plot(dist, spd_lec, color=DRIVER_PROFILES["LEC"]["color"], label="LEC (Fer)", linewidth=1.5)
        ax_spd.plot(dist, spd_ham, color=DRIVER_PROFILES["HAM"]["color"], label="HAM (Fer)", linewidth=1.5, linestyle="--")
        
        ax_spd.axvline(x=33, color="white", linestyle=":", alpha=0.5)
        ax_spd.axvline(x=66, color="white", linestyle=":", alpha=0.5)
        ax_spd.text(10, base_top_speed - 95, "SECTOR 1", color="white", fontsize=8)
        ax_spd.text(42, base_top_speed - 95, "SECTOR 2", color="white", fontsize=8)
        ax_spd.text(75, base_top_speed - 95, "SECTOR 3", color="white", fontsize=8)
        
        ax_spd.set_ylabel("Speed (KM/H)", fontsize=8)
        ax_spd.set_ylim(160, 340)
        ax_spd.legend(loc="lower right", fontsize=7)
        ax_spd.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig_spd)

    # --------------------------------------
    # QUADRANT 2: TYRE DEGRADATION REGRESSION
    # --------------------------------------
    with row1_c2:
        st.markdown("### 2. TYRE DEGRADATION ")
        fig_deg, ax_deg = plt.subplots(figsize=(5.5, 2.8))
        laps_stint = np.arange(1, 23).reshape(-1, 1)
        
        drivers_keys = ["ANT", "RUS", "LEC", "HAM"]
        base_deg_rates = [0.72, 0.81, 0.78, 0.88]
        
        for d_key, base_deg in zip(drivers_keys, base_deg_rates):
            noisy_grip = 100 - base_deg * laps_stint.ravel() + np.random.normal(0, 1.2, len(laps_stint))
            
            deg_model = LinearRegression()
            deg_model.fit(laps_stint, noisy_grip)
            pred_grip = deg_model.predict(laps_stint)
            
            ax_deg.scatter(laps_stint, noisy_grip, color=DRIVER_PROFILES[d_key]["color"], s=10, alpha=0.4)
            ax_deg.plot(laps_stint, pred_grip, color=DRIVER_PROFILES[d_key]["color"], label=f"{d_key}", linewidth=1.8)
        
        ax_deg.set_ylabel("Grip Level %", fontsize=8)
        ax_deg.set_xlabel("LAP", fontsize=8)
        ax_deg.set_ylim(70, 102)
        ax_deg.legend(loc="lower left", fontsize=7)
        ax_deg.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig_deg)

    # --------------------------------------
    # QUADRANT 3: TRACK EVOLUTION
    # --------------------------------------
    with row2_c1:
        st.markdown("### 3. TRACK EVOLUTION")
        fig_evo, ax_evo = plt.subplots(figsize=(5.5, 2.8))
        
        max_race_laps = race_data["total_laps"]
        laps_race = np.arange(1, max_race_laps + 1)
        
        evo_curve = 96.0 - (2.1 / max_race_laps) * laps_race + np.random.normal(0, 0.15, max_race_laps)
        ax_evo.plot(laps_race, evo_curve, color="#76FF03", linewidth=2.0)
        
        ax_evo.set_ylabel("Lap Time (s)", fontsize=8)
        ax_evo.set_xlabel("LAP", fontsize=8)
        ax_evo.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig_evo)

    # --------------------------------------
    # QUADRANT 4: LAP-BY-LAP COMPARISON (DNF AWARE)
    # --------------------------------------
    with row2_c2:
        st.markdown("### 4. LAP-BY-LAP COMPARISON")
        fig_cmp, ax_cmp = plt.subplots(figsize=(5.5, 2.8))
        
        max_race_laps = race_data["total_laps"]
        dnf_dict = race_data["dnfs"]
        
        drivers_keys = ["ANT", "RUS", "LEC", "HAM"]
        base_offsets = [0.0, 0.18, 0.05, 0.28]
        
        for d_key, offset in zip(drivers_keys, base_offsets):
            # Trim lap range if driver suffered a DNF
            if d_key in dnf_dict:
                d_laps_count = dnf_dict[d_key]
                if d_laps_count == 0:
                    continue  # Retired on Lap 0
            else:
                d_laps_count = max_race_laps
                
            d_laps = np.arange(1, d_laps_count + 1)
            pace_curve = (95.0 + offset) - 0.02 * d_laps + np.random.normal(0, 0.12, len(d_laps))
            
            line_style = "--" if d_key in ["RUS", "HAM"] else "-"
            ax_cmp.plot(d_laps, pace_curve, color=DRIVER_PROFILES[d_key]["color"], label=f"{d_key}", linewidth=1.5, linestyle=line_style)
            
            # Plot DNF retirement marker
            if d_key in dnf_dict and d_laps_count > 0:
                ax_cmp.scatter(d_laps_count, pace_curve[-1], color="red", marker="x", s=50, zorder=5)
                ax_cmp.text(d_laps_count + 0.5, pace_curve[-1], "DNF", color="red", fontsize=7, fontweight="bold")

        ax_cmp.set_ylabel("Lap Time (s)", fontsize=8)
        ax_cmp.set_xlabel("LAP", fontsize=8)
        ax_cmp.legend(loc="upper right", fontsize=7)
        ax_cmp.grid(True, linestyle=":", alpha=0.3)
        st.pyplot(fig_cmp)