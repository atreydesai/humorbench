#!/bin/bash

# Qwen/Qwen3-8B
# Qwen/Qwen3-32B
# allenai/Olmo-3-7B-Instruct
# allenai/Olmo-3.1-32B-Instruct
# tiiuae/Falcon3-10B-Instruct (CURRENTLY UNAVAILABLE)
# swiss-ai/Apertus-8B-Instruct-2509
# mistralai/Ministral-8B-Instruct-2410 


MODEL=mistralai/Ministral-8B-Instruct-2410 
PROMPT_FILE=/fs/clip-projects/rlab/atrey/humorbench/datasets/peturbed_es/prompts_task2_jokes_semantic_preserving.txt


if [[ $PROMPT_FILE == *"/peturbed_es/"* ]]; then
    LANG="es"
    IS_PERTURBED_ES=true
elif [[ $PROMPT_FILE == *"/perturbed/"* ]]; then
    LANG="en"
    IS_PERTURBED=true
elif [[ $PROMPT_FILE == *"/es_prompts/"* ]]; then
    LANG="es"
    IS_PERTURBED_ES=false
    IS_PERTURBED=false
elif [[ $PROMPT_FILE == *"/en_prompts/"* ]]; then
    LANG="en"
    IS_PERTURBED_ES=false
    IS_PERTURBED=false
else
    echo "Error: Could not determine language from prompt file path"
    exit 1
fi

if [[ $PROMPT_FILE == *"task1"* ]]; then
    TASK="1"
elif [[ $PROMPT_FILE == *"task2"* ]]; then
    TASK="2"
else
    echo "Error: Could not determine task number from prompt file name"
    exit 1
fi

PERTURB_TYPE=""
if [[ "$IS_PERTURBED_ES" == true ]]; then
    if [[ $PROMPT_FILE == *"ortho_typo"* ]]; then
        PERTURB_TYPE="ortho_typo"
    elif [[ $PROMPT_FILE == *"semantic_drift"* ]]; then
        PERTURB_TYPE="semantic_drift"
    elif [[ $PROMPT_FILE == *"semantic_preserving"* ]]; then
        PERTURB_TYPE="semantic_preserving"
    else
        echo "Error: Could not determine perturbation type from prompt file name"
        exit 1
    fi
fi

MODEL_SHORT=$(echo "$MODEL" | sed 's|.*/||' | tr '[:upper:]' '[:lower:]' | sed 's/\./-/g' | sed 's/-instruct-[0-9]*$//' | sed 's/-instruct$//' | sed 's/olmo-3-7b/olmo3-7b/' | sed 's/olmo-3-1-32b/olmo3-1-32b/')

if [[ "$IS_PERTURBED_ES" == true ]]; then
    OUTPUT_DIR="/fs/clip-projects/rlab/atrey/humorbench/completions/perturbed_es/${PERTURB_TYPE}/${MODEL_SHORT}"
    OUT_PREFIX="${PERTURB_TYPE}_task${TASK}_${MODEL_SHORT}"
elif [[ "$IS_PERTURBED" == true ]]; then
    if [[ $PROMPT_FILE == *"cultural"* ]]; then
        PERTURB_TYPE="cultural"
    elif [[ $PROMPT_FILE == *"ortho"* ]]; then
        PERTURB_TYPE="ortho"
    elif [[ $PROMPT_FILE == *"sem_drift"* ]]; then
        PERTURB_TYPE="sem_drift"
    elif [[ $PROMPT_FILE == *"sem_pres"* ]]; then
        PERTURB_TYPE="sem_pres"
    fi
    OUTPUT_DIR="/fs/clip-projects/rlab/atrey/humorbench/completions/perturbed/${PERTURB_TYPE}/${MODEL_SHORT}"
    OUT_PREFIX="${PERTURB_TYPE}_task${TASK}_${MODEL_SHORT}"
else
    OUTPUT_DIR="/fs/clip-projects/rlab/atrey/humorbench/completions/${LANG}/${MODEL_SHORT}"
    OUT_PREFIX="${LANG}_task${TASK}_${MODEL_SHORT}"
fi

mkdir -p "$OUTPUT_DIR"

echo "Model: $MODEL"
echo "Model short: $MODEL_SHORT"
echo "Language: $LANG"
echo "Task: $TASK"
if [[ "$IS_PERTURBED_ES" == true ]]; then
    echo "Perturbation type: $PERTURB_TYPE"
fi
echo "Output directory: $OUTPUT_DIR"
echo "Output prefix: $OUT_PREFIX"

if [[ $MODEL == *"32B"* ]] || [[ $MODEL == *"32b"* ]]; then
    TENSOR_PARALLEL=2
    echo "Large model detected. Using tensor_parallel_size=$TENSOR_PARALLEL"
else
    TENSOR_PARALLEL=1
fi

python vllm_inference.py --model $MODEL --prompt-file $PROMPT_FILE --max-tokens 512 --temperature 0.6 --top-p 0.95 --tensor-parallel-size $TENSOR_PARALLEL --num-runs 5 --output-prefix ${OUTPUT_DIR}/${OUT_PREFIX}