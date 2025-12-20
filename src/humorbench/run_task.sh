#!/bin/bash

#SBATCH --job-name=tasks1_2
#SBATCH --cpus-per-task=4
#SBATCH --mem=32g
#SBATCH --gres=gpu:rtxa6000:1
#SBATCH --qos=default

MODEL=tiiuae/Falcon3-10B-Instruct
PROMPT_FILE=/nfshomes/ldu0040/humorbench/datasets/es_prompts/prompts_task2_es.txt
OUT_PREFIX=es_task2_falcon3-10b

srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run1.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run2.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run3.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run4.txt &
srun python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 2048 --temperature 0.6 --top-p 0.95 --output ${OUT_PREFIX}_run5.txt &
wait