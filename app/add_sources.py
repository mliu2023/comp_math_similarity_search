from utils.pdf_parser import parse_pdf_from_url
from embeddings.encoder import get_embedding
from faiss_index.faiss_manager import load_urls, add_embedding

import numpy as np
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def add_source(url, source):
    urls = load_urls()
    if url not in urls:
        problems = parse_pdf_from_url(url)
        if len(problems) > 0:
            embeddings = get_embedding(problems)
            embeddings = np.array(embeddings)
            add_embedding(embeddings, [{"Source": source, "text": problems[i], "url": url} for i in range(len(problems))])
            return True
    return False

def add_hmmt_nov_sources():
    for year in range(2011, 2030):
        success = False
        for round in ["gen", "gen1", "gen2", "thm", "guts", "team"]:
            result = add_source(f"https://hmmt-archive.s3.amazonaws.com/tournaments/{year}/nov/{round}/solutions.pdf", 
                                f"HMMT November {year}")
            if result: 
                success = True
        if not success:
            break

def add_pumac_sources():
    base_url = "https://jason-shi-f9dm.squarespace.com/archives#directory"
    response = httpx.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    names = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        name = href.removeprefix("/s/").removeprefix("PUMaC").removeprefix("_").removesuffix(".pdf").removesuffix("_")
        if (href.endswith(".pdf") and 
            "Power" not in name and
            "power" not in name and 
            "Indiv" not in name and 
            "indiv" not in name and 
            "Final" not in name and 
            "final" not in name and 
            "Live" not in name and 
            "live" not in name and 
            "B" not in name and
            (not name[0:4].isdigit() or int(name[0:4]) >= 2012) and
            ("Sol" in name or "sol" in name or "SOL" in name or (len(names) > 0 and name == names[-1] + "-2"))):
            url = urljoin(base_url, href)
            urls.append(url)
        names.append(name)
    return urls

def add_cmimc_sources():
    urls = []
    labels = []
    for year in range(2016, 2030):
        base_url = f"https://cmimc.math.cmu.edu/math/past-problems/{year}"
        response = httpx.get(base_url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith("sharing"):
                label = link["aria-label"]
                if label == "Solutions" and labels[-1] in ["Algebra", "Combinatorics", "Geometry", "Number Theory"]:
                    url = urljoin(base_url, href)
                    urls.append(url)
                labels.append(label)
    return urls

def add_aime_sources():
    pass

if __name__ == "__main__":
    # add_source("https://hmmt-archive.s3.amazonaws.com/tournaments/2024/nov/gen/solutions.pdf", "HMMT November 2024")
    # add_source("https://hmmt-archive.s3.amazonaws.com/tournaments/2024/nov/thm/solutions.pdf", "HMMT November 2024")
    for name in add_cmimc_sources():
        print(name)