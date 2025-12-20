from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol
import random

from .tokenization import tokenize, detokenize


# WordNet support
def _try_get_wordnet():
    try:
        import nltk
        from nltk.corpus import wordnet as wn 
        return nltk, wn
    except Exception:
        return None, None


def ensure_wordnet_downloaded() -> None:
    """
    If nltk isn't installed or downloads fail, synonym perturbation will no-op.
    """
    nltk, _ = _try_get_wordnet()
    if nltk is None:
        return
    try:
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
    except Exception:
        pass


class Perturbation(Protocol):
    name: str

    def apply(self, text: str) -> str: ...


@dataclass(frozen=True)
class Pipeline:
    name: str
    steps: List[Perturbation]

    def apply(self, text: str) -> str:
        for p in self.steps:
            text = p.apply(text)
        return text


# Lexical perturbations 
@dataclass(frozen=True)
class SynonymPerturbation:
    """
    WordNet synonym substitution. Supports multilingual lookups via OMW.

    synonym_lang:
      - "eng" for English (default)
      - "spa" for Spanish
    """
    name: str = "synonyms"
    prob: float = 0.2
    synonym_lang: str = "eng"
    _wn: object = None 

    def __post_init__(self):
        _, wn = _try_get_wordnet()
        object.__setattr__(self, "_wn", wn)

    def _get_synonym(self, word: str) -> str:
        wn = self._wn
        if wn is None:
            return word

        # NLTK WordNet supports lang= for multilingual synset lookup (OMW).
        try:
            synsets = wn.synsets(word, lang=self.synonym_lang)
        except TypeError:
            # Fallback for older interfaces
            synsets = wn.synsets(word)

        if not synsets:
            return word

        syn = random.choice(synsets)

        # Pull lemma names in the requested language if possible
        try:
            lemma_names = syn.lemma_names(lang=self.synonym_lang)
        except TypeError:
            lemma_names = [l.name() for l in syn.lemmas()]

        candidates = []
        for name in lemma_names:
            # Normalize underscores
            cand = name.replace("_", " ")
            if cand.lower() != word.lower():
                candidates.append(cand)

        return random.choice(candidates) if candidates else word

    def apply(self, text: str) -> str:
        tokens = tokenize(text)
        new_tokens: List[str] = []
        for tok in tokens:
            if tok.isalpha() and random.random() < self.prob:
                new_tokens.append(self._get_synonym(tok))
            else:
                new_tokens.append(tok)
        return detokenize(new_tokens)


@dataclass(frozen=True)
class SwapOrderPerturbation:
    name: str = "swap_word_order"
    swap_prob: float = 0.2

    def apply(self, text: str) -> str:
        tokens = tokenize(text)
        i = 0
        while i < len(tokens) - 1:
            if (
                tokens[i].isalpha()
                and tokens[i + 1].isalpha()
                and random.random() < self.swap_prob
            ):
                tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
                i += 2
            else:
                i += 1
        return detokenize(tokens)


# Orthographic perturbations
DEFAULT_KEYBOARD_NEIGHBORS: Dict[str, str] = {
    "a": "qws",
    "s": "awed",
    "d": "sfe",
    "e": "wsr",
    "o": "ip",
    "i": "uok",
    "n": "bhm",
}


def _random_typo(word: str, char_prob: float, keyboard_neighbors: Dict[str, str]) -> str:
    chars = list(word)
    i = 0
    out: List[str] = []
    while i < len(chars):
        c = chars[i]
        if random.random() < char_prob:
            op = random.choice(["sub", "del", "ins"])
            if op == "del":
                i += 1
                continue
            elif op == "sub":
                neighbors = keyboard_neighbors.get(c.lower(), "")
                out.append(random.choice(neighbors) if neighbors else c)
            elif op == "ins":
                neighbors = keyboard_neighbors.get(c.lower(), "")
                out.append(c)
                if neighbors:
                    out.append(random.choice(neighbors))
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


@dataclass(frozen=True)
class TypoPerturbation:
    name: str = "typos"
    word_prob: float = 0.2
    char_prob: float = 0.1
    keyboard_neighbors: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.keyboard_neighbors is None:
            object.__setattr__(self, "keyboard_neighbors", DEFAULT_KEYBOARD_NEIGHBORS)

    def apply(self, text: str) -> str:
        tokens = tokenize(text)
        new_tokens: List[str] = []
        for tok in tokens:
            if tok.isalpha() and random.random() < self.word_prob:
                new_tokens.append(
                    _random_typo(tok, self.char_prob, self.keyboard_neighbors)  # type: ignore[arg-type]
                )
            else:
                new_tokens.append(tok)
        return detokenize(new_tokens)


# Cultural / dialect shift
DEFAULT_CULTURAL_MAP: Dict[str, str] = {
    "soccer": "football",
    "fries": "chips",
    "chips": "crisps",
    "apartment": "flat",
    "truck": "lorry",
    "elevator": "lift",
    "candy": "sweets",
    "costco": "tesco",
    "walmart": "asda",
    "starbucks": "costa",
}


@dataclass(frozen=True)
class CulturalShiftPerturbation:
    name: str = "cultural_shift"
    mapping: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.mapping is None:
            object.__setattr__(self, "mapping", DEFAULT_CULTURAL_MAP)

    def apply(self, text: str) -> str:
        tokens = tokenize(text)
        new_tokens: List[str] = []
        for tok in tokens:
            key = tok.lower()
            if key in self.mapping:  # type: ignore[operator]
                repl = self.mapping[key]  # type: ignore[index]
                if tok and tok[0].isupper():
                    repl = repl.capitalize()
                new_tokens.append(repl)
            else:
                new_tokens.append(tok)
        return detokenize(new_tokens)


# Default pipelines
def make_default_pipelines(
    *,
    synonym_lang: str = "eng",
    include_cultural: bool = True,
) -> Dict[str, Perturbation]:
    """
    Returns perturbation configs.

    synonym_lang:
      - "eng" for English
      - "spa" for Spanish

    include_cultural:
      - True for English experiments
      - False for Spanish (per your plan)
    """
    ensure_wordnet_downloaded()

    semantic_preserving = Pipeline(
        name="semantic_preserving",
        steps=[
            SynonymPerturbation(prob=0.1, synonym_lang=synonym_lang),
            TypoPerturbation(word_prob=0.05, char_prob=0.05),
        ],
    )

    semantic_drift = Pipeline(
        name="semantic_drift",
        steps=[
            SynonymPerturbation(prob=0.4, synonym_lang=synonym_lang),
            SwapOrderPerturbation(swap_prob=0.3),
            TypoPerturbation(word_prob=0.3, char_prob=0.15),
        ],
    )

    ortho_typo = TypoPerturbation(name="ortho_typo", word_prob=0.3, char_prob=0.2)

    pipelines: Dict[str, Perturbation] = {
        "perturbed_joke_semantic_preserving": semantic_preserving,
        "perturbed_joke_semantic_drift": semantic_drift,
        "perturbed_joke_ortho_typo": ortho_typo,
    }

    if include_cultural:
        pipelines["perturbed_joke_cultural_shift"] = CulturalShiftPerturbation()

    return pipelines
