# Autocomplete & Spell Checker using Trie

An efficient **Autocomplete** and **Spell Checker** system built with **Python** and the **Trie** data structure.
It suggests words as you type and can also help identify misspelled words and offer corrections.

---

## 🚀 Features

* **Fast Autocomplete:** Suggests words in real-time based on the typed prefix.
* **Spell Checking:** Detects invalid words and offers close matches.
* **GUI Interface:** User-friendly graphical interface for testing and interaction.
* **Custom Dictionary:** Easily extendable by modifying `data/words.txt`.
* **Recent Search Memory:** Stores and suggests recently searched words from `data/recent.txt`.

---

## 📂 Project Structure

```
autocomplete_trie/
├── data/
│   ├── recent.txt             # Stores recent words typed/searched
│   └── words.txt              # Dictionary of words for the trie
├── gui/
│   ├── __init__.py
│   └── autocomplete_gui.py    # GUI interface for the autocomplete system
├── trie/
│   ├── __init__.py
│   ├── trie.py                 # Core Trie implementation
│   └── trie_node.py            # Trie Node definition
├── main.py                     # Entry point for CLI or GUI execution
├── requirements.txt            # Python dependencies
└── trie_venv/                  # Virtual environment (not tracked in Git)
```

---

## 🧠 How It Works

1. **Trie Construction:**

   * Words from `data/words.txt` are loaded into a **Trie** data structure.
   * Each node in the Trie represents a letter and can lead to many branches for different words.

2. **Autocomplete:**

   * As the user types a prefix, the system traverses the Trie to find matching completions efficiently.

3. **Spell Checking:**

   * If the typed word isn’t found in the Trie, a list of closest matches is suggested.

---

## 🖥️ Installation & Usage

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Tesfalegnp/Longest-Common-Prefix-using-Tries.git
cd autocomplete_trie
```

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv trie_venv
source trie_venv/bin/activate   # On Windows: trie_venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the GUI

```bash
python main.py
```

---

## 📊 Example Usage

**Autocomplete Example:**

```
Input: "aut"
Suggestions: ["auto", "automatic", "autumn"]
```

**Spell Check Example:**

```
Input: "helo"
Suggestions: ["hello", "help", "held"]
```

---

## 🛠️ Technologies Used

* **Python 3.12+**
* **Tkinter** – For GUI
* **Trie Data Structure** – For efficient prefix search
* **Levenshtein Distance** (optional) – For spell checking

---

## 📌 Future Improvements

* Add fuzzy search for better spell correction
* Support multiple languages
* Integrate with a live search API
* Save user preferences in a config file

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
