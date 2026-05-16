import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import os
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Lead Scoring System", page_icon="🎯", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONSTANTS ---
SHEET_ID = "1-4t-PPznFeQMlM5WNptbsp22HGUYSLNIT7yf5l8UL4M"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
SKILL_FILE = "lead_scoring_skill.md"

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Ensure the Google Sheet is set to 'Anyone with the link can view' for direct fetching.")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()

# --- HELPER FUNCTIONS ---
def load_skill_prompt():
    if os.path.exists(SKILL_FILE):
        with open(SKILL_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "Skill file not found."

def get_google_sheet_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Error fetching Google Sheet: {e}")
        return None

def score_lead_with_ai(lead_data, skill_prompt, api_key):
    if not api_key:
        return {"score": 0, "category": "Error", "reasoning": "Missing API Key"}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert Lead Scoring AI for the Real Estate industry. 
    Use the following SKILL DEFINITION to score the lead provided below.
    
    --- SKILL DEFINITION ---
    {skill_prompt}
    
    --- LEAD DATA ---
    ID: {lead_data.get('id')}
    Name: {lead_data.get('ten_khach')}
    Phone: {lead_data.get('sdt')}
    Description: {lead_data.get('nhu_cau_mo_ta')}
    
    Return ONLY a JSON object exactly following the 'Output Format' specified in the Skill Definition.
    Do not include markdown code blocks or any other text.
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean response text in case it includes markdown blocks
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json)
    except Exception as e:
        return {"score": 0, "category": "Error", "reasoning": f"AI Error: {str(e)}"}

# --- MAIN APP ---
st.title("🎯 AI Lead Scoring & Automation")
st.markdown("---")

skill_prompt = load_skill_prompt()

if not api_key:
    st.warning("⚠️ Please enter your Gemini API Key in the sidebar to start scoring.")

# Data Fetching
df = get_google_sheet_data()

if df is not None:
    st.subheader("📋 Raw Customer Data")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🚀 Process & Score Leads"):
        if not api_key:
            st.error("API Key required!")
        else:
            with st.spinner("AI is analyzing leads..."):
                results = []
                for _, row in df.iterrows():
                    lead_data = row.to_dict()
                    score_res = score_lead_with_ai(lead_data, skill_prompt, api_key)
                    
                    # Merge results
                    combined = {**lead_data, **score_res}
                    results.append(combined)
                
                st.session_state['scored_df'] = pd.DataFrame(results)
                st.success("Scoring complete!")

# Human-in-the-loop Review
if 'scored_df' in st.session_state:
    st.markdown("---")
    st.subheader("🧐 Human-in-the-loop Review")
    st.write("Review the AI scores and manually adjust the 'category' or 'score' if necessary.")
    
    # Editable Dataframe
    edited_df = st.data_editor(
        st.session_state['scored_df'],
        column_config={
            "score": st.column_config.NumberColumn("Score", min_value=-50, max_value=100),
            "category": st.column_config.SelectboxColumn("Category", options=["VIP", "Potential", "Neutral", "Trash"]),
            "reasoning": st.column_config.TextColumn("Reasoning", width="large")
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Leads", len(edited_df))
    c2.metric("VIP Leads", len(edited_df[edited_df['category'] == 'VIP']))
    c3.metric("Potential", len(edited_df[edited_df['category'] == 'Potential']))
    c4.metric("Trash", len(edited_df[edited_df['category'] == 'Trash']))
    
    # Export
    st.markdown("### 📥 Export Results")
    col_exp1, col_exp2 = st.columns(2)
    
    # CSV Export
    csv = edited_df.to_csv(index=False).encode('utf-8-sig')
    col_exp1.download_button(
        "Download as CSV",
        csv,
        "lead_scoring_results.csv",
        "text/csv",
        key='download-csv'
    )
    
    # Excel Export
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        edited_df.to_excel(writer, index=False, sheet_name='Leads')
    excel_data = output.getvalue()
    col_exp2.download_button(
        "Download as Excel",
        excel_data,
        "lead_scoring_results.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key='download-excel'
    )
else:
    st.info("Click 'Process & Score Leads' to see the analysis.")
