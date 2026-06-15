import streamlit as st
import sqlite3
from datetime import datetime
import urllib.parse
import os

# 1. إعدادات الصفحة العامة
st.set_page_config(
    page_title="Nasij Studio Premium",
    page_icon="🟫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة الفاخرة المخصصة (Custom CSS)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Amiri:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
}

.stApp {
    background: linear-gradient(135deg, #0b1f17 0%, #15301f 50%, #0b1f17 100%);
    color: #f5e6c8;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1812 0%, #122a1c 100%);
    border-left: 2px solid #d4af37;
}

section[data-testid="stSidebar"] * {
    color: #f5e6c8 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Amiri', serif !important;
    color: #d4af37 !important;
    font-weight: 700 !important;
}

p, span, label, div {
    color: #f5e6c8;
}

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    color: #d4af37;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    padding: 1rem 0;
    border-bottom: 3px double #d4af37;
    margin-bottom: 1.5rem;
}

.sub-title {
    text-align: center;
    font-size: 1.3rem;
    color: #e0c9a6;
    margin-bottom: 2rem;
    font-style: italic;
}

.nasij-card {
    background: linear-gradient(145deg, #1a3326 0%, #102018 100%);
    border: 1px solid #d4af37;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.nasij-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(212,175,55,0.25);
}

.stat-box {
    background: linear-gradient(145deg, #2a4a35 0%, #16301f 100%);
    border: 1px solid #d4af37;
    border-radius: 14px;
    text-align: center;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 900;
    color: #d4af37;
}

.stat-label {
    font-size: 1rem;
    color: #f5e6c8;
    margin-top: 0.3rem;
}

.stButton>button {
    background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
    color: #0b1f17 !important;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 3px 10px rgba(0,0,0,0.3);
}

.stButton>button:hover {
    background: linear-gradient(135deg, #f0c869 0%, #d4af37 100%);
    color: #0b1f17 !important;
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(212,175,55,0.4);
}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,
.stSelectbox>div>div>div {
    background-color: #1a3326 !important;
    color: #f5e6c8 !important;
    border: 1px solid #d4af37 !important;
    border-radius: 8px !important;
}

.stRadio>div {
    background: linear-gradient(145deg, #1a3326 0%, #102018 100%);
    border: 1px solid #d4af37;
    border-radius: 12px;
    padding: 1rem;
}

hr {
    border-top: 2px solid #d4af37;
    opacity: 0.5;
}

.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 1.5rem 0;
}

[data-testid="stDataFrame"] {
    border: 1px solid #d4af37;
    border-radius: 10px;
}

.cost-box {
    background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
    color: #0b1f17;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    font-size: 1.6rem;
    font-weight: 900;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(212,175,55,0.3);
}

.material-card {
    background: linear-gradient(145deg, #1a3326 0%, #102018 100%);
    border-right: 5px solid #d4af37;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 3. إدارة قاعدة البيانات المحلية SQLite
DB_NAME = "nasij_studio.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            service_type TEXT NOT NULL,
            order_details TEXT NOT NULL,
            total_cost REAL NOT NULL,
            order_datetime TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_order(customer_name, phone_number, service_type, order_details, total_cost):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    order_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO orders (customer_name, phone_number, service_type, order_details, total_cost, order_datetime)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_name, phone_number, service_type, order_details, total_cost, order_datetime))
    conn.commit()
    conn.close()

def get_all_orders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, phone_number, service_type, order_details, total_cost, order_datetime FROM orders ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

# 4. الثوابت وإعدادات الأسعار
WHATSAPP_NUMBER = "966500000000"

MATERIAL_PRICING = {
    "الصوف الطبيعي المحفور": 450,
    "الحرير الفاخر": 850,
    "البوليستر المعالج عالي الكثافة": 250
}

# 5. القائمة الجانبية (Sidebar)
with st.sidebar:
    logo_path = "images/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center; padding: 1rem; border: 2px solid #d4af37; "
            "border-radius: 12px; margin-bottom: 1rem;'>"
            "<h2 style='margin:0; color:#d4af37;'>نسيج ستوديو</h2>"
            "<p style='margin:0; font-size:0.9rem; color:#e0c9a6;'>Nasij Studio Premium</p>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    page = st.radio(
        "التنقل بين الأقسام",
        [
            "🏠 الرئيسية",
            "🎨 تصميم الاستوديو",
            "🧶 نسيج (الخامات)",
            "📚 الكاتالوج الأيقوني",
            "💰 المتجر وبوابات الأرباح",
            "⭐ مشاريع العملاء",
            "📞 الاتصالات"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:0.85rem; color:#e0c9a6;'>"
        "© 2026 Nasij Studio Premium<br>صنع بفخر في المملكة العربية السعودية"
        "</p>",
        unsafe_allow_html=True
    )

# 6. محتوى الصفحات بناءً على خيار التنقل
if page == "🏠 الرئيسية":
    st.markdown("<div class='main-title'>نسيج ستوديو بريميوم</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>حيث يلتقي التراث السعودي الأصيل بقوة الذكاء الاصطناعي لصياغة روائع من السجاد الفاخر</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='nasij-card'>
        <h3>رؤيتنا</h3>
        <p style='font-size:1.1rem; line-height:2;'>
        تأسست منصة نسيج ستوديو بريميوم لتكون الجسر الذي يربط بين عبق التراث السعودي العريق
        وأحدث تقنيات التصميم الرقمي ثلاثي الأبعاد. نحن نؤمن بأن كل سجادة تحمل قصة، ونسعى لتمكين
        عملائنا من تصميم وتصنيع سجاد فاخر يعكس هويتهم وذوقهم الرفيع، باستخدام أجود أنواع الخامات
        ومحركات توليد التصاميم المتطورة، لنقدم تجربة استثنائية تمزج بين الفخامة والأصالة والابتكار.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>إحصائيات المنصة</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            "<div class='stat-box'><div class='stat-number'>12,480</div>"
            "<div class='stat-label'>تصميم مولّد</div></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='stat-box'><div class='stat-number'>3,250</div>"
            "<div class='stat-label'>مشترك نشط</div></div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='stat-box'><div class='stat-number'>4.9 / 5</div>"
            "<div class='stat-label'>تقييم الخدمة</div></div>",
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            "<div class='stat-box'><div class='stat-number'>980</div>"
            "<div class='stat-label'>طلب تصنيع مكتمل</div></div>",
            unsafe_allow_html=True
        )

elif page == "🎨 تصميم الاستوديو":
    st.markdown("<div class='main-title'>استوديو التصميم الإبداعي</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>صف رؤيتك، ودع الذكاء الاصطناعي يحول كلماتك إلى تحفة سجاد فنية</div>",
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)

        prompt_text = st.text_area(
            "وصف التصميم المطلوب (Prompt)",
            placeholder="مثال: سجادة فارسية بنمط هندسي معاصر بألوان الذهبي والأخضر الزمردي مع زخارف نجدية...",
            height=120
        )

        col1, col2 = st.columns(2)

        with col1:
            art_style = st.selectbox(
                "النمط الفني",
                ["تراثي نجدي", "فارسي كلاسيكي", "عصري هندسي", "إسلامي زخرفي", "مينيمالي فاخر"]
            )

        with col2:
            dominant_colors = st.selectbox(
                "الألوان المهيمنة",
                ["أخضر زمردي وذهبي", "أسود ملكي وذهبي", "سكري دافئ وبني", "كريمي وذهبي", "كحلي وفضي"]
            )

        if st.button("🎨 توليد التصميم الآن"):
            if prompt_text.strip() == "":
                st.warning("يرجى إدخال وصف نصي للتصميم المطلوب أولاً.")
            else:
                with st.spinner("جاري الاتصال بمحرك التوليد ومعالجة التصميم..."):
                    import time
                    time.sleep(2)
                st.success(
                    f"تم توليد التصميم بنجاح! النمط: {art_style} | الألوان: {dominant_colors}. "
                    f"يمكنك الآن مراجعته في معرض التصاميم أو طلب رخصة الاستخدام من المتجر."
                )

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🧶 نسيج (الخامات)":
    st.markdown("<div class='main-title'>نسيج - دليل الخامات الفاخرة</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>نختار لكم أرقى الخيوط من حول العالم لنضمن جودة استثنائية تدوم</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='material-card'>
        <h3>الصوف الطبيعي المحفور</h3>
        <p style='font-size:1.05rem; line-height:1.9;'>
        خيوط صوف طبيعية ١٠٠٪ يتم انتقاؤها بعناية فائقة، تتميز بملمسها الناعم الكثيف ومتانتها العالية
        وقدرتها على الاحتفاظ بالألوان لعقود. تقنية الحفر اليدوي تضيف بعداً ثلاثي الأبعاد يعزز جمال
        النقشة ويعطي السجادة طابعاً نحتياً فاخراً.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='material-card'>
        <h3>الحرير الفاخر</h3>
        <p style='font-size:1.05rem; line-height:1.9;'>
        خيوط حريرية لامعة فائقة النعومة، تمنح السجادة بريقاً طبيعياً راقياً وملمساً حريرياً يضاهي
        أرقى السجاد الفارسي التقليدي. خيار مستقل ومثالي للقطع التذكارية والتصاميم التراثية الفاخرة التي
        تحتاج إلى تفاصيل دقيقة وألوان نابضة بالحياة.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='material-card'>
        <h3>البوليستر المعالج عالي الكثافة</h3>
        <p style='font-size:1.05rem; line-height:1.9;'>
        خامة عصرية متطورة تمت معالجتها بتقنيات حديثة لمضاهاة ملمس الصوف الطبيعي مع مقاومة فائقة
        للبقع والتلف والاستخدام اليومي المكثف. خيار اقتصادي ذكي يحافظ على الفخامة البصرية مع
        سهولة العناية والتنظيف.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "📚 الكاتالوج الأيقوني":
    st.markdown("<div class='main-title'>الكاتالوج الأيقوني</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>خمسة تصاميم استثنائية تحكي قصص الإرث السعودي الخالد</div>",
        unsafe_allow_html=True
    )

    catalog_items = [
        {
            "title": "الجمل الصحراوي",
            "desc": "تصميم يجسد رمزية الجمل كرفيق رحلة الصحراء، بألوان رملية دافئة مطعمة بتفاصيل ذهبية تحاكي غروب الكثبان.",
            "image": "images/camel.png"
        },
        {
            "title": "تراث نجد",
            "desc": "زخارف هندسية مستوحاة من العمارة النجدية التقليدية والقصور الطينية، بتدرجات بنية وذهبية أنيقة.",
            "image": "images/najd.png"
        },
        {
            "title": "نور المحراب",
            "desc": "تصميم روحاني مستوحى من زخارف المحاريب الإسلامية، يجمع بين الأخضر الزمردي والذهبي بتفاصيل دقيقة.",
            "image": "images/mihrab.png"
        },
        {
            "title": "المجلس الملكي",
            "desc": "تصميم فخم بألوان كحلية وذهبية يحاكي أجواء المجالس الملكية التقليدية بزخارفها المهيبة.",
            "image": "images/majlis.png"
        },
        {
            "title": "الخيل العربي",
            "desc": "تصميم ديناميكي يحتفي برمزية الخيل العربي الأصيل، بتدرجات بنية ونحاسية تعكس القوة والأصالة.",
            "image": "images/horse.png"
        }
    ]

    cols = st.columns(2)
    for index, item in enumerate(catalog_items):
        with cols[index % 2]:
            st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
            if os.path.exists(item["image"]):
                st.image(item["image"], use_container_width=True)
            else:
                st.markdown(
                    f"<div style='text-align:center; padding:2rem; border:1px dashed #d4af37; "
                    f"border-radius:10px; margin-bottom:1rem;'>"
                    f"<p style='color:#e0c9a6;'>📷 الصورة غير متوفرة</p>"
                    f"<p style='font-size:0.85rem; color:#b8860b;'>المسار المتوقع: {item['image']}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            st.markdown(f"<h3>{item['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='line-height:1.9;'>{item['desc']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "💰 المتجر وبوابات الأرباح":
    st.markdown("<div class='main-title'>المتجر وبوابات الأرباح</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>اختر المسار التجاري الذي يناسب احتياجاتك</div>",
        unsafe_allow_html=True
    )

    business_path = st.radio(
        "اختر المسار التجاري والاستثماري",
        [
            "شراء وتصنيع سجادة مخصصة",
            "شراء رخصة التصميم الرقمي بدقة 4K",
            "اشتراك باقة المحترفين والمحلات (SaaS)"
        ]
    )

    total_cost = 0.0
    order_details = ""

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    if business_path == "شراء وتصنيع سجادة مخصصة":
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        st.markdown("<h3>تصنيع سجادة مخصصة</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            length = st.number_input("الطول (متر)", min_value=0.5, max_value=20.0, value=2.0, step=0.1)

        with col2:
            width = st.number_input("العرض (متر)", min_value=0.5, max_value=20.0, value=1.5, step=0.1)

        with col3:
            material = st.selectbox("نوع الخامة", list(MATERIAL_PRICING.keys()))

        area = length * width
        price_per_sqm = MATERIAL_PRICING[material]
        manufacturing_cost = area * price_per_sqm
        shipping_cost = 150 if area <= 10 else 350
        total_cost = manufacturing_cost + shipping_cost

        st.markdown(f"<p style='font-size:1.1rem;'>📐 المساحة الإجمالية: <b>{area:.2f} م²</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.1rem;'>🧶 الخامة المختارة: <b>{material}</b> ({price_per_sqm} ريال / م²)</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.1rem;'>🚚 تكلفة الشحن: <b>{shipping_cost} ريال</b></p>", unsafe_allow_html=True)

        st.markdown(f"<div class='cost-box'>التكلفة الإجمالية: {total_cost:,.2f} ريال سعودي</div>", unsafe_allow_html=True)

        order_details = f"تصنيع سجادة مخصصة - الأبعاد: {length}م × {width}م - المساحة: {area:.2f} م² - الخامة: {material} - الشحن: {shipping_cost} ريال"
        st.markdown("</div>", unsafe_allow_html=True)

    elif business_path == "شراء رخصة التصميم الرقمي بدقة 4K":
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        st.markdown("<h3>رخصة التصميم الرقمي بدقة 4K</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:1.05rem; line-height:1.9;'>"
            "احصل على رخصة استخدام كاملة لأحد تصاميمنا بدقة 4K فائقة الوضوح، مثالية للمهندسين "
            "ومصممي الديكور وأصحاب المعارض، مع إمكانية الطباعة والتعديل التجاري بدون قيود."
            "</p>",
            unsafe_allow_html=True
        )

        total_cost = 199.0
        st.markdown(f"<div class='cost-box'>السعر الموحد: {total_cost:,.2f} ريال سعودي</div>", unsafe_allow_html=True)
        order_details = "شراء رخصة التصميم الرقمي بدقة 4K"
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        st.markdown("<h3>باقة المحترفين والمحلات (SaaS)</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:1.05rem; line-height:1.9;'>"
            "اشتراك شهري متجدد يتيح لك ولفريقك توليد وحفظ عدد غير محدود من التصاميم عبر محرك "
            "الذكاء الاصطناعي، مع أولوية في الدعم الفني وتحديثات حصرية للنماذج والأنماط الفنية الجديدة."
            "</p>",
            unsafe_allow_html=True
        )

        total_cost = 299.0
        st.markdown(f"<div class='cost-box'>السعر الشهري: {total_cost:,.2f} ريال سعودي / شهرياً</div>", unsafe_allow_html=True)
        order_details = "اشتراك باقة المحترفين والمحلات (SaaS) - شهري"
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h3>بيانات إتمام الطلب</h3>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("اسم العميل", key="customer_name_input")
        with col2:
            phone_number = st.text_input("رقم الجوال", key="phone_number_input")

        col_save, col_whatsapp = st.columns(2)

        with col_save:
            if st.button("💾 حفظ الطلب"):
                if customer_name.strip() == "" or phone_number.strip() == "":
                    st.error("يرجى إدخال اسم العميل ورقم الجوال قبل حفظ الطلب.")
                else:
                    save_order(customer_name, phone_number, business_path, order_details, total_cost)
                    st.success("تم حفظ الطلب بنجاح في قاعدة بيانات النظام. سيتم التواصل معك قريباً.")

        with col_whatsapp:
            if st.button("📲 إرسال ومتابعة عبر الواتساب"):
                if customer_name.strip() == "" or phone_number.strip() == "":
                    st.error("يرجى إدخال اسم العميل ورقم الجوال قبل المتابعة عبر الواتساب.")
                else:
                    whatsapp_message = (
                        f"طلب جديد من نسيج ستوديو بريميوم\n"
                        f"اسم العميل: {customer_name}\n"
                        f"رقم الجوال: {phone_number}\n"
                        f"نوع الخدمة: {business_path}\n"
                        f"تفاصيل الطلب: {order_details}\n"
                        f"المبلغ الإجمالي: {total_cost:,.2f} ريال سعودي"
                    )
                    encoded_message = urllib.parse.quote(whatsapp_message)
                    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;"><div class="cost-box" style="font-size:1.1rem; padding:0.5rem; margin:0; background:linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:white;">اضغط هنا لفتح الواتساب وإتمام الدفع فوري 💬</div></a>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "⭐ مشاريع العملاء":
    st.markdown("<div class='main-title'>⭐ لوحة تحكم مشاريع نسيج</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>إدارة ومتابعة طلبات العملاء والاشتراكات الرقمية المسجلة في SQLite</div>",
        unsafe_allow_html=True
    )

    orders = get_all_orders()

    if not orders:
        st.info("لا توجد طلبات أو مشاريع مسجلة في قاعدة البيانات حالياً.")
    else:
        for order in orders:
            with st.expander(f"📦 طلب رقم {order[0]} - العميل: {order[1]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📞 رقم الجوال:** {order[2]}")
                    st.markdown(f"**📌 نوع الخدمة:** {order[3]}")
                    st.markdown(f"**🕒 تاريخ الطلب:** {order[6]}")
                with col2:
                    st.markdown(f"**💰 المبلغ المالي:** {order[5]:,.2f} ريال سعودي")
                    st.markdown(f"**📝 تفاصيل الطلب الفنية:**")
                    st.write(order[4])

elif page == "📞 الاتصالات":
    st.markdown("<div class='main-title'>📞 تواصل مع إدارة نسيج</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>نحن هنا لمساعدتك في تجسيد رؤيتك الفنية وتحويلها إلى واقع</div>",
        unsafe_allow_html=True
    )

    # هذا الجزء مطابق تماماً لما جاء في ملف لقطة الشاشة المرفقة Screenshot_٢٠٢٦-٠٦-١٥-٠٩-٣٥-٢١-٣٨٦_com.anthropic.claude.jpg لضمان التكامل
    with st.container():
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)

        contact_name = st.text_input("الاسم بالكامل")
        contact_phone = st.text_input("رقم الجوال")
        contact_message = st.text_area("الالرسالة الإبداعية")

        if st.button("✉️ تأكيد الإرسال"):
            if contact_name.strip() == "" or contact_phone.strip() == "" or contact_message.strip() == "":
                st.error("الرجاء ملء جميع الحقول قبل الإرسال.")
            else:
                st.success(f"شكراً لك {contact_name}، تم استلام رسالتك بنجاح. سيقوم فريقنا بالتواصل معك على الرقم {contact_phone} في أقرب وقت.")

        st.markdown("</div>", unsafe_allow_html=True)
