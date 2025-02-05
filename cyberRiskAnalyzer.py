from flask import Flask, request, render_template, jsonify #Import Flask framework and related modules
from docx import Document # Import module to process DOCX files
import os # Import module for interacting with the operating system
import magic # Import module to detect file MIME types(standardized identifiers used to specify the nature and format of a file or data.eg text/plain)
import pandas as pd  # Import Pandas for handling CSV files
import fitz # PyMuPDF library to read PDFs
import re # Regular expressions for pattern matching
from werkzeug.utils import secure_filename # Secure file uploads

# Initialize Flask application
app = Flask(__name__, static_folder='static')

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "csv", "docx"}

# Configure Flask app settings
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Limit file upload size to 16MB

# Create the uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the maximum allowed file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Function to validate uploaded file
def validate_file(file):
    if not file or file.filename == '': # Check if a file is selected
        return 'No file selected'

    if not allowed_file(file.filename): # Check if file type is allowed
        return 'Invalid file type. Only TXT, CSV, DOCX and PDF allowed'

    file.seek(0) # Reset file pointer
    mime = magic.Magic(mime=True) # Initialize MIME type detection
    file_type = mime.from_buffer(file.read(2048)) # Read first 2048 bytes to detect type
    file.seek(0) # Reset file pointer again

    # Validate MIME type against allowed types
    if not (file_type in ["text/plain", "application/pdf", "text/csv", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]):
        return f"Invalid file MIME type: {file_type}"

    file.seek(0, os.SEEK_END) # Move pointer to end of file
    file_size = file.tell() # Get file size
    file.seek(0) # Reset pointer to beginning

    if file_size > MAX_FILE_SIZE: # Check file size limit
        return "File is too large. Maximum size allowed is 5MB"

    return None  # No errors

# Route for home page
@app.route("/")
def home():
    return render_template("index.html") # Render HTML template

# Route to handle file upload
@app.route("/upload", methods=["POST"])
def upload_file():
        if 'file' not in request.files: # Check if file is in request
            return jsonify({'error': 'No file selected'}), 400

        file = request.files['file'] # Get the uploaded file
        error = validate_file(file) # Validate file
        
        if error: # Return error if validation fails
            return jsonify({"error": error}), 400

        filename = secure_filename(file.filename)   # Secure the filename
        file_path = os.path.join("uploads", filename) # Define file save path
        file.save(file_path) # Save the file

        analysis_result = analyze_file(file_path) # Analyze the uploaded file

        return jsonify(analysis_result) # Return analysis results as JSON

# Function to analyze the uploaded file
def analyze_file(file_path):
    file_info = {} # Dictionary to store file details

    mime =  magic.Magic(mime=True) # Initialize MIME detection
    file_type = mime.from_file(file_path) # Detect file type
    file_info["File Type"] = file_type # Store file type
    file_info["Size (bytes)"] = os.path.getsize(file_path) # Store file size

    extracted_text = "" # Variable to store extracted text

    # Extract text based on file type
    if file_type == "text/plain":
        with open(file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()
    elif file_type == "text/csv":
        df = pd.read_csv(file_path)
        extracted_text = df.to_string()
    elif file_type == "application/pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_text = extract_text_from_docx(file_path)

    summary = extract_cyber_risk_info(extracted_text) # Extract cyber risk information

    file_info["Extracted Summary"] = summary # Store extracted summary
    return file_info # Return file analysis results

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() # Read text from each page
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs]) # Extract text from paragraphs

# Function to analyze extracted text for cyber risk patterns
def extract_cyber_risk_info(text):
    summary = {}  # Dictionary to store extracted information

    # Define patterns for detecting cyber threats
    attack_patterns = {
        "phishing": r"phishing|email scam|social engineering|spoofing",
        "malware": r"malware|ransomware|virus|trojan|spyware",
        "DoS": r"denial of service|DDoS|service disruption",
        "data breach": r"data breach|unauthorized access|data leak|information theft",
        "insider threat": r"data breach|employee fraud|insider threat|priveleged access"
    }

    # Detect attack type based on patterns
    for attack, pattern in attack_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            summary["Attack Type"] = attack
            break
        else:
            summary["Attack Type"] = "Unknown"

    # Extract attack date from text
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    summary["Attack Date"] = date_match.group(0) if date_match else "Date Not Found"

    # Identify affected systems
    systems = re.findall(r"(Windows|Linux|MacOS|Server|Firewall|Cloud)", text, re.IGNORECASE)
    summary["Affected Systems"] = ", ".join(set(systems)) if systems else "Unknown"

    return summary # Return extracted cyber risk information

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True) # Start server in debug mode