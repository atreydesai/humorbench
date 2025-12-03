# HumorBench

[FILL IN DESCRIPTION HERE]

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