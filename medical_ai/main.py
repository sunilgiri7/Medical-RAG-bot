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

# Page config with dark mode title and icon
st.set_page_config(
    page_title="MediTech Advisor",
    page_icon="🏥",
    layout="wide",
)

# Custom CSS for a modern, professional dark theme
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Background and Text Color */
    .stApp, .main {
        background-color: #0e0e0e;
        color: #e8e8e8;
    }
    
    /* Container settings */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header Styling */
    .header-container {
        padding: 2rem 0;
        text-align: center;
        border-bottom: 1px solid #333333;
    }
    .header-container h1 {
        font-size: 3rem;
        color: #f0a500;
        margin-bottom: 0.5rem;
    }
    .header-container p {
        font-size: 1.25rem;
        color: #a8a8a8;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 1px solid #333333;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #141414;
    }
    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem;
    }
    
    /* Card Section Styling */
    .section-container {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    .section-title {
        font-size: 1.5rem;
        color: #f0a500;
        margin-bottom: 1rem;
        border-bottom: 1px solid #333333;
        padding-bottom: 0.5rem;
    }
    
    /* Input and Button Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #141414;
        color: #e8e8e8;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 0.75rem;
    }
    .stButton>button {
        background-color: #f0a500;
        color: #0e0e0e;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.5);
    }
    
    /* Answer Display Styling */
    .answer-container {
        background-color: #141414;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        border-left: 6px solid #f0a500;
    }
    .answer-header {
        font-size: 1.75rem;
        color: #f0a500;
        margin-bottom: 1rem;
        border-bottom: 1px solid #333333;
        padding-bottom: 0.5rem;
    }
    .answer-content {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #e8e8e8;
    }
    .answer-content a {
        color: #f0a500;
        text-decoration: underline;
    }
    
    /* Table Styling */
    .answer-content table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .answer-content th, .answer-content td {
        border: 1px solid #333333;
        padding: 0.75rem;
        text-align: left;
    }
    .answer-content th {
        background-color: #1f1f1f;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 1rem 0;
        border-top: 1px solid #333333;
        margin-top: 2rem;
        color: #a8a8a8;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header-container">
        <h1>MediTech Advisor</h1>
        <p>Advanced AI Guidance on Medical Equipment & Healthcare Systems</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.image("https://img.freepik.com/free-photo/pills-medical-tools-arrangement-flat-lay_23-2149341610.jpg?semt=ais_hybrid", width=150)
    st.markdown("### About MediTech Advisor")
    st.markdown("""
    MediTech Advisor delivers cutting-edge insights on:
    
    * Medical equipment specifications
    * Device operation guidelines
    * Healthcare technology systems
    * Regulatory compliance and safety
    * Best practices in medical technology
    """)
    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
    1. Upload relevant technical documents (PDFs) if available.
    2. Enter your medical technology query.
    3. Click **Get Expert Answer**.
    """)

# Upload Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📄 Upload Technical Documentation</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("Upload product manuals, spec sheets, or technical guides (PDF)", 
                                  accept_multiple_files=True,
                                  type="pdf",
                                  help="We will extract key details from these documents.")
st.markdown('</div>', unsafe_allow_html=True)

# Query Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">❓ Ask Your Question</div>', unsafe_allow_html=True)
question = st.text_area("Enter your question about medical equipment, devices, or healthcare systems",
                          placeholder="Example: What are the latest features of modern ventilators for ICU settings?",
                          height=120)
with st.expander("See example questions"):
    st.markdown("""
    - What are the advantages of 3T MRI machines over 1.5T models?
    - How do modern insulin pumps integrate with continuous glucose monitors?
    - What are the sterilization protocols for surgical robots?
    - Compare ultrasound systems for cardiac diagnostics.
    - What regulatory approvals are required for new infusion pumps in the US?
    """)
search_button = st.button("Get Expert Answer")
st.markdown('</div>', unsafe_allow_html=True)

def generate_prompt(question: str, pdf_text: str, web_results: str) -> str:
    """
    Generate a detailed prompt that integrates PDF content and web search results.
    """
    context = f"### PDF DOCUMENTATION:\n{pdf_text}\n\n### WEB SEARCH RESULTS:\n{web_results}"
    prompt = f"""
You are MediTech Advisor, an expert AI specializing in medical equipment, devices, healthcare technology systems, and regulatory standards. A healthcare professional has asked: "{question}"

First, analyze the question to identify the specific medical technology domain, key requirements, and information needs.

### AVAILABLE CONTEXT
{context}

### INSTRUCTIONS
1. Provide a comprehensive, accurate, and structured response focusing exclusively on medical equipment and healthcare systems.
2. Begin with a clear, direct answer to the question.
3. Include precise technical specifications, clinical applications, and operational considerations when relevant.
4. Organize your response with clear headings and bullet points for readability.
5. If comparing technologies, use a structured comparison format.
6. Include numerical data and statistics when available.
7. For regulatory details, mention applicable standards (FDA, CE, ISO, etc.) and requirements.
8. Highlight any safety considerations.
9. Cite sources explicitly (PDF document names with page numbers, URLs from web results).
10. If further data is needed, specify what additional information would be helpful.
11. For implementation questions, include practical guidelines and best practices.
12. Use proper medical and technical terminology.

### RESPONSE FORMAT
Structure your answer with the following sections (if applicable):
- Summary Answer
- Technical Specifications
- Clinical Applications
- Operational Considerations
- Regulatory & Safety Information
- Comparison Table (if comparing options)
- Implementation Guidelines
- Sources & Citations

Format your answer using Markdown.
"""
    return prompt

if search_button:
    if not question:
        st.warning("Please enter a question to continue.")
    else:
        with st.spinner("Gathering information... Please wait"):
            # Process PDF uploads
            pdf_text = ""
            if uploaded_files:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_paths = []
                    for uploaded_file in uploaded_files:
                        temp_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        pdf_paths.append(temp_path)
                    
                    # Extract text from PDFs
                    pdf_tool = PDFSearchTool()
                    pdf_text = pdf_tool.search(question, pdf_paths)
            
            # Perform a web search for additional context
            web_tool = DuckDuckGoTools()
            try:
                web_results = web_tool.search(question)
            except Exception as e:
                web_results = f"Web search error: {e}"
            
            # Generate the final prompt for the agent
            prompt = generate_prompt(question, pdf_text, web_results)
            
            # Get the expert response from the agent
            try:
                run_response = agent.run(prompt)
                answer = run_response.content if hasattr(run_response, "content") else str(run_response)
            except Exception as e:
                answer = f"Error generating answer: {e}"
            
            # Display the answer
            st.markdown('<div class="answer-container">', unsafe_allow_html=True)
            st.markdown('<div class="answer-header">Expert Analysis</div>', unsafe_allow_html=True)
            st.markdown('<div class="answer-content">', unsafe_allow_html=True)
            st.markdown(answer, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
