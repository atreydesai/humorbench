import argparse
from jokes_perturb.runner import generate_outputs


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate perturbed joke TSV datasets.")
    ap.add_argument("--input", required=True, help="Path to labelled TSV (e.g., en_task1&2.tsv or es_labelled.tsv)")
    ap.add_argument("--outdir", required=True, help="Output directory for TSVs (e.g., perturbed_en, perturbed_es)")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")

    # Language settings for synonym perturbation via WordNet/OMW
    ap.add_argument(
        "--synlang",
        default="eng",
        choices=["eng", "spa"],
        help='WordNet language code for synonyms: "eng" for English, "spa" for Spanish.',
    )

    # Spanish run: set this flag
    ap.add_argument(
        "--no-cultural",
        action="store_true",
        help="Disable cultural/dialect shift perturbation",
    )

    args = ap.parse_args()

    generate_outputs(
        input_tsv=args.input,
        out_dir=args.outdir,
        seed=args.seed,
        synonym_lang=args.synlang,
        include_cultural=(not args.no_cultural),
    )


if __name__ == "__main__":
    main()
