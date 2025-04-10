import streamlit as st
import PyPDF2
import openai

st.set_page_config(page_title="LegalLens AI", layout="centered", page_icon="📄")

st.title("LegalLens AI")
st.subheader("Upload your property PDF to get a legal summary, risk level, and missing document suggestions")

uploaded_file = st.file_uploader("Upload Property Document (PDF)", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    st.info("Generating AI analysis...")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    prompt = f"""
    You are a real estate legal advisor. Read the following property document content and provide:
    1. A short legal summary of what the document is about.
    2. A risk rating (Low, Medium, High) based on any irregularities or missing info.
    3. A list of important missing documents if any (like NA order, encumbrance certificate, etc.).

    Document content:
    {text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        result = response['choices'][0]['message']['content']
        st.success("Analysis complete")
        st.markdown(result)
    except Exception as e:
        st.error("Error processing your document. Please try again.")
        st.exception(e)
