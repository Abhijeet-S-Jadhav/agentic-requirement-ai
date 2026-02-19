# Agentic AI-Based Requirement Gathering System

## 1. Project Overview
This project implements an autonomous pipeline for converting unstructured audio data into structured technical documentation. In software development, verbal requirement gathering often results in incomplete or ambiguous specifications. This system addresses that problem by utilizing a multi-stage NLP architecture to ingest audio, generate transcripts, extract features, perform logical gap analysis, and produce a serialized PDF specification including architectural models.

---

## 2. 2. Technical Architecture Design
The system follows a Distributed Multi-Agent Architecture designed to separate concerns between data ingestion and semantic reasoning.
1. **Compute Distribution:** The system utilizes a local-compute model for *Automated Speech Recognition (ASR)* to maintain data privacy, while leveraging high-speed cloud-based inference for semantic analysis.
2. **Modular Logic:** Each stage of the pipeline is handled by an independent Large Language Model (LLM) instance with a constrained technical persona. This prevents *Prompt Dilution* and ensures that the analytical weights of the model are focused on one specific domain (e.g., risk analysis vs. structural modeling) at a time.
3. **Deterministic Parsing:** The system uses greedy decoding *(temperature=0)* to ensure that technical extractions remain consistent and reproducible across multiple runs.

---

## 3. Agent Responsibilities
The system employs a pipeline of five specialized agents:

1.  **Transcription Agent:** Ingests audio (MP3/WAV) and performs local ASR using the OpenAI Whisper model to generate a text transcript.
2.  **Requirement Agent:** Performs Semantic Parsing to categorize features into Functional and Non-Functional requirements.
3.  **Ambiguity Agent:** Performs a logical audit to find vague terms or missing technical specifications.
4.  **Question Agent:** Generates technical clarifying questions to mitigate identified risks.
5.  **Diagram Agent:** Translates requirements into DOT language and compiles a System Architecture Blueprint.

## 4. Processing Workflow

1. **Ingestion:** Audio signals (MP3/WAV) are resampled to 16,000 Hz mono-streams and converted to Log-Mel Spectrograms.
2. **Transcription:** The ASR engine performs sequence-to-sequence decoding to generate raw text.
3. **Extraction:** Functional and Non-Functional requirements are categorized via Named Entity Recognition (NER).
4. **Audit:** The system cross-references the transcript with extracted features to identify qualitative ambiguities or logic gaps.
5. **Blueprint:** Requirements are mapped to a Directed Acyclic Graph (DAG) using DOT syntax.
6. **Serialization:** All data structures are cleaned of Unicode incompatibilities and compiled into a structured PDF specification.

**Workflow:** `Audio Ingestion` -> `ASR` -> `Requirement Extraction` -> `Gap Analysis` -> `Question Generation` -> `Architecture Modeling` -> `PDF Serialization`.

---

## 5. How to Run the Project

### Prerequisites
1. **Python 3.10+**
2. **Graphviz System Binary:** 
   - Windows: `winget install graphviz`
   - Mac: `brew install graphviz`
   - *Note: Restart your terminal after installation.*

### Installation
1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd agentic-requirement-ai

2. **Initialize a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

### Execution

1 **Run the application via Streamlit:**
    ```bash
    streamlit run app.py

*A Groq API key is required to power the inference modules.*

## 6. Sample Data

Input Samples: Located in sample_audio/. Includes realistic client-vendor calls.
Output Samples: Located in output/. Includes generated Markdown files and a sample PDF report.

## 7. Technical Stack

UI Framework: Streamlit
Workflow Management: LangChain (LCEL)
Speech Processing: OpenAI Whisper
Inference Engine: Llama 3.3 via Groq LPU
Diagram Engine: Graphviz
PDF Generation: FPDF Engine