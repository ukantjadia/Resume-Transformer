import google.generativeai as genai
import base64
import pdf2image
import io
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


os.environ.get("GOOGLE_API_KEY")
genai.configure(
    api_key=os.environ.get("GOOGLE_API_KEY"),
)

# Set up the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.25,
    "top_k": 23,
    "max_output_tokens": 3989,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel(
        "gemini-pro-vision",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text




def input_pdf_setup(uploaded_file):
    pdf_parts = []
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        for _, item in enumerate(images):
            img_byte_arr = io.BytesIO()
            item.save(img_byte_arr, format="JPEG")
            img_byte_arr = img_byte_arr.getvalue()
            pdf_parts.append(
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode(),
                }
            )
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


input_prompt1 = """
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses in a sentences of the applicant in relation to the specified job requirements give the output in bullet points.
"""
input_prompt2 = """
You are an Technical Human Resource Manager with expertise in data science, 
your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. keep the insight sort by covering all the important facts and condidate's potential.
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed. give this into a sort lines by pointing out the skills and area.
"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
assess the compatibility of the resume with the role. Give me what are the keywords that are missing with there respective section, in bullet points.
Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development. highlight the area and skills and give output in  bullet points.
"""
input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing in bullet points and last final thoughts on behalf of resume and if matching percentage is lesser than the 70 than resume will not be short listed.
"""


# Streamlit App
st.set_page_config(page_title="Resume Transformer")
st.header("JobFit Analyzer")
st.subheader(
    "This web application streamlines your resume review process with the assistance of GEMINI AI [LLM]")
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("What are the Keywords That are Missing")

submit4 = st.button("Percentage match")

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.toast("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.toast("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.toast("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.toast("Please upload a PDF file to proceed.")


st.markdown("---")
st.caption("Resume Expert - Making Job Applications Easier")
