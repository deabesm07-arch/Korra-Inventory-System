import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والستايل الاحترافي
st.set_page_config(page_title="Korra Asset Intel", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main-title { color: #004a87; text-align: center; font-size: 3rem; font-weight: 800; margin-bottom: 20px; border-bottom: 4px solid #ffb800; padding-bottom: 10px; }
    .asset-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 15px; border-right: 10px solid #004a87; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: 0.3s; }
    .asset-card:hover { transform: scale(1.01); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
    .label { color: #888; font-size: 14px; margin-bottom: 5px; }
    .value { color: #333; font-size: 18px; font-weight: 600; }
    .usage-badge { background: #e3f2fd; color: #004a87; padding: 5px 15px; border-radius: 20px; font-size: 14px; display: inline-block; margin-top: 10px; }
    .metric { background: #fff9c4; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #fbc02d; }
    </style>
""", unsafe_allow_html=True)

# 2. دليل الاستخدامات الذكي (AI Brain)
AI_KNOWLEDGE = {
    "كابل": "⚡ تستخدم لنقل وتوزيع الطاقة الكهربائية في المواقع الإنشائية.",
    "محبس": "🔧 صمام تحكم لغلق أو فتح مسارات المياه وأنظمة الإطفاء.",
    "ماسورة": "🏗️ خطوط نقل الموائع، مياه تبريد، أو شبكات صرف وضغط.",
    "طلمبة": "🔄 وحدة ميكانيكية لضخ وتدوير السوائل بضغوط عالية.",
    "قاطع": "🛡️ حماية اللوحات من الالتماس الكهربائي والأحمال الزائدة."
}

# 3. دالة البحث الذكي
def get_ai_usage(query):
    for key in AI_KNOWLEDGE:
        if key in query: return AI_KNOWLEDGE[key]
    return "🛠️ خامة هندسية مخصصة للاستخدام في مشاريع كورا إنيرجي."

@st.cache_data
def load_and_fix_data():
    if os.path.exists('data.xlsx'):
        df = pd.read_excel('data.xlsx', engine='openpyxl')
        df.columns = [str(c).strip() for c in df.columns] # تنظيف الأعمدة
        return df.fillna("غير متوفر")
    return None

# 4. واجهة المستخدم
st.markdown('<div class="main-title">Korra Asset Intel 💎</div>', unsafe_allow_html=True)

df = load_and_fix_data()

if df is not None:
    # شريط بحث احترافي
    search_query = st.text_input("🔍 ابحث عن (خامة، كود، أو وصف) بخاصية الربط الذكي:", placeholder="اكتب هنا مثلاً: كابلات جهد متوسط..")
    
    if search_query:
        # فلترة البيانات بذكاء (البحث في كل الأعمدة)
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.markdown(f"### 🎯 تم العثور على ({len(results)}) سجل مطابق")
            
            # عرض النتائج في شكل كروت
            for _, row in results.iterrows():
                # محاولة لقط أسامي الأعمدة مهما كانت (كود، اسم، كمية)
                name = row.get('Description', row.get('Item Name', row.get('البيان', 'خامة غير معروفة')))
                code = row.get('Item Code', row.get('الكود', row.get('Material Number', 'N/A')))
                qty = row.get('Quantity', row.get('الكمية', row.get('Balance', '0')))
                
                with st.container():
                    st.markdown(f"""
                    <div class="asset-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 2;">
                                <div class="label">اسم الخامة / التوصيف</div>
                                <div class="value" style="font-size: 22px; color: #004a87;">{name}</div>
                                <div class="usage-badge">{get_ai_usage(str(name))}</div>
                            </div>
                            <div style="flex: 1; display: flex; flex-direction: column; gap: 10px;">
                                <div class="metric">
                                    <div class="label">الكود الفني</div>
                                    <div class="value">{code}</div>
                                </div>
                                <div class="metric" style="background: #e8f5e9; border-color: #4caf50;">
                                    <div class="label">الرصيد المتاح</div>
                                    <div class="value" style="color: #2e7d32;">{qty}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("لم يتم العثور على نتائج. حاول تبسيط كلمات البحث.")
    else:
        st.info("💡 جرب البحث عن كلمة 'كابل' أو 'محبس' لمشاهدة العرض الاحترافي.")
else:
    st.error("ملف data.xlsx غير موجود على GitHub.")
