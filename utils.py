import functools
from typing import List, Generator

class FastFuzzyMatcher:
    """Optimized CLI command suggestion engine using pruned search."""
    def __init__(self, commands: List[str]):
        self.commands = commands

    @functools.lru_cache(maxsize=128)
    def _levenshtein(self, s1: str, s2: str, max_dist: int) -> int:
        if abs(len(s1) - len(s2)) > max_dist:
            return max_dist + 1
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            min_val = current_row[0]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                cost = min(insertions, deletions, substitutions)
                current_row.append(cost)
                min_val = min(min_val, cost)
            
            if min_val > max_dist:
                return max_dist + 1
            previous_row = current_row
            
        return previous_row[-1]

    def suggest(self, query: str, threshold: int = 2) -> Generator[str, None, None]:
        """Yields matches within the edit distance threshold."""
        for cmd in self.commands:
            if self._levenshtein(query, cmd, threshold) <= threshold:
                yield cmd