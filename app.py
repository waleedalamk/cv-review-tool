from flask import Flask, render_template, request
import os
import docx
import PyPDF2

app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to review CV content
def analyze_cv(text):
    score = 50  # Default score
    
    # Check for key sections
    required_sections = ["Experience", "Education", "Skills", "Contact"]
    for section in required_sections:
        if section.lower() in text.lower():
            score += 10

    # Give feedback
    if score > 80:
        feedback = "Great CV! It has all the important sections."
    elif score > 60:
        feedback = "Good CV, but you can improve it by adding more details."
    else:
        feedback = "Your CV is missing key sections. Try adding work experience and skills."
    
    return score, feedback

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_cv():
    if "cv" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["cv"]
    if file.filename == "":
        return "No file selected", 400

    # Check file extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "docx"]:
        return "Unsupported file format. Upload PDF or DOCX.", 400

    # Extract text
    text = ""
    if ext == "pdf":
        text = extract_text_from_pdf(file)
    elif ext == "docx":
        text = extract_text_from_docx(file)

    # Analyze CV
    score, feedback = analyze_cv(text)

    return render_template("index.html", score=score, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
