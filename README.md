# Similarity search for competition math problems

While writing problems for Brown's inaugural high school math contest ([BrUMO](https://www.brumo.org/)), I realized it was hard to check if problems were similar to ones used on previous contests. I scraped PDFs from HMMT and PUMaC (more coming soon!), extracted the problems, encoded each problem as vector using the Gemini API, and inserted the vectors into a vector database implemented with FAISS. I also created a command line interface to take in a pdf of problems and return similar problems in the database.
