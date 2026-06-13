import streamlit as st
import pdfplumber
from groq import Groq

# 1. ضبط إعدادات الصفحة الاحترافية وتفعيل وضع التمركز التلقائي للمظهر المظلم
st.set_page_config(
    page_title="CV Reviewer AI", 
    page_icon="🔍", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ترويسة الموقع بشكل منسق ومحترم للعين
st.write("### 🔍 CV Reviewer AI")
st.caption("مقيم ومستشار السير الذاتية الذكي للحصول على تقييم شامل ونقاط التطوير المهني وتجاوز أنظمة الـ ATS")
st.divider()

# 3. تنظيم منطقة رفع الملفات داخل حاوية أنيقة
with st.container():
    st.write("#### 📥 تحميل المستند")
    uploaded_file = st.file_uploader("ارفع سيرتك الذاتية بصيغة (PDF)", type=["pdf"])

st.divider()

# 4. معالجة البيانات وعرض التقييم الاستشاري
if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text_from_pdf = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    # وضع زر البدء بشكل مرتب ومستقل
    if st.button("✨ ابدأ التقييم والمراجعة الفورية", use_container_width=True):
        st.write("#### 📊 تقرير المستشار المهني الذكي")
        
        with st.spinner("⏳ جاري تحليل السيرة الذاتية وصياغة النصائح الاحترافية..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                prompt = f"أنت خبير توظيف ومستشار مهني. قم بتقييم السيرة الذاتية التالية بدقة واذكر التقييم من 100، ونقاط القوة والضعف ونصائح لتجاوز الـ ATS:\n{text_from_pdf}"
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                evaluation_result = completion.choices[0].message.content
                
                # وضع تقرير المخرجات داخل حاوية منفصلة ومحترمة (Card Style) لترييح العين
                with st.container():
                    st.success("🎉 تم التقييم بنجاح! إليك التقرير الشامل:")
                    st.markdown(evaluation_result)
                    st.write("---") # خط فاصل ناعم للختام
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
