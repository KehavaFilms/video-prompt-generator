import streamlit as st
import os
import json
from google import genai

# పేజీ కాన్ఫిగరేషన్
st.set_page_config(
    page_title="Next-Gen AI Prompt Studio (GPT-5.6 Luna Edition)",
    layout="wide",
    page_icon="⚡"
)

st.title("⚡ Next-Gen AI Prompt Studio")

# 1. Sidebar సెట్టింగ్స్
with st.sidebar:
    st.header("⚙️ స్టూడియో సెట్టింగ్స్")
    master_mode = st.radio(
        "టూల్ ఎంచుకోండి:",
        [
            "🎥 Multi-Category Video Studio (GPT-5.6 Luna / Veo 3.1 / Omni 1.1)",
            "🧠 Elite Reasoning LLM Studio (GPT-5.6 Luna / Claude 3.7 / o3)"
        ]
    )
    
    st.markdown("---")
    active_engine = st.selectbox(
        "Gemini Processing Engine:",
        ["gemini-3.1-pro-preview", "gemini-3.6-flash", "gemini-3-flash-preview"],
        help="డీప్ క్వాలిటీ కోసం 3.1 Pro వాడండి, స్పీడ్ కోసం Flash వాడండి."
    )
    
    api_key = st.text_input(
        "Gemini API Key:",
        type="password",
        help="aistudio.google.com నుండి తెచ్చిన ఉచిత కీ ఇవ్వండి."
    )
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key


# ఫెయిల్‌సేఫ్ జనరేషన్ ఫంక్షన్
def generate_with_fallback(client, contents, sys_instruction, is_json=False):
    models_to_try = [active_engine, "gemini-3.6-flash", "gemini-3-flash-preview"]
    models_to_try = list(dict.fromkeys(models_to_try))
    
    config = {"system_instruction": sys_instruction}
    if is_json:
        config["response_mime_type"] = "application/json"
        
    last_error = None
    for model_name in models_to_try:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
            return res.text, model_name
        except Exception as e:
            last_error = e
            continue
    raise last_error


# -------------------------------------------------------------
# మోడ్ 1: వీడియో ప్రాంప్ట్ ఇంజిన్ (GPT-5.6 Luna చేర్చబడింది)
# -------------------------------------------------------------
if master_mode == "🎥 Multi-Category Video Studio (GPT-5.6 Luna / Veo 3.1 / Omni 1.1)":
    st.subheader("🎥 Multi-Category AI Video Prompt Generator")

    video_engine = st.selectbox(
        "టార్గెట్ వీడియో AI మోడల్:",
        [
            "GPT-5.6 Luna (Multimodal Video Director & Narrative Sync)",
            "Google Flow (Veo 3.1 Quality with Native Audio)",
            "Google Flow (Veo 3.1 Fast / Omni 1.1)",
            "Runway Gen-3 Alpha",
            "OpenAI Sora Pro",
            "Kling AI 1.5"
        ]
    )

    video_category = st.selectbox(
        "వీడియో కేటగిరీ ఎంచుకోండి:",
        [
            "🧸 3D కార్టూన్ / యానిమేషన్ (Pixar / Ghibli Style)",
            "🎬 సినిమాటిక్ & మూవీ షాట్స్ (Hollywood Ultra-Realism)",
            "🛍️ ప్రొడక్ట్ యాడ్స్ & కమర్షియల్స్ (Commercial Studio)",
            "📱 వైరల్ రీల్స్ & యూట్యూబ్ షార్ట్స్ (High-Hook Shorts)"
        ]
    )

    if "కార్టూన్" in video_category:
        style_spec = st.selectbox("యానిమేషన్ స్టైల్:", [
            "Pixar 3D Render (Subsurface scattering, expressive physics, bright Octane look)",
            "Studio Ghibli Anime (Lush hand-drawn nature, magical watercolor tones)",
            "Tactile Claymation (Stop-motion clay texture, organic imperfections)",
            "Stylized Disney 3D (Clean character topology, vibrant rim lighting)"
        ])
    elif "సినిమాటిక్" in video_category:
        style_spec = st.selectbox("సినిమాటిక్ విజన్:", [
            "Hyper-Realistic ARRI 8K (Anamorphic lens flares, shallow depth, 35mm grain)",
            "Sci-Fi Neo-Cyberpunk (Wet asphalt, volumetric smoke, moody color grade)",
            "Dark Gothic / Thriller (Chiaroscuro shadows, high contrast, desaturated)",
            "Epic IMAX Fantasy (Golden hour atmospheric haze, grand establishing scale)"
        ])
    elif "యాడ్స్" in video_category:
        style_spec = st.selectbox("యాడ్ & కమర్షియల్ స్టైల్:", [
            "Luxury Product Cinematic (1000fps macro, soft studio lighting, water beads)",
            "Apple-style Tech Aesthetic (Minimalist pure studio, floating exploded view)",
            "Dynamic Beverage Splash (Hyper-detailed fluid dynamics, condensation)",
            "High-Street Fashion Editorial (Punchy high-contrast shadows, modern aesthetic)"
        ])
    else:
        style_spec = st.selectbox("రీల్స్ హుక్ & వైబ్:", [
            "Instant Shock/Curiosity Hook (Fast push-in, intense first frame)",
            "Dynamic Action POV (Handheld realistic action, hyper-immersive)",
            "Ultra-Satisfying Kinetic Motion (Mesmerizing seamless loop)",
            "Fast Paced Punchy Story Beat (Expressive acting, dramatic zooms)"
        ])

    aspect_ratio = st.selectbox("Aspect Ratio:", ["9:16 (Vertical/Reels/Shorts)", "16:9 (Landscape/YouTube)", "1:1 (Square)"])
    story_input = st.text_area("కథ లేదా ఐడియా ఇక్కడ ఇవ్వండి (తెలుగు లేదా ఇంగ్లీష్):", height=120)

    if st.button("🚀 GPT-5.6 Luna / Veo వీడియో సీన్స్ తయారు చేయి", use_container_width=True):
        if not api_key:
            st.error("ఎడమవైపు సైడ్‌బార్‌లో Gemini API Key ఇవ్వండి.")
        elif not story_input.strip():
            st.warning("దయచేసి కథ లేదా ఐడియా రాయండి.")
        else:
            with st.spinner("GPT-5.6 Luna & Veo ఆర్కిటెక్చర్‌తో సీన్లను సిద్ధం చేస్తోంది..."):
                try:
                    client = genai.Client()
                    ar_val = aspect_ratio.split(" ")[0]
                    sys_v = f"""
                    You are an expert AI Video Prompt Architect specialized in {video_engine}.
                    Category: {video_category}. Aspect Ratio: {ar_val}. Style: {style_spec}.

                    Deconstruct the narrative into sequential scenes.
                    If targeted for GPT-5.6 Luna or Veo 3.1:
                    1. Emphasize multi-modal cinematic flow, physics, dynamic camera telemetry (dolly, crane, focal length).
                    2. Synchronize spatial audio cues and exact ambient SFX.
                    3. Provide clear continuity tokens / character anchors to maintain zero drift between cuts.

                    Return a JSON array of objects with keys:
                    - "scene_title": e.g. "Scene 1"
                    - "prompt": Full cinematic prompt with optics, lighting, and audio design.
                    - "continuity_anchor": Visual cue to keep character and environment identical across scenes.
                    - "motion_tip": Camera speed, lens angle, and transition cue.

                    Return ONLY valid JSON.
                    """
                    
                    raw_text, used_model = generate_with_fallback(client, story_input, sys_v, is_json=True)
                    scenes = json.loads(raw_text)
                    
                    st.success(f"మొత్తం {len(scenes)} సీన్లు సిద్ధమయ్యాయి! (Engine: {used_model})")

                    with st.expander("🚫 రికమండెడ్ నెగెటివ్ ప్రాంప్ట్ (Copy):"):
                        st.code("glitches, low quality, character morphing, anatomy drift, jerky motion, pixelated, watermark, frame drops, desynced audio", language="text")

                    for sc in scenes:
                        st.markdown(f"### 🎬 {sc.get('scene_title', 'Scene')}")
                        st.caption(f"🔗 **Continuity Anchor:** {sc.get('continuity_anchor', 'N/A')}")
                        st.caption(f"💡 **Motion & Lens Tip:** {sc.get('motion_tip', '')}")
                        st.code(sc.get("prompt", ""), language="text")
                        st.markdown("---")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# -------------------------------------------------------------
