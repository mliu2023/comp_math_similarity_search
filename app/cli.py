import argparse
from search import similarity_search

def parse_arguments():
    parser = argparse.ArgumentParser(description="Search for similar problems in the database")
    parser.add_argument(
        "file",
        type=str,
        help="The path to the PDF file with the problems to search for")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    distances, metadata = similarity_search(args.file)
    for i in range(len(distances)):
        print(f"Problem {i+1}:")
        for j in range(len(metadata[i])):
            print(f"Distance: {distances[i][j]}")
            print(metadata[i][j]["text"])