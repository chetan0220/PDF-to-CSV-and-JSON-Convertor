import pdfplumber
import csv
import json
import sys
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file using pdfplumber.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: The extracted text from all pages.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_qa_pairs(text):
    """
    Parses text and extracts question-answer pairs.
    Each question starts with 'Q:' and each answer with 'A:'.
    Returns a list of dictionaries with 'Q' and 'A' keys.
    """
    qa_pairs = []
    lines = text.splitlines()
    q, a = None, None
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            if q and a:
                qa_pairs.append({'Q': q, 'A': a})
            q = line[2:].strip()
            a = None
        elif line.startswith('A:'):
            a = line[2:].strip()
        elif q and a:
            a += ' ' + line
    if q and a:
        qa_pairs.append({'Q': q, 'A': a})
    return qa_pairs

def write_to_csv(qa_pairs, csv_path):
    """
    Writes question-answer pairs to a CSV file with columns 'Q' and 'A'.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Q', 'A'])
        writer.writeheader()
        for pair in qa_pairs:
            writer.writerow(pair)

def write_to_json(qa_pairs, json_path):
    """
    Writes question-answer pairs to a JSON file as a list of objects with 'Q' and 'A' keys.
    """
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(qa_pairs, jsonfile, ensure_ascii=False, indent=2)

def main():
    input_file = sys.argv[1]
    filename, ext = os.path.splitext(input_file)
    if ext.lower() == '.pdf':
        text = extract_text_from_pdf(input_file)
    else:
        print("Unsupported file type. Only PDF is supported in this script.")
        sys.exit(1)
    qa_pairs = parse_qa_pairs(text)
    write_to_csv(qa_pairs, filename + '_w_lib' + '.csv')
    write_to_json(qa_pairs, filename + '_w_lib' + '.json')
    print(f"Converted {input_file} to {filename + '.csv'} and {filename + '.json'}.")

if __name__ == "__main__":
    main()
