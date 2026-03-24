import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- 1. إعدادات الواجهة الاحترافية (UI/UX) ---
st.set_page_config(page_title="Korra Inventory Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #f4f7f9; }
    .stat-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center; border-bottom: 5px solid #004a87;
    }
    .stat-value { font-size: 32px; font-weight: bold; color: #004a87; margin: 10px 0; }
    .stat-label { font-size: 16px; color: #555; font-weight: 600; }
    .main-title { background: #004a87; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك معالجة وتصنيف البيانات ---
class KorraSmartEngine:
    @staticmethod
    def classify(desc):
        desc = str(desc).lower()
        if any(x in desc for x in ['cable', 'wire', 'كهربا', 'كابل', 'سلك']): return '⚡ الكهرباء'
        if any(x in desc for x in ['pipe', 'valve', 'pump', 'محبس', 'ماسور']): return '🔧 الميكانيكا'
        if any(x in desc for x in ['steel', 'cement', 'حديد', 'خرسان']): return '🏗️ المدني'
        return '📦 أصناف عامة'

    @staticmethod
    @st.cache_data
    def get_inventory():
        files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
        if not files: return None
        
        all_data = []
        for f in files:
            try:
                # محاولة قراءة الملف مع تجاهل أخطاء التنسيق
                df = pd.read_excel(f, engine='openpyxl').fillna(0)
                df['Source'] = f
                all_data.append(df)
            except: continue
        
        if not all_data: return None
        full_df = pd.concat(all_data, ignore_index=True)
        
        # تحديد عمود الوصف والكمية (بافتراض الترتيب الشائع)
        desc_col = full_df.columns[1] if len(full_df.columns) > 1 else full_df.columns[0]
        # البحث عن عمود يحتوي على كلمة "كمية" أو "Qty" أو "Balance"
        qty_col = next((c for c in full_df.columns if any(k in str(c).lower() for k in ['qty', 'كمي', 'bal', 'stock'])), None)
        
        full_df['Group'] = full_df[desc_col].apply(KorraSmartEngine.classify)
        return full_df, desc_col, qty_col

# --- 3. بناء لوحة التحكم المرئية ---
st.markdown('<div class="main-header"><h1>🔮 Korra Asset Dashboard</h1><p>نظرة شاملة على المتاح في المخازن</p></div>', unsafe_allow_html=True)

inventory_data = KorraSmartEngine.get_inventory()

if inventory_data:
    df, desc_name, qty_name = inventory_data
    
    # صف البطاقات العلوية (المجموعات)
    st.subheader("📊 حالة المخزون الحالية")
    groups = df['Group'].value_counts()
    cols = st.columns(len(groups))
    
    for i, (group_name, count) in enumerate(groups.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{group_name}</div>
                    <div class="stat-value">{count}</div>
                    <div style="color:#888;">صنف مسجل</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # قسم التفاصيل الذكي
    col_chart, col_list = st.columns([1, 2])
    
    with col_chart:
        st.subheader("📈 توزيع المجموعات")
        # حل مشكلة ValueError بضمان وجود بيانات قبل الرسم
        chart_data = groups.reset_index()
        chart_data.columns = ['المجموعة', 'العدد']
        fig = px.pie(chart_data, values='العدد', names='المجموعة', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    with col_list:
        st.subheader("📋 مراجعة المتاح")
        selected_grp = st.selectbox("اختر مجموعة لعرض تفاصيلها:", ["الكل"] + list(groups.index))
        
        filtered = df if selected_grp == "الكل" else df[df['Group'] == selected_grp]
        
        # عرض أهم الأعمدة فقط للراحة البصرية
        important_cols = [desc_name]
        if qty_name: important_cols.append(qty_name)
        important_cols.append('Source')
        
        st.dataframe(filtered[important_cols], use_container_width=True, height=400)

else:
    st.info("👋 بانتظار رفع ملفات الإكسيل (data.xlsx) للبدء في تحليل المجموعات.")
