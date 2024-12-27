import httpx
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(CURRENT_DIR, 
                       "..",
                       "faiss_index",
                       "data",
                       "sources")

def upload_file(url, filename):
    response = httpx.get(url)
    response.raise_for_status()
    filepath = os.path.join(PDF_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    upload_file("https://hmmt-archive.s3.amazonaws.com/tournaments/2024/nov/gen/problems.pdf", "HMMT_November_2024.pdf")