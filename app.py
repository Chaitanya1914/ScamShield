"""
ScamShield — State Cyber Police Threat Intelligence & Omnichannel Active Defence Portal.

This Streamlit application provides an authoritative GovTech portal interface for detecting,
analyzing, and countering digital fraud, social engineering, and cyber threats across India.

Features:
1. GovTech State Cyber Police Styling: White/Blue aesthetic, high contrast, official branding.
2. Omnichannel Input System (R1):
   - SMS / Email text paste
   - WhatsApp Screenshot upload via direct Gemini Multimodal vision (Zero OCR / No Tesseract)
   - Simulate Live Threat dynamically loaded from the Hinglish dataset
3. Sentinel Mode Dashboard (R2 & R4):
   - High-contrast Risk Level Badge & AI Confidence Score
   - Scam Category & Recommended Action Advisory
   - Plain-Language Red Flags & Psychological Tactics Breakdown
   - Extracted Scammer Identifiers (Phone, UPI, URLs)
   - Accessible In-Memory Hindi Voice Advisory (gTTS via BytesIO)
   - State Cyber Police Law Enforcement Alert Banner with #NCRP-XXXXXX reference ID
4. Strike Mode Offensive Honeypot (R3 & User Update):
   - Interactive multi-turn chat bubbles with Rahul (21yo confused college student)
   - Memory preservation via st.session_state.strike_chat_history
   - Quick test triggers and session reset controls
5. Graceful API Key Management & Offline Mode (R5):
   - Non-crashing operation with informative status indicators
   - Deterministic offline intelligence fallback
"""

import csv
import hashlib
import io
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
from PIL import Image

from backend import (
    analyze_threat,
    generate_voice_warning,
    log_threat,
    generate_honeypot_reply,
    load_sample_threats,
    THREAT_LOG_PATH,
    DATASET_PATH,
)

# ===========================================================================
# 1. Page Configuration
# ===========================================================================

