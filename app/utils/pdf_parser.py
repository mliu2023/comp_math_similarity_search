import google.generativeai as genai
import fitz
import base64
import httpx
import os
import re

def _extract_problems(guide_text, data, split=0):
    model = genai.GenerativeModel("gemini-1.5-flash")
    addition = ""
    if split == 1:
        addition = " up until problem 18 (inclusive)"
    elif split == 2:
        addition = " starting from problem 19. If there are no such problems, return an empty string"  

    prompt = f"""
Extract the text from each problem and solution pair in the PDF file{addition}. 
Start each problem with a number followed by a period. 
Do not use LaTeX format. Write math expressions in plain text. 
Carefully handle exponents and fractions. Ignore all diagrams. 
Here is how fitz extracted the text: {guide_text}. 
Please use this as a rough guide. Only print problems and solutions."""
    response = model.generate_content([{'mime_type': 'application/pdf', 'data': data}, prompt])
    problems = re.split("\n\d+\. ", response.text)
    problems = [re.sub("^\d+\. ", "", problem) for problem in problems if len(problem) >= 20]
    return problems

def parse_pdf_from_url(url):
    response = httpx.get(url, follow_redirects=True)
    if response.status_code != 200:
        return []
    pdf = fitz.open(stream=response.content, filetype="pdf")
    text = ""
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text += page.get_text()

    data = base64.standard_b64encode(response.content).decode("utf-8")
    if len(pdf) >= 10:
        problems1 = _extract_problems(text, data, split=1)
        if len(problems1) == 18:
            problems2 = _extract_problems(text, data, split=2)
            return problems1 + problems2
        else:
            return problems1
    else:
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

    if len(pdf) >= 10:
        problems1 = _extract_problems(text, data, split=1)
        problems2 = _extract_problems(text, data, split=2)
        return problems1 + problems2
    else:
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
    output = parse_pdf_from_url("https://static1.squarespace.com/static/570450471d07c094a39efaed/t/6073d60a316f9960ca9fedd3/1618204171500/2020AlgebraASolutions.pdf")
    print(output)
    print(len(output))