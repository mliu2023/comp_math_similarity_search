from embeddings.encoder import get_embedding
from faiss_index.faiss_manager import search_index
from utils.pdf_parser import parse_pdf

import numpy as np

def similarity_search(file):
    problems = parse_pdf(file)
    embeddings = get_embedding(problems)
    embeddings = np.array(embeddings)
    return search_index(embeddings, 3)

if __name__ == "__main__":
    embeddings = get_embedding(["Let $f$ be a degree 7 polynomial satisfying f(k) = 1/k^2 for $k \in \{1\cdot2, 2\cdot3, \dots, 8\cdot9\}$. Find $f(90) - \frac{1}{90^2}$. Define the ninth-degree polynomial $g(x)=x^2f(x)-1$. Then $g$ has roots at each of $\{1\cdot2,2 \cdot2...,8\cdot9\},$ and in particular $g(x)=h(x)(x-1\cdot2)(x-2\cdot3)...(x-8\cdot9)$ where $h(x)$ is linear. Let \[h(x) = a(x+b)\] \[g(x) = a(x+b)(x-1\cdot2)(x-2\cdot3)...(x-8\cdot9)\] Then since $x^2 \mid g(x)+1$, the coefficient of $x$ in $g(x)+1$ must be 0. Let $S$ be the product of the roots. Then we know that \[0=\sum{\frac{S}{r_i}}\] over the roots $r_i$. Thus \[0=\sum{\frac{S}{r_i}} = -\frac{S}{b}+\sum_{i=1}^{8}{\frac{S}{i(i+1)}}\] \[\frac{1}{b} = \sum_{i=1}^{8}{\frac{1}{i(i+1)}}=1-\frac{1}{9}=\frac{8}{9}\] Thus \[b = \frac{9}{8}\] Furthermore, since $x^2 \mid g(x)+1$, the constant term in $g(x)+1$, i.e. $g(0)+1$ must be 0. \[a\frac{9}{8}\prod_{i=1}^8-i(i+1) =-1\] \[a=-\frac{8}{9\cdot9!8!}\] Thus \[x^2f(x)-1=-\frac{8}{9!^2}(x+\frac{9}{8})(x-1\cdot2)(x-2\cdot3)...(x-8\cdot9)\] Plugging in $x=9\cdot10$, \[90^2f(90)-1=-\frac{8}{9!^2}(9\cdot10+\frac{9}{8})(9\cdot10-1\cdot2)(9\cdot10-2\cdot3)...(9\cdot10-8\cdot9)\] \[=-\frac{8}{9!^2}\frac{9^3}{8}(8\cdot11)(7\cdot12)\dots(1\cdot18)=-\frac{8}{9!^2}\frac{9^3}{8}\frac{8!18!}{10!}\] So \[f(90)-\frac{1}{90^2} = -\frac{1}{9^210^2}\frac{8}{9!^2}\frac{9^3}{8}\frac{8!18!}{10!}=-\frac{18!}{10^2\cdot9!\cdot10!}=-\frac{2431}{50}=-48.62\]"])
    embeddings = np.array(embeddings)
    distances, metadata = search_index(embeddings, 10)
    for i in range(len(distances)):
        print(f"Problem {i+1}:")
        for j in range(len(metadata[i])):
            print(f"Distance: {distances[i][j]}")
            print(metadata[i][j]["text"])
    # print(similarity_search("app/faiss_index/data/sources/hmmt_november_2024_general.pdf"))