# మోడ్ 2: LLM Mega-Prompt Generator
# -------------------------------------------------------------
else:
    st.subheader("🧠 Elite Reasoning LLM Mega-Prompt Generator")
    
    latest_llm = st.selectbox(
        "లేటెస్ట్ టార్గెట్ AI మోడల్:",
        [
            "GPT-5.6 Luna (Multimodal Deep Reasoning & Creative Synthesis)",
            "Claude 3.7 Sonnet (Hybrid Reasoning + XML Architecture)",
            "OpenAI o3 / o1 (Multi-Step Logical Reasoning)",
            "OpenAI GPT-4o (High-Speed Multimodal & Precision RTC)",
            "DeepSeek-R1 (Open-Source Chain-of-Thought Specialist)"
        ]
    )

    task_input = st.text_area("మీ అసలు టాస్క్ / ఆలోచన ఇక్కడ రాయండి:", height=130)

    if st.button("✨ ఎలైట్ మెగా-ప్రాంప్ట్ జనరేట్ చేయి", use_container_width=True):
        if not api_key:
            st.error("ఎడమవైపు సైడ్‌బార్‌లో Gemini API Key ఇవ్వండి.")
        elif not task_input.strip():
            st.warning("దయచేసి టాస్క్ వివరాలు టైప్ చేయండి.")
        else:
            with st.spinner("వరల్డ్-క్లాస్ ప్రాంప్ట్ సిద్ధం చేస్తోంది..."):
                try:
                    client = genai.Client()
                    sys_llm = f"""
                    You are an elite Prompt Architect designing a prompt for {latest_llm}.
                    Output only the structured XML mega-prompt with sections:
                    <role>, <context>, <instructions>, <constraints>, and <output_format>.
                    """
                    
                    raw_text, used_model = generate_with_fallback(client, task_input, sys_llm, is_json=False)
                    st.success(f"ప్రాంప్ట్ సిద్ధమైంది! (Engine: {used_model})")
                    st.code(raw_text, language="markdown")
                except Exception as e:
                    st.error(f"Error: {str(e)}")