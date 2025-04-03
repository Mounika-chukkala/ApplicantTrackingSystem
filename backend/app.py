from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from flask_cors import CORS

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow frontend requests

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
    return pdf_parts

@app.route("/evaluate", methods=["POST"])
def evaluate_resume():
    job_description = request.form["job_description"]
    resume_file = request.files["resume"]

    pdf_content = input_pdf_setup(resume_file)
    prompt = """You are an experienced HR evaluating the resume for Data Science, Full Stack Web Development, 
                Big Data Engineering, DevOps, and Data Analyst roles. Provide an analysis of the candidate's 
                suitability for the role, highlighting strengths and weaknesses."""
    
    response = get_gemini_response(prompt, pdf_content, job_description)
    return jsonify(response)

@app.route("/match_percentage", methods=["POST"])
def match_percentage():
    job_description = request.form["job_description"]
    resume_file = request.files["resume"]

    pdf_content = input_pdf_setup(resume_file)
    prompt = "Analyze the resume and job description, and provide a match percentage."

    response = get_gemini_response(prompt, pdf_content, job_description)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
