import streamlit as st
import os
import tempfile
import requests
from streamlit_lottie import st_lottie
from agents.transcription_agent import TranscriptionAgent
from agents.requirement_agent import RequirementAgent
from agents.ambiguity_agent import AmbiguityAgent
from agents.question_agent import QuestionAgent
from agents.diagram_agent import DiagramAgent
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="Agentic AI BTP", layout="centered")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

local_css("style.css")

lottie_processing = load_lottieurl("https://lottie.host/bd715201-c817-47e1-9556-9b4d8964724a/PDB3G8v2E0.json")

# --- STATE MANAGEMENT ---
if 'state' not in st.session_state:
    st.session_state.state = 'INPUT'
if 'results' not in st.session_state:
    st.session_state.results = None

# --- HEADER ---
st.markdown("<h1>AGENTIC AI BTP</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">AUTONOMOUS REQUIREMENT EXTRACTION SYSTEM</p>', unsafe_allow_html=True)

# STATE 1: INPUT

if st.session_state.state == 'INPUT':
    
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    api_key = st.text_input("ACCESS KEY (GROQ)", type="password")
    uploaded_file = st.file_uploader("AUDIO SOURCE (MP3/WAV)", type=["mp3", "wav"])
    
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file and api_key:
        if st.button("INITIALIZE SYSTEM"):
            st.session_state.uploaded_file = uploaded_file
            st.session_state.api_key = api_key
            st.session_state.state = 'PROCESSING'
            st.rerun()

# STATE 2: PROCESSING

elif st.session_state.state == 'PROCESSING':
    
    st.markdown("<br>", unsafe_allow_html=True)
    if lottie_processing:
        st_lottie(lottie_processing, height=150, key="anim")
    
    status_text = st.empty()
    status_text.markdown("<p style='text-align: center; color: #66FF66; font-family: monospace; font-size: 18px;'>SYSTEM ACTIVE: DECODING AUDIO STREAM...</p>", unsafe_allow_html=True)
    
    try:
        # 1. Save File
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(st.session_state.uploaded_file.read())
            temp_audio_path = temp_audio.name
        
        # 2. Transcribe
        transcriber = TranscriptionAgent()
        trans_result = transcriber.transcribe_audio(temp_audio_path)
        
        if "error" in trans_result:
            st.error(f"FATAL ERROR: {trans_result['error']}")
            st.session_state.state = 'INPUT'
        else:
            transcript = trans_result["text"]
            
            # 3. Analyze
            status_text.markdown("<p style='text-align: center; color: #66FF66; font-family: monospace; font-size: 18px;'>SYSTEM ACTIVE: EXTRACTING LOGIC GATES...</p>", unsafe_allow_html=True)
            req_agent = RequirementAgent(st.session_state.api_key)
            requirements = req_agent.analyze(transcript)
            
            # 4. Ambiguity
            status_text.markdown("<p style='text-align: center; color: #66FF66; font-family: monospace; font-size: 18px;'>SYSTEM ACTIVE: CALCULATING RISK VECTORS...</p>", unsafe_allow_html=True)
            amb_agent = AmbiguityAgent(st.session_state.api_key)
            gaps = amb_agent.analyze_gaps(transcript, requirements)
            
            # 5. Questions
            q_agent = QuestionAgent(st.session_state.api_key)
            questions = q_agent.generate_questions(gaps)
            
            # 6. Diagram
            status_text.markdown("<p style='text-align: center; color: #66FF66; font-family: monospace; font-size: 18px;'>SYSTEM ACTIVE: GENERATING BLUEPRINT...</p>", unsafe_allow_html=True)
            diag_agent = DiagramAgent(st.session_state.api_key)
            diagram_code = diag_agent.generate_diagram(requirements)
            
            # Save Results
            st.session_state.results = {
                "requirements": requirements,
                "gaps": gaps,
                "questions": questions,
                "diagram_code": diagram_code
            }
            
            os.remove(temp_audio_path)
            st.session_state.state = 'RESULTS'
            st.rerun()

    except Exception as e:
        st.error(f"SYSTEM FAILURE: {e}")
        if st.button("RESET"):
            st.session_state.state = 'INPUT'
            st.rerun()


# STATE 3: RESULTS

elif st.session_state.state == 'RESULTS':
    
    st.markdown("<h3 style='color: #66FF66; text-align: center; margin-bottom: 20px;'>ANALYSIS COMPLETE</h3>", unsafe_allow_html=True)
    
    # --- PDF GENERATION ---
    pdf_bytes = generate_pdf(
        st.session_state.results["requirements"],
        st.session_state.results["questions"],
        st.session_state.results["gaps"],
        st.session_state.results["diagram_code"]
    )
    
    # Download Button for the Full Report
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📄 DOWNLOAD FULL PROFESSIONAL REPORT (PDF)",
            data=pdf_bytes,
            file_name="project_requirements_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.write("") # Spacer

    # TABS
    tab1, tab2, tab3, tab4 = st.tabs(["REQUIREMENTS", "QUESTIONS", "RISKS", "BLUEPRINT"])
    
    with tab1:
        st.markdown(st.session_state.results["requirements"])
        
    with tab2:
        st.markdown(st.session_state.results["questions"])
        
    with tab3:
        st.markdown(st.session_state.results["gaps"])
        
    with tab4:
        st.markdown("<h4 style='color: #E0E0E0;'>System Architecture Diagram</h4>", unsafe_allow_html=True)
        try:
            st.graphviz_chart(st.session_state.results["diagram_code"])
            st.caption("Auto-generated flow based on requirements.")
        except Exception as e:
            st.error("Diagram Rendering Failed.")
            st.code(st.session_state.results["diagram_code"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("TERMINATE SESSION / RESET"):
        st.session_state.results = None
        st.session_state.state = 'INPUT'
        st.rerun()