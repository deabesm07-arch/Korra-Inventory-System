import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 1. إعدادات الواجهة الاحترافية لشركة Korra
st.set_page_config(page_title="Korra Inventory Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #f4f7f9; }
    .main-header { background: #004a87; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .stat-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid #004a87; }
    </style>
""", unsafe_allow_html=True)

# 2. محرك معالجة البيانات (مع حل مشكلة الأسماء المكررة)
@st.cache_data
def load_and_clean_data():
    files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
    if not files: return None
    
    all_data = []
    for f in files:
        try:
            df = pd.read_excel(f, engine='openpyxl')
            # حل مشكلة الصورة 12: حذف الأعمدة المكررة تلقائياً
            df = df.loc[:, ~df.columns.duplicated()]
            df = df.fillna("---")
            df['المصدر'] = f
            all_data.append(df)
        except: continue
    
    return pd.concat(all_data, ignore_index=True) if all_data else None

# 3. بناء لوحة التحكم
st.markdown('<div class="main-header"><h1>📊 مستودع Korra الرقمي للأصول</h1></div>', unsafe_allow_html=True)

df = load_and_clean_data()

if df is not None:
    # عرض إحصائيات سريعة (البطاقات)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-card"><h3>{len(df)}</h3><p>إجمالي الأصناف</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><h3>{len(df.columns)-1}</h3><p>حقول البيانات</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><h3>{df["المصدر"].nunique()}</h3><p>ملفات نشطة</p></div>', unsafe_allow_html=True)

    st.divider()
    
    tab1, tab2 = st.tabs(["📋 استعراض المخزون المتاح", "📈 تحليل البيانات"])
    
    with tab1:
        search = st.text_input("🔍 ابحث عن أي خامة (مثلاً: كابل، محبس، حديد)...")
        if search:
            results = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            st.dataframe(results, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
            
    with tab2:
        # حل مشكلة الصورة 1: التأكد من وجود بيانات قبل الرسم
        st.subheader("توزيع الأصناف حسب ملف المصدر")
        file_stats = df['المصدر'].value_counts().reset_index()
        file_stats.columns = ['الملف', 'العدد']
        fig = px.pie(file_stats, values='العدد', names='الملف', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("👋 بانتظار رفع ملف data.xlsx في GitHub لبدء عرض لوحة التحكم.")
