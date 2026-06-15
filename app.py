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

# 2. تصميم الواجهة الفاخرة المخصصة والمعدلة للجوال (إصلاح خطوط الـ CSS المتداخلة)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Amiri:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

.stApp {
    background: linear-gradient(135deg, #0b1f17 0%, #15301f 50%, #0b1f17 100%);
    color: #f5e6c8;
}

/* حل مشكلة الخط العمودي الأصفر المتداخل الممتد على الشاشة */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1812 0%, #122a1c 100%) !important;
    border-left: none !important;
    border-right: none !important;
    box-shadow: -2px 0px 10px rgba(0,0,0,0.5);
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
    font-size: 2.2rem;
    font-weight: 900;
    color: #d4af37;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    padding: 0.5rem 0;
    border-bottom: 3px double #d4af37;
    margin-bottom: 1rem;
}

.sub-title {
    text-align: center;
    font-size: 1.1rem;
    color: #e0c9a6;
    margin-bottom: 1.5rem;
    font-style: italic;
}

.nasij-card {
    background: linear-gradient(145deg, #1a3326 0%, #102018 100%);
    border: 1px solid #d4af37;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.stat-box {
    background: linear-gradient(145deg, #2a4a35 0%, #16301f 100%);
    border: 1px solid #d4af37;
    border-radius: 14px;
    text-align: center;
    padding: 1rem;
    margin-bottom: 0.8rem;
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 900;
    color: #d4af37;
}

.stat-label {
    font-size: 0.9rem;
    color: #f5e6c8;
}

.stButton>button {
    background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
    color: #0b1f17 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 700 !important;
    width: 100%;
}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,
.stSelectbox>div>div>div {
    background-color: #1a3326 !important;
    color: #f5e6c8 !important;
    border: 1px solid #d4af37 !important;
    border-radius: 8px !important;
    text-align: right;
}

.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 1rem 0;
}

.cost-box {
    background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
    color: #0b1f17;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    font-size: 1.3rem;
    font-weight: 900;
    margin: 1rem 0;
}

.material-card {
    background: linear-gradient(145deg, #1a3326 0%, #102018 100%);
    border-right: 5px solid #d4af37;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.8rem;
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
    st.markdown(
        "<div style='text-align:center; padding: 0.5rem; border: 2px solid #d4af37; "
        "border-radius: 12px; margin-bottom: 1rem;'>"
        "<h3 style='margin:0; color:#d4af37;'>نسيج ستوديو</h3>"
        "<p style='margin:0; font-size:0.8rem; color:#e0c9a6;'>Nasij Studio Premium</p>"
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
        "<p style='text-align:center; font-size:0.8rem; color:#e0c9a6;'>"
        "© 2026 Nasij Studio Premium<br>صنع بفخر في المملكة العربية السعودية"
        "</p>",
        unsafe_allow_html=True
    )

# 6. محتوى الصفحات
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
        <p style='font-size:1rem; line-height:1.8;'>
        تأسست منصة نسيج ستوديو بريميوم لتكون الجسر الذي يربط بين عبق التراث السعودي العريق
        وأحدث تقنيات التصميم الرقمي ثلاثي الأبعاد. نحن نؤمن بأن كل سجادة تحمل قصة، ونسعى لتمكين
        عملائنا من تصميم وتصنيع سجاد يعكس هويتهم وذوقهم الرفيع.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stat-box'><div class='stat-number'>12,480</div><div class='stat-label'>تصميم مولّد</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-box'><div class='stat-number'>4.9 / 5</div><div class='stat-label'>تقييم الخدمة</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stat-box'><div class='stat-number'>3,250</div><div class='stat-label'>مشترك نشط</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-box'><div class='stat-number'>980</div><div class='stat-label'>طلب مكتمل</div></div>", unsafe_allow_html=True)

elif page == "🎨 تصميم الاستوديو":
    st.markdown("<div class='main-title'>استوديو التصميم الإبداعي</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>صف رؤيتك، ودع الذكاء الاصطناعي يحول كلماتك إلى تحفة سجاد حقيقية وثلاثية الأبعاد</div>",
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)

        prompt_text = st.text_area(
            "وصف التصميم المطلوب (Prompt)",
            placeholder="مثال: سجادة فاخرة بنمط هندسي معاصر بألوان الذهبي والأخضر الزمردي وزخارف نجدية ثلاثية الأبعاد...",
            height=100
        )

        col1, col2 = st.columns(2)
        with col1:
            art_style = st.selectbox("النمط الفني", ["تراثي نجدي", "فارسي كلاسيكي", "عصري هندسي", "إسلامي زخرفي", "مينيمالي فاخر"])
        with col2:
            dominant_colors = st.selectbox("الألوان المهيمنة", ["أخضر زمردي وذهبي", "أسود ملكي وذهبي", "سكري دافئ وبني", "كريمي وذهبي"])

        if st.button("🎨 توليد وتصميم السجادة الآن"):
            if prompt_text.strip() == "":
                st.warning("يرجى إدخال وصف نصي للتصميم المطلوب أولاً.")
            else:
                with st.spinner("🧠 يقوم الذكاء الاصطناعي بنسج وتوليد سجادتك الفاخرة الآن..."):
                    search_prompt = f"Luxurious 3D carpet rug, {prompt_text}, {art_style} style, {dominant_colors} theme, hyperrealistic textile texture, 4k"
                    encoded_prompt = urllib.parse.quote(search_prompt)
                    image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=800&height=800&nologo=true"
                    
                    st.image(image_url, caption=f"التصميم المولد: {art_style} ({dominant_colors})", use_container_width=True)
                    st.success("✨ تم توليد التصميم الرقمي بنجاح! يمكنك حفظ الصورة أو طلب تصنيعها من المتجر.")

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🧶 نسيج (الخامات)":
    st.markdown("<div class='main-title'>نسيج - دليل الخامات الفاخرة</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='material-card'><h3>الصوف الطبيعي المحفور</h3><p>خيوط صوف طبيعية ١٠٠٪ يتم انتقاؤها بعناية فائقة، تتميز بملمسها الناعم الكثيف وتقنية الحفر اليدوي ثلاثي الأبعاد.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='material-card'><h3>الحرير الفاخر</h3><p>خيوط حريرية لامعة فائقة النعومة، تمنح السجادة بريقاً طبيعياً راقياً يضاهي أرقى قطع السجاد الملكي.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='material-card'><h3>البوليستر المعالج عالي الكثافة</h3><p>خامة عصرية متطورة تمت معالجتها بتقنيات حديثة لمقاومة البقع والتلف والاستخدام اليومي المكثف.</p></div>", unsafe_allow_html=True)

elif page == "📚 الكاتالوج الأيقوني":
    st.markdown("<div class='main-title'>الكاتالوج الأيقوني</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>استكشف روائعنا المستوحاة من الأصالة والهوية الحية</div>", unsafe_allow_html=True)

    catalog_items = [
        {"title": "تراث نجد", "desc": "زخارف هندسية مستوحاة من العمارة النجدية والقصور الطينية الخالدة بتدرجات بنية وذهبية أنيقة.", "prompt": "Najdi traditional Saudi architecture patterns on luxury carpet, brown and gold theme"},
        {"title": "المجلس الملكي", "desc": "تصميم فخم بألوان كحلية وذهبية يحاكي أجواء المجالس الملكية التقليدية بزخارفها المهيبة.", "prompt": "Royal Saudi majlis luxury carpet, deep blue and gold colors, traditional patterns"},
        {"title": "نور المحراب", "desc": "تصميم روحاني مستوحى من الهندسة الإسلامية والمحاريب العتيقة بلون أخضر زمردي فاخر.", "prompt": "Islamic Mihrab luxury carpet rug, emerald green and gold premium patterns"},
        {"title": "الجمل الصحراوي", "desc": "تموجات رملية دافئة تعكس تفاصيل الصحراء العربية الأصيلة مدمجة بخيوط حريرية.", "prompt": "Arabian desert camel silhouette premium luxury rug carpet, golden sand colors"}
    ]

    for item in catalog_items:
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{item['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{item['desc']}</p>", unsafe_allow_html=True)
        
        encoded_p = urllib.parse.quote(item['prompt'])
        cat_url = f"https://image.pollinations.ai/p/{encoded_p}?width=700&height=400&nologo=true"
        st.image(cat_url, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "💰 المتجر وبوابات الأرباح":
    st.markdown("<div class='main-title'>المتجر وبوابات الأرباح</div>", unsafe_allow_html=True)

    business_path = st.radio("اختر المسار التجاري والاستثماري", ["شراء وتصنيع سجادة مخصصة", "شراء رخصة التصميم الرقمي بدقة 4K", "اشتراك باقة المحترفين والمحلات (SaaS)"])

    total_cost = 0.0
    order_details = ""

    if business_path == "شراء وتصنيع سجادة مخصصة":
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        length = st.number_input("الطول (متر)", min_value=0.5, max_value=20.0, value=2.0, step=0.1)
        width = st.number_input("العرض (متر)", min_value=0.5, max_value=20.0, value=1.5, step=0.1)
        material = st.selectbox("نوع الخامة", list(MATERIAL_PRICING.keys()))

        area = length * width
        total_cost = (area * MATERIAL_PRICING[material]) + 150
        st.markdown(f"<div class='cost-box'>التكلفة الإجمالية للتصنيع والشحن: {total_cost:,.2f} ريال</div>", unsafe_allow_html=True)
        order_details = f"تصنيع مخصص - {length}x{width}م - خامة: {material}"
        st.markdown("</div>", unsafe_allow_html=True)
    elif business_path == "شراء رخصة التصميم الرقمي بدقة 4K":
        total_cost = 199.0
        st.markdown(f"<div class='cost-box'>السعر الموحد للرخصة: {total_cost} ريال</div>", unsafe_allow_html=True)
        order_details = "رخصة تصميم رقمي 4K"
    else:
        total_cost = 299.0
        st.markdown(f"<div class='cost-box'>الاشتراك الشهري للباقة: {total_cost} ريال / شهرياً</div>", unsafe_allow_html=True)
        order_details = "اشتراك باقة SaaS للمحلات"

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h3>بيانات إتمام الطلب فوري</h3>", unsafe_allow_html=True)

    with st.container():
        customer_name = st.text_input("اسم العميل")
        phone_number = st.text_input("رقم الجوال")

        col_save, col_whatsapp = st.columns(2)
        with col_save:
            if st.button("💾 حفظ الطلب بالنظام"):
                if customer_name.strip() == "" or phone_number.strip() == "":
                    st.error("الرجاء إدخل البيانات أولاً.")
                else:
                    save_order(customer_name, phone_number, business_path, order_details, total_cost)
                    st.success("تم الحفظ في قاعدة بيانات SQLite بنجاح.")
        with col_whatsapp:
            if st.button("📲 إرسال عبر الواتساب"):
                if customer_name.strip() == "" or phone_number.strip() == "":
                    st.error("الرجاء إدخال البيانات أولاً.")
                else:
                    msg = f"طلب جديد: {customer_name}\nجوال: {phone_number}\nالخدمة: {business_path}\nالمبلغ: {total_cost} ريال"
                    encoded_msg = urllib.parse.quote(msg)
                    st.markdown(f'<a href="https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}" target="_blank"><div class="cost-box" style="background:#25D366; color:white; font-size:1rem;">اضغط هنا للواتساب 💬</div></a>', unsafe_allow_html=True)

elif page == "⭐ مشاريع العملاء":
    st.markdown("<div class='main-title'>⭐ لوحة تحكم مشاريع نسيج</div>", unsafe_allow_html=True)
    orders = get_all_orders()
    if not orders:
        st.info("لا توجد طلبات مسجلة حالياً.")
    else:
        for order in orders:
            with st.expander(f"📦 طلب رقم {order[0]} - {order[1]}"):
                st.write(f"**الجوال:** {order[2]} | **الخدمة:** {order[3]}")
                st.write(f"**التفاصيل:** {order[4]} | **المبلغ:** {order[5]} ريال")
                st.write(f"**تاريخ الطلب:** {order[6]}")

elif page == "📞 الاتصالات":
    st.markdown("<div class='main-title'>📞 تواصل مع إدارة نسيج</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='nasij-card'>", unsafe_allow_html=True)
        contact_name = st.text_input("الاسم بالكامل")
        contact_phone = st.text_input("رقم الجوال")
        contact_message = st.text_area("الرسالة الإبداعية")

        if st.button("✉️ تأكيد الإرسال"):
            if contact_name.strip() == "" or contact_phone.strip() == "" or contact_message.strip() == "":
                st.error("الرجاء ملء جميع الحقول قبل الإرسال.")
            else:
                st.success(f"شكراً لك {contact_name}، تم استلام رسالتك الإبداعية بنجاح وسنتواصل معك على الرقم {contact_phone}.")
        st.markdown("</div>", unsafe_allow_html=True)
