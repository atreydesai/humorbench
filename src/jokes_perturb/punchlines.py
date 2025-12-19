from __future__ import annotations

from dataclasses import dataclass
from .perturbations import Perturbation

@dataclass(frozen=True)
class PunchlineOnly:
    """
    Applies an inner perturbation ONLY to lines whose 
    corresponding Task2 label line is 'punchline'.
    
    """
    inner: Perturbation

    def apply_to_joke(self, full_joke_text: str, task2_label_text: str) -> str:
        j_lines = str(full_joke_text).split("\\n")
        l_lines = str(task2_label_text).split("\\n")

        out_lines = []
        for joke_line, label_line in zip(j_lines, l_lines):
            if label_line.strip() == "punchline":
                out_lines.append(self.inner.apply(joke_line))
            else:
                out_lines.append(joke_line)

        if len(j_lines) > len(l_lines):
            out_lines.extend(j_lines[len(l_lines):])

        return "\\n".join(out_lines)
