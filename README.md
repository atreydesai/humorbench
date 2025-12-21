# From LOL to LLM: Measuring Multilingual Multi-Turn Humor Understanding in AI

This project implements a benchmark that evaluates how well language models understand multi-line humor across English and Spanish. The benchmark includes both standard evaluation tasks and robustness testing through various perturbations.

## Overview

The benchmark consists of two main tasks:
1. **Overall Joke Classification**: Classify the entire multi-line joke as funny or not funny
2. **Line Purpose Identification**: Identify the purpose that each line serves in developing the joke's punchline (e.g., setup, punchline, transition)

## Results

### Task 1: Overall Joke Classification

<p align="center">
  <img src="readme_figures/Task 1 Accuracy, Full Set.png" height="250" style="margin: 0 5px;" />
  <img src="readme_figures/Task 1 F1 Score, Full Set.png" height="250" style="margin: 0 5px;" />
  <img src="readme_figures/Task 1 AUC Score, Full Set.png" height="250" style="margin: 0 5px;" />
</p>

### Task 2: Line Purpose Identification

<p align="center">
  <img src="readme_figures/Task 2 Accuracy, Full Set.png" height="250" style="margin: 0 5px;" />
  <img src="readme_figures/Task 2 F1 Score, Full Set.png" height="250" style="margin: 0 5px;" />
  <img src="readme_figures/Task 2 AUC Score, Full Set.png" height="250" style="margin: 0 5px;" />
</p>

## Repository Structure

### Main Directories

- **`datasets/`**: Contains all datasets and prompts
  - `labeled/`: Labeled datasets for training and evaluation
    - `en_task1&2.tsv`: English labeled data
    - `es_labelled.tsv`: Spanish labeled data
    - `jokes_en/`: English perturbed joke datasets
    - `jokes_es/`: Spanish perturbed joke datasets
  - `en_prompts/`: English prompt files for tasks 1 and 2
  - `es_prompts/`: Spanish prompt files for tasks 1 and 2
  - `perturbed/`: English perturbed prompts (orthographic, semantic drift, semantic preserving, cultural)
  - `peturbed_es/`: Spanish perturbed prompts (orthographic/typo, semantic drift, semantic preserving)

- **`completions/`**: Model-generated completions organized by:
  - `en/`: English task completions
  - `es/`: Spanish task completions
  - `perturbed/`: English perturbed task completions
  - `perturbed_es/`: Spanish perturbed task completions

- **`results/`**: Evaluation results and metrics
  - Organized by language (`en/`, `es/`) and perturbation type
  - Contains CSV files with metrics and confusion matrices

- **`src/humorbench/`**: Source code modules

### Source Code Modules

- **`vllm_inference.py`**
- **`download_models.py`**: Script to download and cache all models used in evaluation
- **`eval_task1.py`**: Evaluation script for Task 1 (Overall Joke Classification)
- **`eval_task2.py`**: Evaluation script for Task 2 (Line Purpose Identification)
- **`eval_tasks.py`**: Combined evaluation for both tasks on English and Spanish datasets
- **`run_task.sh`**: Shell script for running inference on specific tasks/models
- **`generate_prompts.py`**: Script to generate prompts from labeled data
- **`prepare_es_dataset.py`**: Script to prepare Spanish dataset (includes YouTube transcript scraping)
- **`standup_sources.py`**

## Evaluated Models

The following models were evaluated on this benchmark:

- `Qwen/Qwen3-8B`
- `Qwen/Qwen3-32B`
- `allenai/Olmo-3-7B-Instruct`
- `allenai/Olmo-3.1-32B-Instruct`
- `tiiuae/Falcon3-10B-Instruct`
- `swiss-ai/Apertus-8B-Instruct-2509`
- `mistralai/Ministral-8B-Instruct-2410`

## Installation

### Prerequisites

- Python 3.10+
- Conda (for environment management)
- CUDA-capable GPU (for running VLLM inference)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd humorbench
   ```

2. **Create and activate a conda environment**
   ```bash
   conda create -n humorbench python=3.10
   conda activate humorbench
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Note: VLLM may require additional setup. Refer to the [VLLM documentation](https://docs.vllm.ai/) for detailed installation instructions, especially if you need CUDA support.

## Usage

### Download Models

To download and cache all models used in evaluation:

```bash
python -m humorbench.download_models
```

This will download models to the HuggingFace cache directory specified in the script (default: `/fs/nexus-scratch/adesai10/hub`).

### Run Inference

#### Basic inference on a prompt file:

```bash
python -m humorbench.vllm_inference --prompt-file demo_prompt.txt
```

#### Advanced inference with custom parameters:

```bash
python -m humorbench.vllm_inference \
    --prompt-file datasets/en_prompts/prompts_task1.txt \
    --model "Qwen/Qwen3-8B" \
    --max-tokens 1024 \
    --temperature 0.8 \
    --batch-size 8 \
    --output results.txt
```

#### Using the run_task.sh script:

Edit `src/humorbench/run_task.sh` to set:
- `MODEL`: The model to use (e.g., `mistralai/Ministral-8B-Instruct-2410`)
- `PROMPT_FILE`: Path to the prompt file

Then run:
```bash
cd src/humorbench
bash run_task.sh
```

The script automatically detects:
- Language (English/Spanish)
- Task number (1 or 2)
- Perturbation type (if applicable)
- Output directory structure

### Run Evaluation

#### Evaluate both tasks on English and Spanish datasets:

```bash
python -m humorbench.eval_tasks
```

#### Evaluate perturbed Spanish datasets:

```bash
python -m humorbench.eval_perturbed_es
```

#### Evaluate combined English and Spanish perturbed datasets:

```bash
python -m humorbench.eval_perturbed_combined
```

Evaluation scripts generate:
- CSV files with accuracy, F1, and AUC metrics (pass@1 and pass@5)
- Confusion matrices saved as images

Results are saved in the `results/` directory, organized by task, language, and perturbation type.

## Metrics

The evaluation reports the following metrics for each task:

- **Accuracy**: Overall classification accuracy
- **F1 Score**: Macro-averaged F1 score
- **AUC**: Area under the ROC curve

Metrics are computed for **Pass@1** and **Pass@5**.

## Perturbations

The benchmark includes several types of perturbations to test robustness:

### English Perturbations
- **Orthographic**: Spelling variations and typos
- **Semantic Drift**: Changes that alter meaning
- **Semantic Preserving**: Paraphrases that preserve meaning
- **Cultural**: Culture-specific variations

### Spanish Perturbations
- **Orthographic/Typo**: Spelling errors and typos
- **Semantic Drift**: Meaning-altering changes
- **Semantic Preserving**: Meaning-preserving paraphrases

## Citation

If you use this benchmark in your research, please cite:

```bibtex
@article{humorbench2024,
  title={From LOL to LLM: Measuring Multilingual Multi-Turn Humor Understanding in AI},
  author={Desai, Atrey and Du, Leo and van Doorn, James and Sreepada, Kamala},
  year={2025}
}
```