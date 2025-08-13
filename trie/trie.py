from .trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def _dfs_collect(self, node, prefix, results, limit=None):
        """Collect words under node. limit=None -> unlimited, else max results."""
        if limit is not None and len(results) >= limit:
            return
        if node.is_end_of_word:
            results.append(prefix)
        for char, child in node.children.items():
            self._dfs_collect(child, prefix + char, results, limit)

    def autocomplete(self, prefix, limit=30):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._dfs_collect(node, prefix.lower(), results, limit)
        return results

    def get_all_words(self):
        results = []
        self._dfs_collect(self.root, "", results, limit=None)
        return results

    # --- Levenshtein distance (efficient 2-row DP) ---
    @staticmethod
    def _levenshtein(a, b):
        a = a.lower()
        b = b.lower()
        if len(a) < len(b):
            a, b = b, a  # ensure len(a) >= len(b)
        previous = list(range(len(b) + 1))
        for i, ca in enumerate(a, start=1):
            current = [i] + [0] * len(b)
            for j, cb in enumerate(b, start=1):
                insertions = previous[j] + 1
                deletions = current[j - 1] + 1
                substitutions = previous[j - 1] + (0 if ca == cb else 1)
                current[j] = min(insertions, deletions, substitutions)
            previous = current
        return previous[-1]

    def spell_check(self, word, max_suggestions=5):
        """Return nearest words by Levenshtein distance if any are close enough.

        If none are 'close' (distance threshold), return [].
        Threshold determined as max(1, round(len(word) * 0.4)).
        """
        all_words = self.get_all_words()
        if not all_words:
            return []

        # Compute distances and sort by (distance, word)
        distances = []
        for w in all_words:
            d = self._levenshtein(word, w)
            distances.append((d, w))
        distances.sort(key=lambda x: (x[0], x[1]))

        min_dist = distances[0][0]
        threshold = max(1, int(round(len(word) * 0.4)))

        if min_dist <= threshold:
            # collect all with distance <= threshold, up to max_suggestions
            suggestions = [w for d, w in distances if d <= threshold][:max_suggestions]
            return suggestions
        else:
            # No close matches
            return []
