import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 1. إعدادات الواجهة
st.set_page_config(page_title="Korra Oracle", layout="wide")

st.markdown("<h1 style='text-align: center; color: #004a87;'>🔮 Korra Smart-Asset Oracle</h1>", unsafe_allow_html=True)

# 2. محرك قراءة البيانات
@st.cache_data
def load_data():
    files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    if not files: return None
    all_dfs = []
    for f in files:
        try:
            temp_df = pd.read_excel(f).fillna("---")
            temp_df['المصدر'] = f
            all_dfs.append(temp_df)
        except: continue
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else None

df = load_data()

# 3. عرض المحتوى
if df is not None:
    tab1, tab2 = st.tabs(["🔍 محرك البحث", "📊 التحليل الاستراتيجي"])
    
    with tab1:
        query = st.text_input("🎯 ابحث عن أي خامة أو كود:")
        if query:
            # بحث شامل في كل الأعمدة
            mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
            results = df[mask]
            st.success(f"وجدنا {len(results)} سجل.")
            st.dataframe(results, use_container_width=True)
            
    with tab2:
        st.subheader("تحليل كثافة البيانات")
        if not df.empty:
            # حل مشكلة الصورة الثانية: التأكد من وجود أعمدة كافية للرسم
            source_counts = df['المصدر'].value_counts().reset_index()
            source_counts.columns = ['اسم الملف', 'عدد الأصناف']
            fig = px.bar(source_counts, x='اسم الملف', y='عدد الأصناف', title="عدد الأصناف لكل ملف مرفوع")
            st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("👋 من فضلك ارفع ملف إكسيل (.xlsx) في المستودع ليعمل النظام.")
