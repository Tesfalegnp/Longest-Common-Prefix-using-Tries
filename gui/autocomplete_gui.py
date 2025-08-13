import tkinter as tk
from tkinter import StringVar, END, messagebox
import os
from datetime import datetime
from trie.trie import Trie

class AutocompleteGUI:
    def __init__(self, trie: Trie):
        self.trie = trie
        self.root = tk.Tk()
        self.root.title("Autocomplete + Spellcheck + History")
        self.root.geometry("430x520")

        # ensure data directory exists
        os.makedirs("data", exist_ok=True)
        self.recent_file = os.path.join("data", "recent.txt")

        self.entry_var = StringVar()
        self.entry_var.trace_add("write", self.update_suggestions)

        tk.Label(self.root, text="Type a word:", font=("Arial", 12)).pack(pady=6)
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, font=("Arial", 14))
        self.entry.pack(pady=5, fill="x", padx=12)

        # if the user clicks the entry and it's empty, show recent selections
        self.entry.bind("<FocusIn>", self.show_recent_if_empty)

        # Listbox for suggestions
        self.listbox = tk.Listbox(self.root, font=("Arial", 12))
        self.listbox.pack(pady=10, fill="both", expand=True, padx=12)

        # Bind selection event
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Footer / hint
        tk.Label(self.root, text="Click a suggestion to autocorrect & save to recent.", font=("Arial", 9)).pack(pady=6)

        # initialize listbox empty
        self.listbox.delete(0, END)

    def update_suggestions(self, *args):
        typed_word = self.entry_var.get().strip()
        self.listbox.delete(0, END)

        if not typed_word:
            # reset color and show nothing (or recent on focus)
            self.entry.config(fg="black")
            return

        # 1) Exact match
        if self.trie.search(typed_word):
            self.entry.config(fg="black")
            suggestions = self.trie.autocomplete(typed_word)
            for s in suggestions:
                self.listbox.insert(END, s)
            return

        # 2) Partial (prefix) matches
        partials = self.trie.autocomplete(typed_word)
        if partials:
            # partial exists (valid prefix) — treat as non-error
            self.entry.config(fg="black")
            for s in partials:
                self.listbox.insert(END, s)
            return

        # 3) No partials — try spell check (nearest words)
        spell_suggestions = self.trie.spell_check(typed_word, max_suggestions=5)
        if spell_suggestions:
            # Show suggestions and mark entry as problematic (red) until user fixes/selects
            self.entry.config(fg="red")
            for s in spell_suggestions:
                self.listbox.insert(END, f"{s}")
            return
        else:
            # No close matches
            self.entry.config(fg="red")
            self.listbox.insert(END, "No match found!")
            return

    def show_recent_if_empty(self, event=None):
        """If the entry is empty and user focuses it, load recent selections."""
        if self.entry_var.get().strip():
            return
        self.listbox.delete(0, END)
        recents = self.load_recent_words()
        if not recents:
            self.listbox.insert(END, "(No recent selections)")
            return
        for word in recents:
            self.listbox.insert(END, f"{word}")

    def on_select(self, event):
        """Handle clicking a listbox item:
           - if it's a valid suggestion, replace input box, mark valid, save to recent, and show message.
           - if it's 'No match found!' or placeholder, show an info only.
        """
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return

        selected = self.listbox.get(index)

        if selected == "No match found!" or selected == "(No recent selections)":
            messagebox.showinfo("No selection", "No word to select. Please type another word.")
            return

        # remove prefixes if present
        if selected.startswith("(Recent)"):
            selected_word = selected[len("(Recent) "):]
        elif selected.startswith("Did you mean: "):
            selected_word = selected[len("Did you mean: "):]
        else:
            selected_word = selected

        # Autocorrect the entry to the selected word
        self.entry_var.set(selected_word)
        self.entry.config(fg="black")  # now valid because it's a trie word

        # Save selection to recent file with timestamp
        self.save_recent_word(selected_word)

        # Notify user
        messagebox.showinfo("Word selected", f"You selected: {selected_word}")

        # Refresh suggestions for the newly set (valid) word
        self.update_suggestions()

    def save_recent_word(self, word):
        """Append word with timestamp to recent.txt (creates file if needed)."""
        with open(self.recent_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{word}\n")

    def load_recent_words(self, max_items=10):
        """Return recent words in most-recent-first order (deduped)."""
        if not os.path.exists(self.recent_file):
            return []
        with open(self.recent_file, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]

        # parse timestamp|word, sort by timestamp desc
        entries = []
        for ln in lines:
            if "|" in ln:
                ts, w = ln.split("|", 1)
                entries.append((ts, w))
        entries.sort(key=lambda x: x[0], reverse=True)

        # dedupe preserving recency
        seen = set()
        result = []
        for _, w in entries:
            if w not in seen:
                seen.add(w)
                result.append(w)
            if len(result) >= max_items:
                break
        return result

    def run(self):
        self.root.mainloop()
