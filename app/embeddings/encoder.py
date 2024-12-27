import google.generativeai as genai
import os
from dotenv import load_dotenv

def get_embedding(texts):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model="models/text-embedding-004", content=texts, output_dimensionality=128
    )
    return result["embedding"]

if __name__ == "__main__":
    embedding = get_embedding("Consider a 54-deck of cards, i.e. a standard 52 card deck together with two jokers. Ada draws cards from the deck until Ada has both a king and a queen. How many cards does Ada pick up on average?")
    print(type(embedding)) # list