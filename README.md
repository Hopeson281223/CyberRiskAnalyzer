# CyberRiskAnalyzer

## Description
**CyberRiskAnalyzer** is a project designed to analyze and assess different types of cyber risk files, including incident reports, and generate summarized risk assessments. It is intended to assist cybersecurity analysts in identifying, understanding, and managing cyber risks efficiently, enabling informed decision-making and enhanced security measures.

## Features
- **File Parsing & Data Extraction**  
  Supports parsing multiple file formats (PDF, CSV, DOCX) to extract relevant risk data from incident reports and other cyber risk files.

- **Risk Analysis**  
  Analyzes parsed data to identify and categorize risks based on predefined risk parameters.

- **Risk Summarization**  
  Automatically generates clear and concise summaries of cyber risk reports, focusing on key findings such as threat types, affected systems, and severity levels.

## Installation

### Prerequisites
To run **CyberRiskAnalyzer**, ensure you have the following installed:

- Python 3.x (>=3.7)
- Required Python packages (listed in `requirements.txt`)

### Steps to Install
1. Clone the repository:
    ```bash
    git clone https://github.com/Hopeson281223/CyberRiskAnalyzer
    ```

2. Navigate to the project directory:
    ```bash
    cd CyberRiskAnalyzer
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. (Optional) Set up a virtual environment for isolated dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

## Usage

### Running the Analyzer
To analyze a cyber risk file and generate a report, use the following command:
```bash
python cyberRiskAnalyzer.py --input <path_to_file> --output <path_to_output_file> --format <output_format>
