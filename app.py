import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- 1. إعدادات الهوية البصرية (Professional Dark/Light UI) ---
st.set_page_config(page_title="Korra Inventory Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #f8f9fa; }
    .main-header { background: linear-gradient(90deg, #004a87, #002d50); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .category-card { background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #004a87; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    .stat-number { font-size: 24px; font-weight: bold; color: #004a87; }
    .stat-label { color: #666; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التصنيف والذكاء (Core Logic) ---
class InventoryEngine:
    @staticmethod
    def get_category(desc):
        desc = str(desc).lower()
        if any(x in desc for x in ['cable', 'wire', 'كهربا', 'كابل', 'سلك', 'breaker']): return '⚡ قطاع الكهرباء'
        if any(x in desc for x in ['pipe', 'valve', 'pump', 'محبس', 'ماسور', 'طلمب']): return '🔧 قطاع الميكانيكا'
        if any(x in desc for x in ['steel', 'cement', 'حديد', 'خرسان', 'مدنى']): return '🏗️ قطاع المدني'
        if any(x in desc for x in ['gasket', 'seal', 'جوان', 'سيول', 'bearing']): return '⚙️ قطع غيار'
        return '📦 أصناف عامة'

    @staticmethod
    @st.cache_data
    def load_data():
        files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
        if not files: return None
        all_dfs = []
        for f in files:
            try:
                temp_df = pd.read_excel(f, engine='openpyxl')
                temp_df['Source_File'] = f
                all_dfs.append(temp_df)
            except: continue
        if not all_dfs: return None
        df = pd.concat(all_dfs, ignore_index=True)
        # تحديد العمود الثاني كاسم للخامة
        desc_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        df['Category'] = df[desc_col].apply(InventoryEngine.get_category)
        return df, desc_col

# --- 3. بناء لوحة التحكم ---
st.markdown('<div class="main-header"><h1>📊 نظام الرصد الذكي للمخزون - Korra Energi</h1><p>تحليل فوري للمجموعات والكميات المتاحة</p></div>', unsafe_allow_html=True)

data_pack = InventoryEngine.load_data()

if data_pack:
    df, desc_col = data_pack
    
    # صف الملخص العلوي
    cols = st.columns(4)
    categories = df['Category'].unique()
    
    for i, cat in enumerate(categories[:4]): # عرض أول 4 تصنيفات في الأعلى
        cat_count = len(df[df['Category'] == cat])
        with cols[i]:
            st.markdown(f"""
                <div class="category-card">
                    <div class="stat-label">{cat}</div>
                    <div class="stat-number">{cat_count}</div>
                    <div style="font-size:12px; color:#999;">خامة مسجلة</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # توزيع المحتوى: البحث والتصفية
    col_side, col_main = st.columns([1, 3])
    
    with col_side:
        st.subheader("🎯 مصفاة المخزون")
        selected_cat = st.selectbox("اختر المجموعة:", ["الكل"] + list(categories))
        search_query = st.text_input("🔍 بحث سريع في المجموعة:")
        
    with col_main:
        filtered_df = df.copy()
        if selected_cat != "الكل":
            filtered_df = filtered_df[filtered_df['Category'] == selected_cat]
        
        if search_query:
            filtered_df = filtered_df[filtered_df.apply(lambda r: r.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        st.markdown(f"### القائمة التفصيلية: {selected_cat}")
        # عرض البيانات بشكل احترافي مع التركيز على الوصف والكمية
        display_cols = [desc_col] + [c for c in filtered_df.columns if c not in [desc_col, 'Category', 'Source_File']]
        st.dataframe(filtered_df[display_cols], use_container_width=True, height=500)

    # رسم بياني مريح للعين
    st.divider()
    st.subheader("📈 نظرة عامة على حجم المجموعات")
    fig = px.bar(df['Category'].value_counts().reset_index(), 
                 x='index', y='Category', 
                 labels={'index':'المجموعة', 'Category':'عدد الأصناف'},
                 color='Category', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👋 النظام جاهز للعمل. من فضلك ارفع ملف إكسيل ببيانات المخزون في المستودع.")
