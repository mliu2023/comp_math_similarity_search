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
    # embeddings = get_embedding(["Consider a 54-deck of cards, i.e. a standard 52 card deck together with two jokers. Ada draws cards from the deck until Ada has both a king and a queen. How many cards does Ada pick up on average?     Consider the order in which Ada draws the kings and queens, ignoring all the other cards. Without loss of generality assume that Ada draws a king before a queen. Then the chance of drawing the first queen as the 2nd card is $4/7$, the chance of drawing the first queen as the 3rd card is $3/7 \cdot 4/6 = 2/7$, the chance of drawing the first queen as the 4th card is $3/7 \cdot 2/6 \cdot 4/5 = 4/35$, and the chance of drawing the first queen as the 5th card is $3/7 \cdot 2/6 \cdot 1/5 \cdot4/4 = 1/35$. \\ Now observe that since there are a total of 8 kings and queen combined, distributed between the 46 other cards, the expected number of cards before drawing the first king or queen and the expected number of cards between each king or queen and the following king or queen is \[E[\text{\# between}] = 46/(8 + 1) = 46/9.\] In the case where Ada draws the first queen as the second card, the expected number of cards drawn is \[2 + 2E[\text{\# between}].\] In the case where Ada draws the first queen as the third card, the expected number of cards drawn is \[3 + 3E[\text{\# between}].\] In the case where Ada draws the first queen as the fourth card, the expected number of cards drawn is \[4 + 4E[\text{\# between}].\] In the case where Ada draws the first queen as the fifth card, the expected number of cards drawn is \[5 + 5E[\text{\# between}].\] Thus overall, the expected number of cards drawn is \[(2\cdot4/7+3\cdot 2/7+4\cdot4/35+5\cdot1/35)(1+E[\text{\# between}]) = 13/5 \cdot 55/9 = 143/9.\]"])
    # embeddings = np.array(embeddings)
    # print(search_index(embeddings, 5))
    print(similarity_search("app/faiss_index/data/sources/hmmt_november_2024_general.pdf"))