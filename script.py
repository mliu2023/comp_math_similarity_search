import httpx
import fitz

if __name__ == "__main__":
    url = "https://drive.google.com/file/d/1Ylm34N-nTIeBaA8GsfcDQySvpImMwWiE/view?usp=sharing"
    response = httpx.get(url)
    print(response.content)
    # pdf = fitz.open(stream=response.content, filetype="pdf")
    # text = ""
    # for page_number in range(len(pdf)):
    #     page = pdf[page_number]
    #     text += page.get_text()