st.set_page_config(
    page_title="ScamShield — State Cyber Police Active Defence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===========================================================================
# 2. GovTech State Cyber Police Portal Styling (White & Blue Theme)
# ===========================================================================

st.markdown("""
<style>
    /* Global Background and Typography */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    }

    /* Top Official Government Portal Banner */
    .gov-header {
        background: linear-gradient(135deg, #0b3b60 0%, #07263e 100%);
        color: #ffffff;
        padding: 22px 28px;
        border-radius: 8px;
        border-bottom: 4px solid #f97316; /* Indian National Saffron Trim */
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .gov-badge-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }
    .gov-badge-text {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #f97316;
        background: rgba(249, 115, 22, 0.12);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }
    .gov-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
        margin: 0;
        line-height: 1.2;
    }
    .gov-subtitle {
        font-size: 14px;
        color: #cbd5e1;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* High-Contrast GovTech Threat Alert Cards */
    .threat-card-high {
        background-color: #fef2f2;
        border: 1.5px solid #dc2626;
        border-left: 8px solid #dc2626;
        border-radius: 8px;
        padding: 18px 22px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(220, 38, 38, 0.08);
    }
    .threat-card-medium {
        background-color: #fffbeb;
        border: 1.5px solid #d97706;
        border-left: 8px solid #d97706;
        border-radius: 8px;
        padding: 18px 22px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(217, 119, 6, 0.08);
    }
    .threat-card-low {
        background-color: #f0fdf4;
        border: 1.5px solid #16a34a;
        border-left: 8px solid #16a34a;
        border-radius: 8px;
        padding: 18px 22px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(22, 163, 74, 0.08);
    }

    .threat-card-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .threat-card-sub {
        font-size: 14px;
        font-weight: 500;
    }

    /* Law Enforcement NCRP Incident Banner */
    .ncrp-dispatch-banner {
        background-color: #eff6ff;
        border: 1.5px solid #2563eb;
        border-left: 8px solid #1d4ed8;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.08);
    }

    /* Accessible Hindi Audio Advisory Card */
    .hindi-audio-card {
        background-color: #f5f3ff;
        border: 1.5px solid #7c3aed;
        border-left: 8px solid #6d28d9;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0;
    }

    /* Clean Card Container */
    .gov-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    /* Metric & Tag Chips */
    .ioc-chip {
        display: inline-block;
        background-color: #f1f5f9;
        color: #0f172a;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
    }
    .tactic-chip {
        display: inline-block;
        background-color: #fef3c7;
        color: #92400e;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 6px;
        border: 1px solid #fde68a;
    }

    /* Sidebar Clean Government Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Streamlit Tab High-Contrast Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# 3. Helper Functions
# ===========================================================================

def get_threat_log_metrics() -> Tuple[int, List[List[str]]]:
    """
    Safely reads threat_log.csv and returns total threats logged and recent records.

    Returns:
        Tuple[int, List[List[str]]]: Count of logged indicators and list of rows.
    """
    if not THREAT_LOG_PATH.exists():
        return 0, []
    try:
        with open(THREAT_LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return 0, []
            data_rows = rows[1:]
            return len(data_rows), data_rows
    except Exception:
        return 0, []


def generate_ncrp_reference_id(content: Any) -> str:
    """
    Generates a deterministic yet unique reference ID for law enforcement tracking.

    Args:
        content: Message text or identifier string.

    Returns:
        str: Formatted incident ID, e.g. '#NCRP-2026-8942'.
    """
    seed = f"{content}_{datetime.now().strftime('%Y%m%d%H%M')}"
    h = hashlib.md5(seed.encode("utf-8", errors="ignore")).hexdigest()[:6].upper()
    return f"#NCRP-2026-{h}"


@st.cache_data(show_spinner=False)
def get_cached_sample_threats() -> List[Dict[str, str]]:
    """
    Loads and caches sample scam messages from the Hinglish dataset for live threat simulation.

    Returns:
        List[Dict[str, str]]: Curated list of distinct scam scenarios.
    """
    return load_sample_threats(csv_path=DATASET_PATH, n=8)


# ===========================================================================
# 4. Session State Management
# ===========================================================================

if "threat_assessment" not in st.session_state:
    st.session_state.threat_assessment = None

if "active_channel" not in st.session_state:
    st.session_state.active_channel = "SMS / Email Text"

if "active_text_content" not in st.session_state:
    st.session_state.active_text_content = ""

if "strike_chat_history" not in st.session_state:
    st.session_state.strike_chat_history = []

if "logged_incident_id" not in st.session_state:
    st.session_state.logged_incident_id = None

if "logged_iocs" not in st.session_state:
    st.session_state.logged_iocs = []


# ===========================================================================
# 5. Sidebar: Authentication, Protocols & System Registry
# ===========================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="font-size: 40px; margin-bottom: 4px;">🛡️</div>
        <div style="font-size: 16px; font-weight: 800; color: #0b3b60; letter-spacing: -0.3px;">
            STATE CYBER CRIME CELL
        </div>
        <div style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px;">
            National Cyber Crime Portal (NCRP)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### ⚙️ System Configuration")
    api_key_input = st.text_input(
        "🔑 Google Gemini API Key",
        type="password",
        help="Enter your free API key from Google AI Studio (aistudio.google.com). If empty, the system operates in deterministic offline mock mode.",
    )
    api_key = api_key_input.strip()

    if api_key:
        st.success("🟢 **Live Gemini API Connected**")
    else:
        st.info("🟡 **Offline Intelligence Active**\n\n*Running in deterministic offline mode for automated tests and demonstrations. Enter an API key for live Gemini 2.0 multimodal analysis.*")

    st.divider()

    st.markdown("### 🎯 Operating Protocol")
    mode_selection = st.radio(
        "Select Active Protocol:",
        [
            "🛡️ Sentinel Mode (Analysis & Hindi Voice Alert)",
            "⚔️ Strike Mode (Rahul Honeypot Tarpit)",
            "🛡️ + ⚔️ Dual Active Defence",
        ],
        index=0,
        help="Sentinel Mode provides visual threat breakdown and accessible Hindi voice warning.\nStrike Mode engages scammers with an offensive Rahul honeypot tarpit.",
    )

    st.divider()

    st.markdown("### 📊 State Threat Database")
    threat_count, threat_rows = get_threat_log_metrics()
    st.metric("Total Threats Logged (NCRP)", threat_count)

    if threat_count > 0:
        try:
            with open(THREAT_LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
                csv_bytes = f.read().encode("utf-8")
            st.download_button(
                label="📥 Export Threat Log (CSV)",
                data=csv_bytes,
                file_name="state_cyber_police_threat_log.csv",
                mime="text/csv",
                use_container_width=True,
            )
        except Exception:
            pass

    st.divider()

    st.markdown("""
    <div style="background-color: #f1f5f9; border-radius: 6px; padding: 12px; font-size: 12px; color: #334155; line-height: 1.5;">
        <strong>🚨 National Cyber Helpline:</strong> <span style="font-size: 14px; font-weight: 800; color: #dc2626;">1930</span><br>
        <strong>🌐 Citizen Portal:</strong> <a href="https://cybercrime.gov.in" target="_blank" style="color: #2563eb; text-decoration: none;">cybercrime.gov.in</a><br>
        <strong>⚖️ Statutory Alignment:</strong> IT Act, 2000 & CERT-In Guidelines
    </div>
    """, unsafe_allow_html=True)


# ===========================================================================
# 6. Main Portal Header
# ===========================================================================

st.markdown("""
<div class="gov-header">
    <div class="gov-badge-row">
        <span class="gov-badge-text">Ministry of Home Affairs Alignment</span>
        <span style="color: #94a3b8; font-size: 12px;">•</span>
        <span style="color: #cbd5e1; font-size: 12px; font-weight: 600;">State Cyber Police Special Task Force</span>
    </div>
    <div class="gov-title">ScamShield — AI Omnichannel Active Threat Interceptor</div>
    <div class="gov-subtitle">
        Real-time artificial intelligence threat detection, multimodal image forensics, accessible Hindi voice advisories,
        and offensive honeypot tarpitting against digital arrest, KYC fraud, and extortion scams.
    </div>
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# 7. Omnichannel Threat Ingestion (R1)
# ===========================================================================

st.markdown("### 📥 Omnichannel Threat Ingestion")

tab_text, tab_image, tab_simulate = st.tabs([
    "📝 SMS / Email Text Analysis",
    "📸 WhatsApp Screenshot Forensics (Multimodal Vision)",
    "⚡ Simulate Live Threat (Hinglish Dataset)",
])

# ---- Tab 1: SMS / Email Text Analysis ----
with tab_text:
    st.markdown("##### Paste Suspicious SMS, WhatsApp Text, or Email:")
    text_input = st.text_area(
        "Message Content",
        height=130,
        placeholder="Example: Ji namaskar Aapka SBI bank account 2 ghante mein block ho jayega KYC pending hone ke karan. Abhi apna OTP share kijiye is number par: 9876543210 ya fir is link par click karein: http://sbi-kyc-update.com",
        label_visibility="collapsed",
    )
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.caption("Supports English, Hindi, and code-mixed Hinglish smishing messages.")
    with col_t2:
        btn_analyze_text = st.button("🔍 Analyze Text Threat", type="primary", use_container_width=True, key="btn_analyze_text")

    if btn_analyze_text:
        if not text_input.strip():
            st.warning("⚠️ Please paste or type a message to analyze.")
        else:
            with st.spinner("🔍 Analyzing threat vectors with AI intelligence..."):
                assessment = analyze_threat(text=text_input.strip(), api_key=api_key)
                st.session_state.threat_assessment = assessment
                st.session_state.active_channel = "SMS / Email Text"
                st.session_state.active_text_content = text_input.strip()

                if assessment.get("risk_level") in ("High", "Medium"):
                    inc_id = generate_ncrp_reference_id(text_input)
                    st.session_state.logged_incident_id = inc_id
                    logged = log_threat(assessment, source_channel="SMS / Email Text")
                    st.session_state.logged_iocs = list(logged)
                else:
                    st.session_state.logged_incident_id = None
                    st.session_state.logged_iocs = []

                # Seed Strike Mode honeypot with initial message
                st.session_state.strike_chat_history = [
                    {"role": "user", "content": text_input.strip()}
                ]
                rahul_opening = generate_honeypot_reply(text_input.strip(), api_key=api_key)
                st.session_state.strike_chat_history.append(
                    {"role": "assistant", "content": rahul_opening}
                )

# ---- Tab 2: WhatsApp Screenshot Forensics ----
with tab_image:
    st.info(
        "🔬 **Direct Gemini Multimodal Vision Active**: Screenshot images are processed natively by multimodal neural vision. "
        "Strictly **zero external OCR software (No Tesseract)** required."
    )
    st.markdown("##### Upload WhatsApp Screenshot (.png, .jpg, .jpeg):")
    uploaded_image = st.file_uploader(
        "Upload WhatsApp Screenshot",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    if uploaded_image is not None:
        try:
            uploaded_image.seek(0)
            preview_img = Image.open(uploaded_image)
            st.image(preview_img, caption=f"Uploaded Screenshot: {uploaded_image.name}", use_container_width=False, width=380)
        except Exception as e:
            st.error(f"Could not render image preview: {e}")

        btn_analyze_img = st.button("🔍 Scan Screenshot with Multimodal AI", type="primary", use_container_width=True, key="btn_analyze_img")

        if btn_analyze_img:
            with st.spinner("🔎 Executing Gemini Multimodal Visual Forensics..."):
                uploaded_image.seek(0)
                assessment = analyze_threat(image=uploaded_image, api_key=api_key)
                st.session_state.threat_assessment = assessment
                st.session_state.active_channel = f"WhatsApp Screenshot ({uploaded_image.name})"
                st.session_state.active_text_content = f"[Screenshot Analysis: {uploaded_image.name}] {assessment.get('scam_category')}"

                if assessment.get("risk_level") in ("High", "Medium"):
                    inc_id = generate_ncrp_reference_id(uploaded_image.name)
                    st.session_state.logged_incident_id = inc_id
                    logged = log_threat(assessment, source_channel="WhatsApp Screenshot")
                    st.session_state.logged_iocs = list(logged)
                else:
                    st.session_state.logged_incident_id = None
                    st.session_state.logged_iocs = []

                # Seed Strike Mode honeypot with category/red flag context
                seed_msg = (
                    f"Message intercepted from screenshot ({assessment.get('scam_category')}): "
                    f"{assessment.get('recommended_action')}"
                )
                st.session_state.strike_chat_history = [
                    {"role": "user", "content": seed_msg}
                ]
                rahul_opening = generate_honeypot_reply(seed_msg, api_key=api_key)
                st.session_state.strike_chat_history.append(
                    {"role": "assistant", "content": rahul_opening}
                )

# ---- Tab 3: Simulate Live Threat ----
with tab_simulate:
    st.markdown("##### Intercept Real Scam Threats from Indian Cyber Crime Dataset:")
    sample_threats = get_cached_sample_threats()

    sample_options = [
        f"🚨 {item['category']} — [{item.get('source', 'Dataset')}]"
        for item in sample_threats
    ]

    selected_idx = st.selectbox(
        "Choose Live Threat Scenario:",
        range(len(sample_threats)),
        format_func=lambda i: sample_options[i],
    )

    current_sample = sample_threats[selected_idx]

    st.markdown(f"**Threat Category:** `{current_sample['category']}`")
    st.code(current_sample["message"], language=None)

    btn_analyze_sim = st.button("⚡ Intercept & Analyze Threat", type="primary", use_container_width=True, key="btn_analyze_sim")

    if btn_analyze_sim:
        with st.spinner("⚡ Intercepting live threat and scanning with AI..."):
            assessment = analyze_threat(text=current_sample["message"], api_key=api_key)
            st.session_state.threat_assessment = assessment
            st.session_state.active_channel = f"Simulator ({current_sample['category']})"
            st.session_state.active_text_content = current_sample["message"]

            if assessment.get("risk_level") in ("High", "Medium"):
                inc_id = generate_ncrp_reference_id(current_sample["message"])
                st.session_state.logged_incident_id = inc_id
                logged = log_threat(assessment, source_channel=f"Simulator ({current_sample['category']})")
                st.session_state.logged_iocs = list(logged)
            else:
                st.session_state.logged_incident_id = None
                st.session_state.logged_iocs = []

            # Seed Strike Mode
            st.session_state.strike_chat_history = [
                {"role": "user", "content": current_sample["message"]}
            ]
            rahul_opening = generate_honeypot_reply(current_sample["message"], api_key=api_key)
            st.session_state.strike_chat_history.append(
                {"role": "assistant", "content": rahul_opening}
            )


# ===========================================================================
# 8. Sentinel Mode: Threat Assessment & Incident Dispatch (R2 & R4)
# ===========================================================================

is_sentinel_active = "Sentinel" in mode_selection or "Dual" in mode_selection
is_strike_active = "Strike" in mode_selection or "Dual" in mode_selection

if st.session_state.threat_assessment and is_sentinel_active:
    st.divider()
    st.markdown("## 🛡️ Sentinel Mode — Threat Assessment & Incident Dispatch")

    assessment = st.session_state.threat_assessment
    risk_level = assessment.get("risk_level", "Medium")
    confidence = assessment.get("confidence", 85)
    category = assessment.get("scam_category", "Suspicious Activity")
    channel = st.session_state.active_channel

    # 1. Prominent Risk Level Badge
    if risk_level == "High":
        st.markdown(f"""
        <div class="threat-card-high">
            <div class="threat-card-title" style="color: #b91c1c;">
                🚨 HIGH RISK THREAT DETECTED — {category}
            </div>
            <div class="threat-card-sub" style="color: #7f1d1d;">
                AI Confidence: <strong>{confidence}%</strong> | Threat Category: <strong>{category}</strong> | Source Vector: <strong>{channel}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "Medium":
        st.markdown(f"""
        <div class="threat-card-medium">
            <div class="threat-card-title" style="color: #b45309;">
                ⚠️ MEDIUM RISK — SUSPICIOUS ACTIVITY DETECTED
            </div>
            <div class="threat-card-sub" style="color: #78350f;">
                AI Confidence: <strong>{confidence}%</strong> | Threat Category: <strong>{category}</strong> | Source Vector: <strong>{channel}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="threat-card-low">
            <div class="threat-card-title" style="color: #15803d;">
                ✅ LOW RISK — LIKELY SAFE / BENIGN COMMUNICATION
            </div>
            <div class="threat-card-sub" style="color: #14532d;">
                AI Confidence: <strong>{confidence}%</strong> | Verification: <strong>No malicious indicators identified</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. GovTech Law Enforcement Alert Banner (R4)
    if risk_level in ("High", "Medium") and st.session_state.logged_incident_id:
        inc_id = st.session_state.logged_incident_id
        iocs = st.session_state.logged_iocs or ["Threat signature logged"]
        ioc_chips_html = "".join([f'<span class="ioc-chip">{item}</span>' for item in iocs[:5]])
        st.markdown(f"""
        <div class="ncrp-dispatch-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 15px; font-weight: 800; color: #1e3a8a;">
                    🚨 STATE CYBER POLICE — THREAT INTELLIGENCE LOGGED
                </span>
                <span style="background: #1e40af; color: #ffffff; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">
                    {inc_id}
                </span>
            </div>
            <div style="font-size: 13px; color: #1e293b; line-height: 1.4;">
                This threat incident has been automatically recorded to the <strong>State Cyber Police Threat Database (threat_log.csv)</strong>
                in alignment with National Cyber Crime Reporting Portal (NCRP / I4C) directives.
            </div>
            <div style="margin-top: 8px; font-size: 12px; color: #334155;">
                <strong>Dispatched Indicators of Compromise ({len(iocs)}):</strong> {ioc_chips_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Key Metrics Grid
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Risk Level", risk_level)
    col_m2.metric("AI Confidence", f"{confidence}%")
    col_m3.metric("Scam Category", category)
    col_m4.metric("Input Channel", channel.split("(")[0].strip())

    # 4. Recommended Action Advisory
    action_text = assessment.get("recommended_action") or assessment.get("recommendation", "Exercise caution.")
    st.markdown("#### 🛡️ Recommended Citizen Action:")
    st.info(f"👉 **{action_text}**")

    # 5. Red Flags & Psychological Tactics Breakdown
    col_flags, col_tactics = st.columns(2)

    with col_flags:
        st.markdown("#### 🚩 Red Flags Detected:")
        red_flags = assessment.get("red_flags", [])
        if red_flags:
            for flag in red_flags:
                st.error(f"🔴 {flag}")
        else:
            st.success("No critical fraud red flags identified in this message.")

    with col_tactics:
        st.markdown("#### 🧠 Psychological Manipulation Tactics:")
        tactics = assessment.get("psychological_tactics", [])
        if tactics:
            tactics_html = "".join([f'<span class="tactic-chip">⚡ {t}</span>' for t in tactics])
            st.markdown(tactics_html, unsafe_allow_html=True)
        else:
            st.caption("No coercive psychological manipulation tactics detected.")

    # 6. Extracted Scammer Identifiers (IoCs)
    st.markdown("#### 🔗 Extracted Indicators of Compromise (IoCs):")
    extracted_data = assessment.get("extracted_identifiers") or assessment.get("extracted_threat_data") or {}
    phones = extracted_data.get("phone_numbers", [])
    upis = extracted_data.get("upi_ids", [])
    urls = extracted_data.get("urls", [])

    col_p, col_u, col_l = st.columns(3)
    with col_p:
        st.markdown("**📞 Phone Numbers:**")
        if phones:
            for p in phones:
                st.code(p, language=None)
        else:
            st.caption("None extracted")

    with col_u:
        st.markdown("**💳 UPI Payment IDs (VPAs):**")
        if upis:
            for u in upis:
                st.code(u, language=None)
        else:
            st.caption("None extracted")

    with col_l:
        st.markdown("**🔗 Suspicious URLs & Links:**")
        if urls:
            for link in urls:
                st.code(link, language=None)
        else:
            st.caption("None extracted")

    # 7. Accessible Hindi Voice Advisory (In-Memory gTTS Audio)
    hindi_text = assessment.get("hindi_warning_text") or assessment.get("warning_message_hindi")
    if hindi_text and risk_level in ("High", "Medium"):
        st.markdown("#### 🔊 Accessible Voice Warning (Hindi Audio Advisory):")
        st.markdown(f"""
        <div class="hindi-audio-card">
            <div style="font-size: 13px; font-weight: 700; color: #6d28d9; margin-bottom: 4px;">
                📢 HINDI AUDIO ADVISORY FOR CITIZENS & ELDERLY
            </div>
            <div style="font-size: 16px; font-weight: 600; color: #3b0764; margin-bottom: 8px;">
                "{hindi_text}"
            </div>
            <div style="font-size: 11px; color: #7c3aed;">
                Audio is synthesized in-memory via gTTS (BytesIO stream) for accessible warning across regional demographics.
            </div>
        </div>
        """, unsafe_allow_html=True)

        audio_stream = generate_voice_warning(assessment)
        if audio_stream is not None:
            st.audio(audio_stream.getvalue(), format="audio/mp3", autoplay=True)
        else:
            st.info(f"🗣️ Voice synthesis unavailable offline. Devanagari advisory: {hindi_text}")


# ===========================================================================
# 9. Strike Mode: Rahul Honeypot Counter-Tarpit (R3 & User Update)
# ===========================================================================

if is_strike_active:
    st.divider()
    st.markdown("## ⚔️ Strike Mode — Offensive Rahul Honeypot Counter-Tarpit")
    st.markdown("""
    <div style="background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 14px; font-size: 13px; color: #334155; line-height: 1.5;">
        <strong>Active Persona:</strong> 🧑‍🎓 <strong>Rahul (21yo College Student)</strong><br>
        <em>A naive, easily confused B.Tech student stressed about semester exams, attendance, and hostel fees, using an old phone with a cracked screen.
        Rahul stalls scammers with circular Hinglish questions, exam panic, and broken phone excuses while revealing strictly ZERO real credentials.</em>
    </div>
    """, unsafe_allow_html=True)

    col_act1, col_act2 = st.columns([4, 1])
    with col_act2:
        if st.button("🔄 Reset Honeypot", key="btn_reset_strike", use_container_width=True):
            st.session_state.strike_chat_history = []
            st.rerun()

    # Empty State: Prompt user or allow quick test
    if not st.session_state.strike_chat_history:
        st.info("💡 Intercept a threat above or select a quick scam scenario below to activate Rahul's honeypot trap:")
        q1, q2, q3 = st.columns(3)
        if q1.button("⚡ Test KYC Scam Threat", use_container_width=True):
            scam_msg = "Ji namaskar Aapka SBI account 2 ghante mein block ho jayega KYC pending hone ke karan. Abhi OTP share karein."
            st.session_state.strike_chat_history = [{"role": "user", "content": scam_msg}]
            with st.spinner("🧑‍🎓 Rahul is replying..."):
                reply = generate_honeypot_reply(scam_msg, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if q2.button("⚡ Test KBC Lottery Scam", use_container_width=True):
            scam_msg = "CONGRATULATIONS!! Aapne KBC Season 15 mein Rs 25,00,000 ka lottery jeeta hai! Claim karne ke liye turant call karein."
            st.session_state.strike_chat_history = [{"role": "user", "content": scam_msg}]
            with st.spinner("🧑‍🎓 Rahul is replying..."):
                reply = generate_honeypot_reply(scam_msg, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if q3.button("⚡ Test Electricity Power Cut", use_container_width=True):
            scam_msg = "Dear Customer, Your electricity connection will be disconnected tonight at 9:30 PM due to pending bill payment. Contact officer now."
            st.session_state.strike_chat_history = [{"role": "user", "content": scam_msg}]
            with st.spinner("🧑‍🎓 Rahul is replying..."):
                reply = generate_honeypot_reply(scam_msg, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    # Render Conversation Turns
    for msg in st.session_state.strike_chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🦹"):
                st.markdown(f"**Scammer:** {msg['content']}")
        else:
            with st.chat_message("assistant", avatar="🧑‍🎓"):
                st.markdown(f"**Rahul:** {msg['content']}")

    # Quick Scammer Follow-up Actions for Fast Testing
    if st.session_state.strike_chat_history:
        st.markdown("##### ⚡ Quick Scammer Pressure Responses (Click to test Rahul's stalling):")
        qc1, qc2, qc3 = st.columns(3)

        if qc1.button("🚨 'Jaldi OTP batao varna account block hoga!'", key="quick_otp", use_container_width=True):
            followup = "Arre jaldi OTP batao varna account abhi block ho jayega! Time mat kharab karo!"
            st.session_state.strike_chat_history.append({"role": "user", "content": followup})
            with st.spinner("🧑‍🎓 Rahul is stalling..."):
                reply = generate_honeypot_reply(st.session_state.strike_chat_history, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if qc2.button("🚔 'Crime Branch se bol raha hoon, police aa rahi hai!'", key="quick_police", use_container_width=True):
            followup = "Main Crime Branch officer bol raha hoon! Agar turant baat nahi suni toh police jeep bhej raha hoon!"
            st.session_state.strike_chat_history.append({"role": "user", "content": followup})
            with st.spinner("🧑‍🎓 Rahul is stalling..."):
                reply = generate_honeypot_reply(st.session_state.strike_chat_history, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if qc3.button("💸 'Pehle ₹500 fee transfer karo is UPI pe!'", key="quick_fee", use_container_width=True):
            followup = "Lottery lene ke liye pehle ₹500 file processing fee transfer karo officer@upi pe tabhi paise aayenge!"
            st.session_state.strike_chat_history.append({"role": "user", "content": followup})
            with st.spinner("🧑‍🎓 Rahul is stalling..."):
                reply = generate_honeypot_reply(st.session_state.strike_chat_history, api_key=api_key)
            st.session_state.strike_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    # Interactive Chat Input for Multi-Turn Stalling
    scammer_response = st.chat_input("Enter scammer's response to continue stalling Rahul...")
    if scammer_response and scammer_response.strip():
        st.session_state.strike_chat_history.append({"role": "user", "content": scammer_response.strip()})
        with st.spinner("🧑‍🎓 Rahul is typing a confused reply..."):
            rahul_reply = generate_honeypot_reply(st.session_state.strike_chat_history, api_key=api_key)
        st.session_state.strike_chat_history.append({"role": "assistant", "content": rahul_reply})
        st.rerun()
