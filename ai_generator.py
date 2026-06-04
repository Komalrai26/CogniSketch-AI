import streamlit as st
from PIL import Image
from io import BytesIO
import speech_recognition as sr
from api_handler import generate_ai_image

# ==============================================================================
# # COGNISKETCH AI SYSTEM CORE CONFIGURATIONS
# ==============================================================================
API_KEY = "sk-b6uqFWRWdJpWHXWmvZfla8o50mN5HsZztMDvUt1XDdGtFduM"

st.set_page_config(
    page_title="COGNISKETCH AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Initialize production runtime memory variables
if "prompt_context_buffer" not in st.session_state:
    st.session_state.prompt_context_buffer = ""
if "canvas_output_cache" not in st.session_state:
    st.session_state.canvas_output_cache = None
if "history_gallery" not in st.session_state:
    st.session_state.history_gallery = []
if "voice_telemetry" not in st.session_state:
    st.session_state.voice_telemetry = "🟢 VOICE ENGINE STANDBY // READY FOR INPUT"

# Global Preset Category Mapping Variables
PRESET_GROUPS = {
    "🤖 Figurine Models": [
        {"label": "Cybernetic Figurine", "prompt": "A crisp 35mm studio photography capture of an intricate cybernetic 1/7 scale action figurine model, glowing neon mechanical accents, high contrast studio lighting."},
        {"label": "Steampunk Mech", "prompt": "An industrial 1/7 scale brass mechanical figurine model, intricate gears, clockwork detailing, soft volumetric workbench light."},
    ],
    "🎨 Traditional & Classical Art": [
        {"label": "Indian Folk Art", "prompt": "Beautiful decorative Indian classical folk art style vector layout illustration, gold foil accents, vibrant canvas composition mandala elephant."},
        {"label": "Mughal Miniature", "prompt": "Fine detailed traditional Indian Mughal miniature painting style, opaque watercolor on paper, intricate borders."},
    ],
    "📸 Editorial Photography": [
        {"label": "Night-Flash Aesthetic", "prompt": "Raw editorial night-flash candid portrait photograph, 90s vintage film aesthetic, high contrast harsh shadows, grainy texturized look."},
        {"label": "35mm Cinematic Film", "prompt": "A warm cinematic 35mm film still of an atmospheric cyberpunk street alleyway, neon light reflections on wet pavement asphalt."}
    ]
}

# ==============================================================================
# # PREMIUM CONDENSED ZERO-VOID GRAPHICAL STYLING (CUSTOM CSS)
# ==============================================================================
st.markdown("""
    <style>
    /* Dark radial ambient studio backdrop layout mapping */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #0d0f22 0%, #030407 100%);
        color: #ffffff !important;
    }
    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        letter-spacing: 2px;
        margin-top: -5px;
        margin-bottom: 5px;
    }
    .engineer-badge {
        display: block;
        margin: 0 auto 25px auto;
        text-align: center;
        background: linear-gradient(90deg, rgba(236, 72, 153, 0.15) 0%, rgba(124, 58, 237, 0.15) 100%);
        border: 1px solid #ec4899;
        padding: 5px 18px;
        border-radius: 20px;
        width: fit-content;
        font-size: 0.82rem;
        font-weight: bold;
        color: #f472b6;
    }
    
    /* CRITICAL DESIGN CORRECTION: 
       Completely eliminated artificial fixed min-heights. 
       The panels now shrink dynamically to fit contents perfectly with NO top empty space!
    */
    .tight-workspace-card {
        background: rgba(10, 12, 22, 0.75);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        height: auto !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .active-glow-border {
        border: 1px solid #ec4899 !important;
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.15) !important;
    }
    .panel-header-label {
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
    }
    
    /* Interactive Automation Voice Capture Module Panel */
    .voice-hub-panel {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(21, 29, 54, 0.8) 100%);
        border: 2px solid #00f2fe;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15);
    }
    
    /* Native Hardware Microphone Button Element */
    .mic-btn-layout [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.4) !important;
    }
    
    /* Preset Option Selector button formatting rows */
    div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        font-size: 0.82rem !important;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background: rgba(236, 72, 153, 0.12) !important;
        border-color: #ec4899 !important;
        color: #f472b6 !important;
    }
    
    /* Main Generation Dispatch Pipeline Button styling */
    .execute-btn-wrapper [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        font-size: 1.05rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- PRESENTATION BRANDING LAYER ---
st.markdown('<h1 style="text-align: center; font-size: 3.5rem; font-weight: 900; letter-spacing: -1.5px; background: linear-gradient(90deg, #38bdf8 0%, #ec4899 50%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;">🧠 COGNISKETCH AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">ADVANCED VOICE-DRIVEN NEURAL SYNTHESIS WORKSPACE</div>', unsafe_allow_html=True)
st.markdown('<div class="engineer-badge">✨ DESIGNED & ENGINEERED BY KOMAL RAI ✨</div>', unsafe_allow_html=True)

# --- TOP LEVEL INTEGRATED CONTROLLER CARD (NATIVE DRIVER) ---
st.markdown('<div class="voice-hub-panel">', unsafe_allow_html=True)
st.markdown("### 🎙️ Direct Hardware Voice-to-Image Hub")
st.markdown("<p style='color:#94a3b8; font-size:0.92rem; margin-bottom:12px;'>Click below and speak naturally. The system tracks continuous sentences and generates images automatically.</p>", unsafe_allow_html=True)

st.markdown('<div class="mic-btn-layout">', unsafe_allow_html=True)
trigger_mic = st.button("🎙️ INITIALIZE VOICE-TO-IMAGE CAPTURE")
st.markdown('</div>', unsafe_allow_html=True)

# Hardware listening processing state logic
auto_fire_pipeline = False
if trigger_mic:
    st.session_state.voice_telemetry = "🔴 INITIALIZING AUDIO STREAM... Speak your prompt parameters clearly now."
    recognizer = sr.Recognizer()
    
   # --- CLOUD-SAFE VOICE CAPTURE ---
    if trigger_mic:
        import os
        # 1. Detect environment
        if "STREAMLIT_SERVER_PORT" in os.environ:
            st.info("🎙️ Hardware mic is unavailable in the cloud. Please use text input.")
        else:
            # 2. Only import and use hardware libraries on your local machine
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.session_state.voice_telemetry = "🔴 LISTENING..."
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5)
                    st.session_state.voice_telemetry = "⚙️ Transcribing..."
                    text = recognizer.recognize_google(audio)
                    st.session_state.prompt_context_buffer = text
                    st.session_state.voice_telemetry = "🟢 SUCCESS"
            except Exception as e:
                st.error(f"⚠️ Audio system error: {e}")

st.markdown(f'<div style="margin-top:12px; font-family:monospace; font-size:0.92rem; color:#38bdf8;">{st.session_state.voice_telemetry}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- WORKSPACE DISPLAY DUAL CORE SPLIT ---
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.markdown('<div class="tight-workspace-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header-label">📝 Execution Desk</div>', unsafe_allow_html=True)
    
    header_col, action_col = st.columns([3.2, 1])
    with header_col:
        st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:2px;'>Spoken parameters convert to layout prompts below.</p>", unsafe_allow_html=True)
    with action_col:
        if st.button("🔄 Reset Slate", use_container_width=True):
            st.session_state.prompt_context_buffer = ""
            st.session_state.canvas_output_cache = None
            st.session_state.voice_telemetry = "🟢 VOICE ENGINE STANDBY // READY FOR INPUT"
            st.rerun()

    # Dynamic text input field
    prompt_input_box = st.text_area(
        "Prompt Specification Data Layout",
        value=st.session_state.prompt_context_buffer,
        placeholder="Click 'INITIALIZE VOICE-TO-IMAGE CAPTURE' or select one of the templates down below...",
        height=120,
        label_visibility="collapsed"
    )
    st.session_state.prompt_context_buffer = prompt_input_box
    st.markdown('</div>', unsafe_allow_html=True)

    # --- INDEPENDENT PRESETS WORKSPACE CONTAINER ---
    st.markdown('<div class="tight-workspace-card">', unsafe_allow_html=True)
    st.markdown("##### ⚡ Global Options Preset Matrix Templates")
    
    for section_title, item_presets in PRESET_GROUPS.items():
        st.markdown(f"<p style='color:#f472b6; font-size:0.85rem; font-weight:bold; margin-bottom:4px; margin-top:8px;'>{section_title}</p>", unsafe_allow_html=True)
        preset_cols = st.columns(len(item_presets))
        for col_idx, item in enumerate(item_presets):
            with preset_cols[col_idx]:
                if st.button(item["label"], key=f"btn_{item['label'].lower().replace(' ', '_')}"):
                    st.session_state.prompt_context_buffer = item["prompt"]
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="execute-btn-wrapper">', unsafe_allow_html=True)
    manual_fire_pipeline = st.button("🚀 FIRE SYNTHESIS PIPELINE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Adds an active pink glow border ONLY when an image is rendered inside the canvas
    canvas_style = "tight-workspace-card active-glow-border" if st.session_state.canvas_output_cache else "tight-workspace-card"
    st.markdown(f'<div class="{canvas_style}">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header-label">🖼️ Realized Production Canvas</div>', unsafe_allow_html=True)
    
    # Process requests if manual or automatic voice triggers fire
    if manual_fire_pipeline or auto_fire_pipeline:
        if not prompt_input_box.strip():
            st.error("⚠️ Pipeline Error: Cannot compile an empty description.")
        else:
            with st.spinner("⏳ Rendering neural canvas layers across network channels..."):
                raw_image_data, fault_msg = generate_ai_image(prompt_input_box, API_KEY)
                if fault_msg:
                    st.error(fault_msg)
                elif raw_image_data:
                    compiled_canvas = Image.open(BytesIO(raw_image_data))
                    st.session_state.canvas_output_cache = compiled_canvas
                    if compiled_canvas not in st.session_state.history_gallery:
                        st.session_state.history_gallery.insert(0, compiled_canvas)
                    st.success("🎉 Interface Pipeline Rendered Successfully!")
                    st.rerun()

    if st.session_state.canvas_output_cache is not None:
        st.image(st.session_state.canvas_output_cache, use_container_width=True)
        
        image_stream = BytesIO()
        st.session_state.canvas_output_cache.save(image_stream, format="PNG")
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 EXPORT MASTERPIECE RENDER LAYOUT",
            data=image_stream.getvalue(),
            file_name="cognisketch_render.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        # A lightweight message container that naturally collapses when empty
        st.info("🌌 Awaiting instructions. Initialize the voice capture module or template presets to synthesize display graphics.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORE HISTORY FOOTER STRIP ROWS ---
st.markdown("<br>### 🗂️ Active Studio Production History Gallery", unsafe_allow_html=True)
if st.session_state.history_gallery:
    gallery_slots = st.columns(6)
    for idx, image_node in enumerate(st.session_state.history_gallery[:6]):
        with gallery_slots[idx]:
            st.image(image_node, use_container_width=True)
else:
    st.markdown("<p style='color:#4b5563; font-style:italic;'>Dynamic workspace history gallery strip is currently empty.</p>", unsafe_allow_html=True)
