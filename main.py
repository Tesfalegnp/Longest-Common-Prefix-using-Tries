from trie.trie import Trie
from gui.autocomplete_gui import AutocompleteGUI
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Build trie from words file
trie = Trie()
words_file = os.path.join("data", "words.txt")
if not os.path.exists(words_file):
    raise FileNotFoundError(f"Please create '{words_file}' and add dictionary words (one per line).")

with open(words_file, "r", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            trie.insert(w)

app = AutocompleteGUI(trie)
app.run()
