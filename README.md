# From LOL to LLM: Measuring Multilingual Multi-Turn Humor Understanding in AI

This project implements a benchmark that aims to understand how well models do in understanding multi-line humor.

There are two tasks:
1. Overall Joke Classification: Classify the entire multi-line joke.
2. Line Purpose Identification: Identify the purpose that a line in a joke serves in developing the joke's punchline.

The raw labeled datasets can be found in `datasets/labeled`.  
The prompts generated from the datasets can be found in `datasets/en_prompts`, `datasets/es_prompts`, and `datasets/perturbed`.

We evaluated the following models:
- Qwen/Qwen3-8B
- Qwen/Qwen3-32B
- allenai/Olmo-3-7B-Instruct
- allenai/Olmo-3.1-32B-Instruct
- tiiuae/Falcon3-10B-Instruct
- swiss-ai/Apertus-8B-Instruct-2509
- mistralai/Ministral-8B-Instruct-2410

Model completions can be found in the `completions/` folder.  
Performance metrics and confusion matrices can be found in `results/`.  
All python files used for this project can be found in `src/humorbench`.

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/humorbench.git
cd humorbench

# Install dependencies
uv sync


# Format and lint code
uv run ruff check .

```

```
python -m humorbench.vllm_inference --prompt-file demo_prompt.txt

python -m humorbench.vllm_inference \
    --prompt-file demo_prompt.txt \
    --model "Qwen/Qwen2.5-7B-Instruct" \
    --max-tokens 1024 \
    --temperature 0.8 \
    --batch-size 8

python -m humorbench.vllm_inference \
    --prompt-file demo_prompt.txt \
    --output results.txt

python -m humorbench.vllm_inference \
    --prompt-file demo_prompt.txt \
    --model "meta-llama/Llama-3.1-8B-Instruct"
```
