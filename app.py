import streamlit as st
import pandas as pd
import os
from difflib import get_close_matches

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Korra AI Search", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(90deg, #004a87, #002d50); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .info-card { background: #f0f7ff; padding: 15px; border-radius: 10px; border-right: 5px solid #004a87; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. قاموس الذكاء الاصطناعي للهوية الهندسية (Knowledge Base)
# ده "المخ" اللي بيعرف الخامة بتستخدم في إيه
AI_KNOWLEDGE = {
    "كابل": "نقل الطاقة الكهربائية وتغذية اللوحات الرئيسية والفرعية.",
    "محبس": "التحكم في تدفق السوائل (مياه، حريق، تبريد) ومنع الارتجاع.",
    "ماسورة": "نقل الموائع مثل مياه التبريد (Chilled Water) أو مكافحة الحريق.",
    "قاطع": "حماية الدوائر الكهربائية من زيادة الحمل (Overload) أو القصر (Short Circuit).",
    "طلمبة": "رفع ضغط المياه أو السوائل لضمان وصولها للنقاط المطلوبة.",
    "خرسانة": "الأعمال الإنشائية والأساسات والهياكل الخرسانية للمباني.",
    "حديد": "تسليح العناصر الإنشائية لزيادة قدرتها على تحمل أحمال الشد.",
    "محول": "تحويل الجهد الكهربائي من المتوسط إلى المنخفض لتشغيل المعدات."
}

# 3. محرك البحث الذكي
def smart_search(query, dataframe):
    query = query.lower()
    # تنظيف الأعمدة من الأسماء المكررة
    df_clean = dataframe.loc[:, ~dataframe.columns.duplicated()]
    
    # البحث عن كلمات دلالية في القاموس
    usage = "لم يتم العثور على وصف دقيق في قاعدة البيانات، ولكن إليك النتائج من الشيت:"
    for key in AI_KNOWLEDGE:
        if key in query:
            usage = AI_KNOWLEDGE[key]
            break
            
    # البحث المرن في الشيت (Fuzzy Matching)
    # بيبحث في كل الصفوف والأعمدة عن أي كلمة قريبة من الاستعلام
    mask = df_clean.apply(lambda row: row.astype(str).str.contains(query.split()[0], case=False).any(), axis=1)
    results = df_clean[mask]
    
    return usage, results

# 4. بناء التطبيق
st.markdown('<div class="main-header"><h1 style="color:white; text-align:center;">🔮 محرك بحث Korra الذكي للأصول</h1></div>', unsafe_allow_html=True)

# قراءة الملف (data.xlsx)
if os.path.exists('data.xlsx'):
    try:
        df = pd.read_excel('data.xlsx', engine='openpyxl')
        
        search_query = st.text_input("🔍 اكتب اسم الخامة (بالعربي أو الإنجليزي) لتعرف استخدامها وأين توجد:", placeholder="مثلاً: كابل، محبس، طلمبة...")
        
        if search_query:
            usage, results = smart_search(search_query, df)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div class="info-card">
                    <h4 style="color:#004a87;">💡 الاستخدام الهندسي:</h4>
                    <p style="font-size:18px;">{usage}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.subheader("📍 النتائج المطابقة في المخزن:")
                if not results.empty:
                    st.success(f"وجدنا {len(results)} سجل مطابق لطلبك.")
                    st.dataframe(results, use_container_width=True)
                else:
                    st.warning("لم نجد سجلات مطابقة تماماً في الشيت، حاول كتابة كلمة أبسط.")
        else:
            st.info("👋 ابدأ بكتابة اسم أي خامة في خانة البحث أعلاه.")
            
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
else:
    st.warning("⚠️ ملف data.xlsx غير موجود. من فضلك ارفعه على GitHub ليعمل محرك البحث.")
