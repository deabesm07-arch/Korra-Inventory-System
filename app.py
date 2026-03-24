import streamlit as st
import pandas as pd
import os
import plotly.express as px

# إعدادات الواجهة
st.set_page_config(page_title="Korra Oracle", layout="wide")
st.markdown("<h1 style='text-align: center; color: #004a87;'>🔮 Korra Smart-Asset Oracle</h1>", unsafe_allow_html=True)

# محرك قراءة الملفات الذكي (يقرأ data.xlsx الذي رفعته)
@st.cache_data
def load_data():
    files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
    if not files: return None
    all_dfs = []
    for f in files:
        try:
            # استخدام engine='openpyxl' لضمان قراءة ملفات XLSX
            temp_df = pd.read_excel(f, engine='openpyxl').fillna("---")
            temp_df['المصدر'] = f
            all_dfs.append(temp_df)
        except Exception as e:
            st.error(f"خطأ في الملف {f}: {e}")
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else None

df = load_data()

if df is not None:
    st.success(f"✅ تم تحميل البيانات بنجاح من ملف: {df['المصدر'].unique()}")
    
    query = st.text_input("🎯 ابحث عن أي خامة أو كود:")
    if query:
        # بحث شامل وبسيط يتجنب تعقيدات scipy
        mask = df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)
        results = df[mask]
        st.dataframe(results, use_container_width=True)
        
    # لوحة تحليلات بسيطة تمنع خطأ ValueError الظاهر في الصورة الثانية
    st.divider()
    if not df.empty:
        source_counts = df['المصدر'].value_counts().reset_index()
        source_counts.columns = ['الملف', 'العدد']
        fig = px.bar(source_counts, x='الملف', y='العدد', title="إحصائيات الملفات المرفوعة")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("👋 تأكد من وجود ملف data.xlsx في المستودع.")
