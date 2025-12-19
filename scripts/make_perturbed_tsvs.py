import argparse
from jokes_perturb.runner import generate_outputs

def main() -> None:
    ap = argparse.ArgumentParser(description="Generate perturbed joke TSV datasets.")
    ap.add_argument("--input", required=True, help="Path to en_task1&2.tsv")
    ap.add_argument("--outdir", required=True, help="Output directory for TSVs")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = ap.parse_args()

    generate_outputs(input_tsv=args.input, out_dir=args.outdir, seed=args.seed)

if __name__ == "__main__":
    main()
