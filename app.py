import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Korra Enterprise AI", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stDataFrame { border: 1px solid #004a87; border-radius: 10px; }
    .main-title { background: #004a87; color: white; padding: 20px; border-radius: 15px; text-align: center; }
    .search-box { border: 2px solid #004a87 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. قاموس الذكاء الاصطناعي الموسع (دليل المهندس)
AI_GUIDE = {
    "كابل": "نقل وتوزيع الطاقة الكهربائية في المواقع والمباني.",
    "محبس": "التحكم في تدفق المياه، سواء في أنظمة الحريق أو التبريد المركزي.",
    "ماسورة": "مسارات لنقل السوائل والغازات بضغوط وأقطار مختلفة.",
    "قاطع": "تأمين اللوحات الكهربائية ضد الارتفاع المفاجئ في التيار.",
    "طلمبة": "وحدات ضخ ميكانيكية لتدوير المياه في الشبكات.",
    "خرسانة": "الأساس الإنشائي للمباني، تختلف رتبتها حسب نوع الإضافات.",
    "حديد": "عنصر التسليح الأساسي لمقاومة أحمال الشد في المنشآت."
}

# 3. محرك قراءة وتنظيف البيانات
@st.cache_data
def get_clean_data():
    if not os.path.exists('data.xlsx'):
        return None
    try:
        # قراءة الشيت مع التأكد من عدم ضياع أي بيانات
        df = pd.read_excel('data.xlsx', engine='openpyxl')
        # تنظيف أسامي الأعمدة المكررة أو الفارغة
        df.columns = [str(c).strip() if not pd.isna(c) else f"Unnamed_{i}" for i, c in enumerate(df.columns)]
        return df.fillna("غير مسجل")
    except:
        return None

# 4. بناء الواجهة
st.markdown('<div class="main-title"><h1>🔮 نظام Korra للبحث الذكي عن الأصول</h1></div>', unsafe_allow_html=True)

df = get_clean_data()

if df is not None:
    # شريط البحث العلوي
    search_query = st.text_input("🎯 ابحث عن أي خامة أو كود أو وظيفة هندسية:", placeholder="مثلاً: ما هو استخدام محابس السكين؟")

    if search_query:
        # أ) محرك الذكاء الاصطناعي للوصف
        with st.expander("📝 التحليل الهندسي للخامة (AI Insights)", expanded=True):
            found_desc = False
            for key, desc in AI_GUIDE.items():
                if key in search_query:
                    st.info(f"**الاستخدام الشائع:** {desc}")
                    found_desc = True
                    break
            if not found_desc:
                st.write("يبحث النظام حالياً في الشيت عن أقرب تطابق فني...")

        # ب) محرك البحث العميق في الجدول (Deep Filter)
        # بيبحث في كل كلمة في الجملة بشكل منفصل لضمان أعلى دقة
        keywords = search_query.split()
        mask = df.apply(lambda row: all(any(k.lower() in str(val).lower() for val in row) for k in keywords), axis=1)
        results = df[mask]

        # ج) عرض النتائج
        st.divider()
        st.subheader(f"📍 النتائج المطابقة من واقع البيانات المرفوعة ({len(results)} نتيجة)")
        
        if not results.empty:
            # عرض الجدول بشكل كامل وواضح
            st.dataframe(
                results, 
                use_container_width=True, 
                height=500,
                column_config={"Source": st.column_config.TextColumn("ملف المصدر", width="medium")}
            )
            
            # ميزة التحميل
            csv = results.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل النتائج كملف Excel", csv, "search_results.csv", "text/csv")
        else:
            st.warning("لم نجد نتائج مطابقة تماماً في الشيت. جرب كتابة اسم الخامة بشكل مختصر (مثل: كابل بدلاً من كابلات).")

else:
    st.error("❌ ملف 'data.xlsx' مش موجود! ارفع الملف على GitHub الأول عشان أقدر أطلعلك نتايج حقيقية.")
