import os
import json
import PyPDF2
import re

def clean_text(text):
    """Clean extracted text to remove unsupported and non-UTF-8 characters."""
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)  # Remove control characters
    return text.encode("utf-8", "ignore").decode("utf-8")  # Remove non-UTF-8 characters

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file, handling corruption errors."""
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except PyPDF2.errors.PdfReadError:
        return "File is corrupt"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return "File is corrupt"
    return clean_text(text.strip()) if text else "File is empty or unreadable"

def clean_json_file(json_path):
    """Reads, cleans, and rewrites the JSON file to remove any non-UTF-8 characters."""
    try:
        with open(json_path, "r", encoding="utf-8", errors="replace") as f:
            json_content = f.read()
        
        # Remove non-UTF-8 characters
        cleaned_json_content = re.sub(r'[^\x00-\x7F]+', '', json_content)
        
        # Save cleaned content
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(cleaned_json_content)
        
        print(f"JSON file cleaned and saved: {json_path}")
    except Exception as e:
        print(f"Error cleaning JSON file: {e}")

def process_dair_directory(form_folders):
    """Process the specified form folders and generate JHS.JSON."""
    jhs_data = {"JHS": {}}
    
    for form_folder in form_folders:
        form_path = os.path.join(os.getcwd(), form_folder)
        
        if os.path.isdir(form_path):  # Ensure it's a directory
            for file in os.listdir(form_path):
                if file.endswith(".pdf") and "-F" not in file and "-Q" not in file:
                    clinical_variable = file.replace(".pdf", "")
                    
                    f_file = os.path.join(form_path, f"{clinical_variable}-F.pdf")
                    q_file = os.path.join(form_path, f"{clinical_variable}-Q.pdf")
                    
                    jhs_data["JHS"][clinical_variable] = {}
                    
                    if os.path.exists(f_file):
                        jhs_data["JHS"][clinical_variable]["F"] = extract_text_from_pdf(f_file)
                    else:
                        jhs_data["JHS"][clinical_variable]["F"] = "File does not exist"
                    
                    if os.path.exists(q_file):
                        jhs_data["JHS"][clinical_variable]["Q"] = extract_text_from_pdf(q_file)
                    else:
                        jhs_data["JHS"][clinical_variable]["Q"] = "File does not exist"
    
    # Save data to JSON file
    json_path = os.path.join(os.getcwd(), "JHS.JSON")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(jhs_data, json_file, indent=4, ensure_ascii=False)
    
    # Clean the JSON file
    clean_json_file(json_path)
    
    print(f"Final cleaned JSON file created: {json_path}")

# Example usage
process_dair_directory(["form1", "form2", "form3"])
