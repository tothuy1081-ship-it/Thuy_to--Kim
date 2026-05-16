import streamlit as st
import pandas as pd
import os
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Lead Scoring Dashboard", page_icon="🎯", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #007bff;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background: linear-gradient(to right, #007bff, #0056b3);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONSTANTS ---
SHEET_ID = "1-4t-PPznFeQMlM5WNptbsp22HGUYSLNIT7yf5l8UL4M"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- SCORING ENGINE ---
def score_lead(description):
    desc = str(description).lower()
    score = 0
    reasons = []

    # 1. VIP CRITERIA (+50)
    vip_keywords = {
        'Ngân sách lớn': ['20 tỷ', 'tài chính mạnh', 'không thành vấn đề', 'ngân sách vô hạn'],
        'Loại hình cao cấp': ['biệt thự đơn lập', 'penthouse', 'shophouse', 'quỹ đất công nghiệp', 'sàn văn phòng diện tích lớn'],
        'Vị trí đắc địa': ['quận 1', 'ven sông', 'vinhomes ocean park', 'phú mỹ hưng'],
        'Đối tượng VIP': ['chủ doanh nghiệp', 'nhà đầu tư chuyên nghiệp', 'mua sỉ', 'mua số lượng lớn'],
        'Tính cấp thiết': ['pháp lý chuẩn 100%', 'sổ hồng riêng', 'gặp trực tiếp chủ đầu tư']
    }

    for category, keywords in vip_keywords.items():
        found = [k for k in keywords if k in desc]
        if found:
            score += 50
            reasons.append(f"{category} ({', '.join(found)})")

    # 2. TRASH CRITERIA (-50)
    trash_keywords = {
        'Nhu cầu phi thực tế': ['quận 1 giá 1 tỷ', 'quận 1 giá 2 tỷ', 'trung tâm vài trăm triệu'],
        'Không có nhu cầu': ['nhầm số', 'không có nhu cầu', 'dữ liệu cũ', 'nhầm ngành'],
        'Không thiện chí': ['hỏi giá cho vui', 'chưa có ý định mua', 'thái độ không hợp tác'],
        'Spam/Ads': ['bảo hiểm', 'vay vốn', 'mời chào dịch vụ', 'quảng cáo'],
        'Lỗi liên lạc': ['thuê bao', 'không bắt máy', 'không phản hồi zalo']
    }

    for category, keywords in trash_keywords.items():
        found = [k for k in keywords if k in desc]
        if found:
            score -= 50
            reasons.append(f"{category} ({', '.join(found)})")

    # 3. NEUTRAL / SMALL BONUS
    if 'chung cư' in desc or 'nhà phố' in desc:
        if '3-10 tỷ' in desc or 'tầm trung' in desc:
            score += 10
            reasons.append("Phân khúc tầm trung (10đ)")
    
    if 'vay ngân hàng' in desc or 'cân nhắc chính sách' in desc:
        reasons.append("Cần hỗ trợ tài chính")

    # Final Categorization
    if score >= 50:
        cat = "VIP"
    elif score > 0:
        cat = "Potential"
    elif score == 0:
        cat = "Neutral"
    else:
        cat = "Trash"

    return score, cat, "; ".join(reasons) if reasons else "Thông tin cơ bản"

# --- MAIN UI ---
st.title("🎯 AI Lead Scoring & Management")
st.subheader("Hệ thống chấm điểm khách hàng tự động cho Bất Động Sản")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/target.png")
    st.header("Cài đặt hệ thống")
    if st.button("🔄 Tải lại dữ liệu từ Google Sheet"):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.markdown("### Hướng dẫn:")
    st.write("1. Nhấn **Process Leads** để chấm điểm.")
    st.write("2. Kiểm duyệt tại bảng **Human-in-the-loop**.")
    st.write("3. Xuất file Excel để bàn giao.")

# Data Fetching
@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("### 📊 Thống kê nhanh")
        st.metric("Tổng số Leads", len(df))
        if st.button("🚀 Process & Score All Leads", use_container_width=True):
            with st.spinner("Đang phân tích dữ liệu..."):
                results = []
                for _, row in df.iterrows():
                    score, cat, reason = score_lead(row.get('nhu_cau_mo_ta', ''))
                    results.append({**row.to_dict(), 'Score': score, 'Category': cat, 'Reasoning': reason})
                st.session_state['scored_df'] = pd.DataFrame(results)
                st.success("Đã chấm điểm xong!")

    with col2:
        if 'scored_df' in st.session_state:
            st.write("### 🧐 Human-in-the-loop Review")
            st.info("💡 Bạn có thể chỉnh sửa trực tiếp điểm hoặc phân loại trong bảng dưới đây.")
            
            # Interactive Editor
            edited_df = st.data_editor(
                st.session_state['scored_df'],
                column_config={
                    "Score": st.column_config.NumberColumn("Điểm", format="%d"),
                    "Category": st.column_config.SelectboxColumn("Phân loại", options=["VIP", "Potential", "Neutral", "Trash"]),
                    "Reasoning": st.column_config.TextColumn("Lý do", width="large")
                },
                use_container_width=True,
                num_rows="dynamic"
            )
            
            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("VIP", len(edited_df[edited_df['Category'] == 'VIP']))
            m2.metric("Potential", len(edited_df[edited_df['Category'] == 'Potential']))
            m3.metric("Neutral", len(edited_df[edited_df['Category'] == 'Neutral']))
            m4.metric("Trash", len(edited_df[edited_df['Category'] == 'Trash']))

            # Export Area
            st.divider()
            st.write("### 📥 Xuất dữ liệu bàn giao")
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='Leads_Scored')
            
            st.download_button(
                label="📥 Tải xuống file Excel hoàn chỉnh",
                data=output.getvalue(),
                file_name="lead_scoring_final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.write("### 📋 Dữ liệu thô từ Google Sheets")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Không thể kết nối với Google Sheet. Vui lòng kiểm tra quyền chia sẻ. Lỗi: {e}")

st.markdown("---")
st.caption("© 2026 AI Lead Scoring System - Developed for Real Estate Professionalism")
