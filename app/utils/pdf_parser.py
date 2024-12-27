import google.generativeai as genai
import fitz
import base64
import httpx
import os
import re

def _extract_problems(guide_text, data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""Extract the text from each problem and solution pair in the PDF file. 
Start each problem with a number followed by a period. 
Do not use LaTeX format. Write math expressions in plain text. 
Carefully handle exponents and fractions. Ignore all diagrams. 
Here is how fitz extracted the text: {guide_text}. 
Please use this as a guide to make sure you don't miss anything. 
Only print problems and solutions."""
    response = model.generate_content([{'mime_type': 'application/pdf', 'data': data}, prompt])
    problems = re.split("\n\d+\. ", response.text)
    problems = [re.sub("^\d+\. ", "", problem) for problem in problems if len(problem) >= 20]
    return problems

def parse_pdf_from_url(url):
    response = httpx.get(url, follow_redirects=True)
    if response.error_code != 200:
        return []
    pdf = fitz.open(stream=response.content, filetype="pdf")
    text = ""
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text += page.get_text()

    data = base64.standard_b64encode(httpx.get(url).content).decode("utf-8")

    problems = _extract_problems(text, data)
    return problems

def parse_pdf(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found")
    with open(file, "rb") as f:
        pdf = fitz.open(f)
        text = ""
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            text += page.get_text()

    with open(file, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")

    problems = _extract_problems(text, data)
    return problems

if __name__ == "__main__":
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.join(current_dir, 
    #                     "..", 
    #                     "faiss_index", 
    #                     "data", 
    #                     "sources", 
    #                     "hmmt_november_2024_theme.pdf")
    # print(parse_pdf(path))
    output = parse_pdf_from_url("https://hmmt-archive.s3.amazonaws.com/tournaments/2024/nov/gen/solutions.pdf")
    print(output)
    print(len(output))