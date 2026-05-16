from pathlib import Path


def count_words(path):
    try:
        contents = path.read_text(encoding='utf-8') # It can give error
    except FileNotFoundError:
        print(f"Error: {path} not found")
    else:    
        words = contents.split()    # breaks after a space
        num_words = len(words)
        print(f"The file {path} has approximate {num_words} words.") # Total no. of words in the file

path = Path('alice.txt')
count_words(path)                