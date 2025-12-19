#!/bin/bash

#SBATCH --job-name=tasks1_2
#SBATCH --cpus-per-task=8
#SBATCH --mem=64g
#SBATCH --gres=gpu:rtxa6000:2
#SBATCH --qos=medium

MODEL=allenai/Olmo-3.1-32B-Instruct
PROMPT_FILE=/nfshomes/ldu0040/humorbench/datasets/perturbed/prompts_task2_sem_pres.txt
OUT_PREFIX=sem_pres_task2_olmo3-1-32b

srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run1.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run2.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run3.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run4.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run5.txt &
wait