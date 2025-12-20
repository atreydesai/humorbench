from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

from .punchlines import PunchlineOnly
from .perturbations import Perturbation, make_default_pipelines


@dataclass(frozen=True)
class RunConfig:
    input_tsv: str
    out_dir: str
    seed: Optional[int] = None
    synonym_lang: str = "eng"          # "eng" or "spa"
    include_cultural: bool = True      # False for Spanish


def set_seed(seed: Optional[int]) -> None:
    if seed is not None:
        random.seed(seed)


def _default_filename_for_column(out_col: str) -> str:
    # "perturbed_joke_semantic_preserving" -> "jokes_semantic_preserving.tsv"
    if not out_col.startswith("perturbed_joke_"):
        return f"{out_col}.tsv"
    suffix = out_col[len("perturbed_joke_") :]
    return f"jokes_{suffix}.tsv"


def generate_outputs(
    input_tsv: str,
    out_dir: str,
    seed: Optional[int] = None,
    pipelines: Optional[Dict[str, Perturbation]] = None,
    *,
    synonym_lang: str = "eng",
    include_cultural: bool = True,
) -> None:
    os.makedirs(out_dir, exist_ok=True)
    set_seed(seed)

    df = pd.read_csv(input_tsv, sep="\t")

    required = {"Joke", "Task1 Label", "Task2 Label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in input TSV: {sorted(missing)}")

    if pipelines is None:
        pipelines = make_default_pipelines(
            synonym_lang=synonym_lang,
            include_cultural=include_cultural,
        )

    # Apply each perturbation to punchlines only
    for out_col, perturb in pipelines.items():
        wrapper = PunchlineOnly(inner=perturb)
        df[out_col] = df.apply(
            lambda r: wrapper.apply_to_joke(r["Joke"], r["Task2 Label"]),
            axis=1,
        )

    output_columns = ["Task1 Label", "Task2 Label"]

    # Write one TSV per perturbation
    mapping: Dict[str, str] = {out_col: _default_filename_for_column(out_col) for out_col in pipelines.keys()}

    for out_col, filename in mapping.items():
        path = os.path.join(out_dir, filename)
        df[[out_col] + output_columns].to_csv(path, sep="\t", index=False)

    # Save metadata for reproducibility
    meta = {
        "input_tsv": input_tsv,
        "seed": seed,
        "row_count": int(len(df)),
        "synonym_lang": synonym_lang,
        "include_cultural": include_cultural,
        "outputs": {k: os.path.join(out_dir, v) for k, v in mapping.items()},
    }
    with open(os.path.join(out_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print("All perturbed datasets created and saved:")
    for filename in mapping.values():
        print(" -", os.path.join(out_dir, filename))
    print("Metadata:", os.path.join(out_dir, "metadata.json"))
