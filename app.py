import streamlit as st
import pdfplumber
from groq import Groq

st.set_page_config(page_title="CV Reviewer AI", page_icon="🔍", layout="centered")
st.title("🔍 CV Reviewer AI - مقيم ومستشار السير الذاتية")
st.write("ارفع سيرتك الذاتية بصيغة PDF للحصول على تقييم شامل ونقاط التطوير.")

uploaded_file = st.file_uploader("ارفع سيرتك الذاتية (PDF)", type=["pdf"])

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text_from_pdf = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    if st.button("✨ ابدأ التقييم والمراجعة"):
        with st.spinner("جاري تحليل السيرة الذاتية وصياغة النصائح..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                prompt = f"أنت خبير توظيف ومستشار مهني. قم بتقييم السيرة الذاتية التالية بدقة واذكر التقييم من 100، ونقاط القوة والضعف ونصائح لتجاوز الـ ATS:\n{text_from_pdf}"
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                evaluation_result = completion.choices[0].message.content
                st.markdown(evaluation_result)
                st.success("تم التقييم بنجاح!")
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
