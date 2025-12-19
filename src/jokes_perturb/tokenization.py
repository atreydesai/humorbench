import re
from typing import List

# Matches "words" or any single non-whitespace char
WORD_RE = re.compile(r"\w+|\S")

def tokenize(text: str) -> List[str]:
    """Very rough tokenizer: words + punctuation as separate tokens."""
    return WORD_RE.findall(text)

def detokenize(tokens: List[str]) -> str:
    """
    Simple detokenizer.
    """
    out = ""
    for t in tokens:
        if re.match(r"\w", t) and out and out[-1].isalnum():
            out += " " + t
        else:
            out += t
    return out
