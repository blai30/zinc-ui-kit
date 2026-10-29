from __future__ import annotations

from dataclasses import dataclass

MATCH = 10
CONTIGUOUS_BONUS = 5
WORD_START_BONUS = 8
MAX_GAP_PENALTY = 5
LABEL_BONUS = 50


@dataclass(frozen=True)
class Entry:
    name: str
    label: str
    path: str = ""
    shortcut: str = ""


def score(query: str, text: str) -> int | None:
    # Every query character must appear in order. None means no match.
    query = query.lower().replace(" ", "")
    if not query:
        return 0
    lowered = text.lower()
    position = 0
    previous = -2
    total = 0
    for character in query:
        found = lowered.find(character, position)
        if found == -1:
            return None
        total += MATCH
        if found == previous + 1:
            total += CONTIGUOUS_BONUS
        if found == 0 or not lowered[found - 1].isalnum():
            total += WORD_START_BONUS
        total -= min(found - position, MAX_GAP_PENALTY)
        previous = found
        position = found + 1
    # Prefer shorter text when everything else ties.
    return total - len(lowered) // 10


def _entry_score(query: str, entry: Entry) -> int | None:
    # A match in the label outranks a match that only exists through the menu path.
    label_score = score(query, entry.label)
    if label_score is not None:
        return label_score + LABEL_BONUS
    return score(query, f"{entry.path} {entry.label}".strip())


def rank(query: str, entries: list, limit: int = 30) -> list:
    if not query.strip():
        return sorted(entries, key=lambda entry: entry.label.lower())[:limit]
    scored = []
    for entry in entries:
        value = _entry_score(query, entry)
        if value is not None:
            scored.append((value, entry))
    scored.sort(key=lambda pair: (-pair[0], pair[1].label.lower()))
    return [entry for _, entry in scored[:limit]]
