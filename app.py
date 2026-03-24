import streamlit as st

# 1. إعدادات الواجهة الموسوعية
st.set_page_config(page_title="Korra Engineering Wiki", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main-header { background: #004a87; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
    .material-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; border-right: 8px solid #ffb800; }
    .material-title { color: #004a87; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات الموسوعة (تقدر تزود عليها براحتك)
materials_db = [
    {
        "name": "كابلات الجهد المتوسط (MV Cables)",
        "use": "تستخدم لنقل الطاقة من محطات التوزيع الرئيسية إلى المحولات الفرعية في المشروعات الكبرى.",
        "image": "https://p.globalsources.com/IMAGES/PDT/BIG/311/B1187424311.jpg",
        "category": "⚡ كهرباء"
    },
    {
        "name": "محابس السكين (Gate Valves)",
        "use": "تستخدم في أنظمة الحريق ومحطات المياه للتحكم الكامل في تدفق السوائل (فتح أو غلق تام).",
        "image": "https://5.imimg.com/data5/SELLER/Default/2022/9/XF/OI/XQ/4491703/cast-iron-gate-valve-500x500.jpg",
        "category": "🔧 ميكانيكا"
    },
    {
        "name": "المواسير المعزولة (Pre-insulated Pipes)",
        "use": "تستخدم في أنظمة التبريد المركزي (District Cooling) للحفاظ على درجة حرارة المياه وتقليل الفقد الحراري.",
        "image": "https://www.isoplus.org/media/1336/isoplus-pre-insulated-pipes.jpg",
        "category": "🔧 ميكانيكا"
    }
]

# 3. بناء الصفحة
st.markdown('<div class="main-header"><h1>📚 موسوعة Korra للأصول الهندسية</h1><p>دليلك الشامل لاستخدامات ومواصفات الخامات</p></div>', unsafe_allow_html=True)

# قائمة جانبية للتصفية
st.sidebar.header("🔍 تصفح حسب القسم")
cat_filter = st.sidebar.selectbox("اختر القسم:", ["الكل", "⚡ كهرباء", "🔧 ميكانيكا"])

search = st.sidebar.text_input("ابحث عن خامة محددة:")

# عرض الخامات
for mat in materials_db:
    if (cat_filter == "الكل" or mat['category'] == cat_filter) and (search.lower() in mat['name'].lower()):
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(mat['image'], use_container_width=True)
            with col2:
                st.markdown(f"""
                <div class="material-card">
                    <div class="material-title">{mat['name']}</div>
                    <p style="color: #666; font-size: 14px;"><b>القسم:</b> {mat['category']}</p>
                    <p><b>الاستخدام الأساسي:</b> {mat['use']}</p>
                    <button style="background:#004a87; color:white; border:none; padding:8px 15px; border-radius:5px;">قراءة المواصفات الفنية</button>
                </div>
                """, unsafe_allow_html=True)

if not materials_db:
    st.info("لم يتم العثور على خامات تطابق بحثك.")
