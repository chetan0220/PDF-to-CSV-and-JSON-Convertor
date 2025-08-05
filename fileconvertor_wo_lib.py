import sys
import os
import csv
import json
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts and returns all text from a PDF file using PyPDF2.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: The extracted text from all pages of the PDF.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_word(word_path):
    """
    Reads and returns the content of a Word file as plain text.
    Note: Only works for plain text files, not true .docx/.doc binary files.
    Args:
        word_path (str): Path to the Word file.
    Returns:
        str: The file content as text.
    """
    with open(word_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_qa_pairs(text):
    """
    Parses text and extracts question-answer pairs.
    Each question starts with 'Q:' and each answer with 'A:'.
    Returns a list of dictionaries with 'Q' and 'A' keys.
    Args:
        text (str): The input text containing Q/A pairs.
    Returns:
        list: List of dicts, each with 'Q' and 'A' keys.
    """
    qa_pairs = []
    lines = text.splitlines()
    q, a = None, None
    for line in lines:
        line = line.strip()

        # Check for a new question
        if line.startswith('Q:'):
            if q and a:
                qa_pairs.append({'Q': q, 'A': a})
            q = line[2:].strip()
            a = None

        # Check for a new answer
        elif line.startswith('A:'):
            a = line[2:].strip()

        # Handle multi-line answers
        elif q and a:
            a += ' ' + line
    
    # Add the last Q/A pair if present
    if q and a:
        qa_pairs.append({'Q': q, 'A': a})
    return qa_pairs

def write_to_csv(text, csv_path):
    """
    Writes question-answer pairs to a CSV file with columns 'Q' and 'A'.
    Args:
        text (str): The input text containing Q/A pairs.
        csv_path (str): Path to the output CSV file.
    """
    qa_pairs = parse_qa_pairs(text)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Q', 'A'])
        writer.writeheader()
        for pair in qa_pairs:
            writer.writerow(pair)

def write_to_json(text, json_path):
    """
    Writes question-answer pairs to a JSON file as a list of objects with 'Q' and 'A' keys.
    Args:
        text (str): The input text containing Q/A pairs.
        json_path (str): Path to the output JSON file.
    """
    qa_pairs = parse_qa_pairs(text)
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(qa_pairs, jsonfile, ensure_ascii=False, indent=2)

def main():
    input_file = sys.argv[1]
    filename, ext = os.path.splitext(input_file)
    if ext.lower() == '.pdf':
        text = extract_text_from_pdf(input_file)
    elif ext.lower() in ['.doc', '.docx']:
        text = extract_text_from_word(input_file)
    else:
        print("Unsupported file type. Only PDF and Word files are supported.")
        sys.exit(1)

    write_to_csv(text, filename + 'wo_lib' + '.csv')
    write_to_json(text, filename + 'wo_lib' +'.json')
    print(f"Converted {input_file} to {filename + '.csv'} and {filename + '.json'}.")

if __name__ == "__main__":
    main()
