"""VLLM inference script with batching support for Qwen models."""

import argparse
import os
import sys
from typing import List

# Set HuggingFace cache directory
HF_HOME = "/fs/nexus-scratch/adesai10"
os.environ["HF_HOME"] = HF_HOME
os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(HF_HOME, "hub")


def load_prompts_from_file(prompt_file: str) -> List[str]:
    """Load prompts from a text file."""
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
    return prompts


def check_model_cache(model_name: str) -> None:
    """Check if model is cached and print status."""
    # HuggingFace cache format: models--{org}--{model_name}
    cache_name = model_name.replace("/", "--")
    cache_dir = os.path.join(HF_HOME, "hub", f"models--{cache_name}")

    if os.path.exists(cache_dir):
        print(f"Found cached model at: {cache_dir}")
    else:
        print(f"Model not found in cache, will download to: {HF_HOME}/hub")


def run_inference(
    model_name: str,
    prompts: List[str],
    max_tokens: int = 2048,
    temperature: float = 0.7,
    top_p: float = 0.9,
    batch_size: int = 4,
    tensor_parallel_size: int = 1,
    max_model_len: int = None,
) -> List[str]:
    """Run inference using VLLM with batching."""
    from vllm import LLM, SamplingParams

    check_model_cache(model_name)

    print(f"Loading model: {model_name}")
    
    llm = LLM(
        model=model_name,
        trust_remote_code=True,
        max_model_len=max_model_len,
        tensor_parallel_size=tensor_parallel_size,
    )

    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stop=["### END"]
    )

    print(f"Running inference on {len(prompts)} prompts with batch size {batch_size}...")
    outputs = llm.generate(prompts, sampling_params)

    responses = []
    for output in outputs:
        generated_text = output.outputs[0].text
        responses.append(generated_text)

    return responses


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run inference using VLLM with batching on Qwen models"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-4B",
        help="Model name or path (default: Qwen/Qwen3-4B)",
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        required=True,
        help="Path to text file containing prompts (one per line)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Maximum tokens to generate (default: 2048)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9,
        help="Top-p sampling parameter (default: 0.9)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Batch size for inference (default: 4)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file to save results (optional)",
    )
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=1,
        help="Number of GPUs for tensor parallelism (default: 1)",
    )
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=None,
        help="Maximum model length (default: auto-detect based on model size)",
    )
    parser.add_argument(
        "--max-num-batched-tokens",
        type=int,
        default=None,
        help="Maximum number of batched tokens per iteration (default: auto-detect)",
    )
    parser.add_argument(
        "--max-num-seqs",
        type=int,
        default=None,
        help="Maximum number of sequences per batch (default: auto-detect)",
    )
    parser.add_argument(
        "--num-runs",
        type=int,
        default=1,
        help="Number of runs to generate (default: 1)",
    )
    parser.add_argument(
        "--output-prefix",
        type=str,
        help="Output file prefix for multiple runs (e.g., 'output/prefix' creates 'output/prefix_run1.txt', etc.)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.prompt_file):
        print(f"Error: Prompt file not found: {args.prompt_file}")
        sys.exit(1)

    prompts = load_prompts_from_file(args.prompt_file)
    print(f"Loaded {len(prompts)} prompts from {args.prompt_file}")

    if not prompts:
        print("Error: No prompts found in file.")
        sys.exit(1)

    # Load model once and reuse for all runs
    from vllm import LLM, SamplingParams

    check_model_cache(args.model)

    print(f"Loading model: {args.model}")
    
    llm = LLM(
        model=args.model,
        trust_remote_code=True,
        max_model_len=args.max_model_len,
        tensor_parallel_size=args.tensor_parallel_size,
        max_num_batched_tokens=args.max_num_batched_tokens,
        max_num_seqs=args.max_num_seqs,
    )
    
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        stop=["### END"]
    )

    for run_num in range(1, args.num_runs + 1):
        print(f"\n{'='*80}")
        print(f"Run {run_num}/{args.num_runs}")
        print(f"{'='*80}")
        
        print(f"Running inference on {len(prompts)} prompts...")
        outputs = llm.generate(prompts, sampling_params)

        responses = []
        for output in outputs:
            generated_text = output.outputs[0].text
            responses.append(generated_text)

        if args.output_prefix:
            output_file = f"{args.output_prefix}_run{run_num}.txt"
        elif args.output:
            if args.num_runs > 1:
                base_name, ext = os.path.splitext(args.output)
                output_file = f"{base_name}_run{run_num}{ext}"
            else:
                output_file = args.output
        else:
            output_file = None

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                for i, (prompt, response) in enumerate(zip(prompts, responses), 1):
                    f.write(f"=== Prompt {i} ===\n")
                    f.write(f"{response}\n\n")
            print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()

