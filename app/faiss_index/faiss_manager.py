import faiss
import os
import json
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(CURRENT_DIR, "data", "faiss_index.bin")
META_FILE = os.path.join(CURRENT_DIR, "data", "metadata.json")

def _load_index():
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
    else:
        index = faiss.IndexFlatL2(128)
        faiss.write_index(index, INDEX_FILE)
    if os.path.exists(META_FILE):
        with open(META_FILE, "r") as f:
            metadata = json.load(f)
    else:
        metadata = {}
    return index, metadata

def load_urls():
    _, metadata = _load_index()
    return {metadata[key]["url"] for key in metadata}
    
def add_embedding(embeddings, metadata_entries):
    index, metadata = _load_index()
    for i in range(len(embeddings)):
        id = index.ntotal
        index.add(np.expand_dims(embeddings[i], 0))
        faiss.write_index(index, INDEX_FILE)
        metadata[str(id)] = metadata_entries[i]
        with open(META_FILE, "w") as f:
            json.dump(metadata, f, indent=4)

def search_index(query_embeddings, k):
    index, metadata = _load_index()
    if index.ntotal == 0:
        return [], []
    else:
        distances, indices = index.search(query_embeddings, k)
        return distances, [[metadata[str(j)] for j in indices[i]] for i in range(len(indices))]

if __name__ == "__main__":
    import numpy as np
    index, metadata = _load_index()
    print(search_index(np.zeros((1, 128)), 2))