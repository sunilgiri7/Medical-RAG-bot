import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from utils.pdf_tool import PDFSearchTool

# Load environment variables and set API key
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize the Agno agent
model = Groq(id="llama-3.3-70b-versatile")
agent = Agent(model=model, markdown=True)

# Page config
st.set_page_config(
    page_title="MediTech Advisor",
    page_icon="🏥",
    layout="wide",
)

# Custom CSS for a clean, modern medical theme
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
        color: #334155;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1 {
        color: #0369a1;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .stButton>button {
        background-color: #0284c7;
        color: white;
        border-radius: 8px;
        padding: 0.75em 2em;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    .upload-section, .query-section {
        background-color: white;
        padding: 0.1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .section-title {
        color: #0369a1;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .answer-container {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
        border-left: 5px solid #0284c7;
    }
    .answer-header {
        color: #0369a1;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    .answer-content {
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .answer-content h2 {
        color: #0369a1;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    .answer-content h3 {
        color: #334155;
        font-size: 1.1rem;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .answer-content ul, .answer-content ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    .answer-content li {
        margin-bottom: 0.5rem;
    }
    .answer-content p {
        margin-bottom: 1rem;
    }
    .answer-content a {
        color: #0284c7;
        text-decoration: none;
        border-bottom: 1px dotted #0284c7;
    }
    .answer-content blockquote {
        border-left: 3px solid #0284c7;
        padding-left: 1rem;
        font-style: italic;
        color: #64748b;
        margin: 1rem 0;
    }
    .answer-content table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0 2rem 0;
    }
    .answer-content table th {
        background-color: #f1f5f9;
        padding: 0.75rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
    }
    .answer-content table td {
        padding: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .citation {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #64748b;
        font-size: 0.9rem;
    }
    .footer img {
        height: 24px;
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    .stAlert {
        background-color: #f0f9ff;
        color: #0c4a6e;
        border: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h1>MediTech Advisor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Expert guidance on medical equipment, devices, and healthcare systems</p>", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.image("https://img.freepik.com/free-photo/pills-medical-tools-arrangement-flat-lay_23-2149341610.jpg?semt=ais_hybrid", width=150)
    st.markdown("### About MediTech Advisor")
    st.markdown("""
    MediTech Advisor provides expert knowledge on:
    
    * Medical equipment specifications
    * Device operation guidelines
    * Healthcare technology systems
    * Regulatory compliance information
    * Best practices in medical technology
    """)
    
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Upload relevant PDF documentation (optional)
    2. Enter your medical technology question
    3. Click 'Get Expert Answer'
    """)

# Main content area
st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>📄 Upload Technical Documentation</p>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Upload product manuals, spec sheets, or technical guides (PDF)", 
                                 accept_multiple_files=True, 
                                 type="pdf",
                                 help="We'll extract relevant information from these documents")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='query-section'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>❓ Ask Your Question</p>", unsafe_allow_html=True)
question = st.text_area("Enter your question about medical equipment, devices, or healthcare systems",
                      placeholder="Example: What are the key features of modern ventilators for COVID-19 patients?",
                      height=100)

# Examples to help users
with st.expander("See example questions"):
    st.markdown("""
    - What are the advantages of 3T MRI machines compared to 1.5T models?
    - How do modern insulin pumps integrate with continuous glucose monitoring systems?
    - What are the sterilization requirements for surgical robots?
    - Compare ultrasound systems for cardiac diagnostics
    - What regulatory approvals are needed for a new infusion pump in the US market?
    """)

search_button = st.button("Get Expert Answer")
st.markdown("</div>", unsafe_allow_html=True)

def generate_prompt(question: str, pdf_text: str, web_results: str) -> str:
    """
    Create a detailed prompt that combines context from PDFs and web searches,
    optimized for medical device and healthcare technology information.
    """
    context = f"### PDF DOCUMENTATION:\n{pdf_text}\n\n### WEB SEARCH RESULTS:\n{web_results}"
    
    prompt = f"""
You are MediTech Advisor, an expert AI specializing in medical equipment, devices, healthcare technology systems, and related regulatory standards. A healthcare professional has asked: "{question}"

First, analyze this question to identify the specific medical technology domain, key requirements, and information needs.

### AVAILABLE CONTEXT
{context}

### INSTRUCTIONS
1. Provide a comprehensive, accurate, and structured response focusing exclusively on medical equipment and healthcare systems.
2. Begin with a clear, direct answer to the question.
3. Include precise technical specifications, clinical applications, and operational considerations when relevant.
4. Organize your response with clear headings and bullet points for readability.
5. If comparing technologies or approaches, use a structured comparison format.
6. Include numerical data and statistics when available.
7. For regulatory information, specify applicable standards (FDA, CE, ISO, etc.) and requirements.
8. If safety considerations are relevant, highlight them prominently.
9. Cite your sources explicitly (PDF document names with page numbers, URLs from web results).
10. If information is incomplete, clearly state what additional data would be helpful.
11. For implementation questions, include practical considerations and best practices.
12. Use medical and technical terminology appropriately, defining complex terms.

### RESPONSE FORMAT
Structure your answer with these sections as appropriate:
- Summary Answer (direct response to the question)
- Technical Specifications (when discussing equipment)
- Clinical Applications
- Operational Considerations
- Regulatory & Safety Information
- Comparison Table (when comparing options)
- Implementation Guidelines
- Sources & Citations

Format your response using Markdown for readability. Use tables for comparing options and bullet points for lists.
"""
    return prompt

if search_button:
    if not question:
        st.warning("Please enter a question to continue.")
    else:
        with st.spinner("Researching your query... This may take a moment"):
            # Process PDFs if uploaded
            pdf_text = ""
            if uploaded_files:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_paths = []
                    for uploaded_file in uploaded_files:
                        temp_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        pdf_paths.append(temp_path)
                        
                    # Extract relevant information from PDFs
                    pdf_tool = PDFSearchTool()
                    pdf_text = pdf_tool.search(question, pdf_paths)
            
            # Gather information from the web
            web_tool = DuckDuckGoTools()
            try:
                web_results = web_tool.search(question)
            except Exception as e:
                web_results = f"Web search error: {e}"
            
            # Generate optimized prompt
            prompt = generate_prompt(question, pdf_text, web_results)
            
            # Get response from the agent
            try:
                run_response = agent.run(prompt)
                answer = run_response.content if hasattr(run_response, "content") else str(run_response)
            except Exception as e:
                answer = f"Error generating answer: {e}"
            
            # Display the answer in a structured format
            st.markdown("<div class='answer-container'>", unsafe_allow_html=True)
            st.markdown("<div class='answer-header'>Expert Analysis</div>", unsafe_allow_html=True)
            st.markdown("<div class='answer-content'>", unsafe_allow_html=True)
            st.markdown(answer, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)