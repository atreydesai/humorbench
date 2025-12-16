import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extract_answers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on === Prompt i ===
    blocks = re.split(r"=== Prompt \d+ ===", text)

    results = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract the first array object in the block
        matches = re.findall(r"\{.*\}", block, re.DOTALL)
        if not matches:
            results.append("")
            continue

        json_str = matches[-1]

        try:
            parsed = json.loads(json_str)
            results.append(parsed['category'])
        except json.JSONDecodeError:
            # Skip malformed entries
            continue

    return results

def insert_answers(output_list, completions):
    for i in range(len(completions)):
        if i > len(output_list) - 1:
            output_list.append([])
        output_list[i].append(completions[i])
    return output_list

def eval_pass_at_k(completions, ground_truths, k):
    '''
    completions: Should be of shape NUM_QUESTIONS x NUM_COMPLETIONS x NUM_LINES, type list[list[list[str]]]
        NUM_QUESTIONS = number of jokes that we want to evaluate on
        NUM_COMPLETIONS = number of completions per joke, >= k
        NUM_LINES = number of lines per joke
    ground_truths: Should be shape NUM_QUESTIONS x NUM_LINES, type list[list[str]]
        NUM_QUESTIONS = number of jokes that we want to evaluate on
        NUM_LINES = number of lines per joke
    k: int
    '''

    total = 0
    num_correct = 0
    labels = [
        'satire',
        'parody',
        'irony',
        'aggressive',
        'dry',
        'self-deprecating',
        'surreal/absurdism',
        'wordplay',
        'witty',
        'topical',
        'observational/anecdotal',
        'dark',
        'NA'
    ]
    confusion_matrix = {}
    for label in labels:
        confusion_matrix[label] = {}
        for l in labels:
            confusion_matrix[label][l] = 0

    for completion, truth in zip(completions, ground_truths):
        correct = False
        while len(completion) < k:
            completion.append("")
        for i in range(k):
            if i < len(completion):
                pred = completion[i]
            else:
                pred = 'NA'
            if truth in confusion_matrix:
                sub_matrix = confusion_matrix[truth]
            else:
                sub_matrix = confusion_matrix['NA']
            if pred in sub_matrix:
                sub_matrix[pred] += 1
            else:
                sub_matrix['NA'] += 1
            correct = correct or (truth == pred)
        if correct:
            num_correct += 1
        total += 1
    return num_correct, total, confusion_matrix

def main():
    completions = extract_answers("/nfshomes/ldu0040/humorbench/src/humorbench/en_task1_qwen3-8b_run1.txt")
    out1 = insert_answers([], completions)
    dataset = pd.read_csv('../../datasets/labeled/en_task1&2.tsv', sep='\t')
    task1 = dataset[['Joke', 'Task1 Label']].copy().dropna()
    labels = task1['Task1 Label'].tolist()[:len(completions)]
    num_correct, total, cm = eval_pass_at_k(out1, labels, 1)
    print(num_correct, total)
    cm_df = pd.DataFrame.from_dict(cm, orient="index")

    ls = sorted(cm_df.columns)
    cm_r = cm_df.reindex(index=ls, columns=ls, fill_value=0)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm_r,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=ls,
        yticklabels=ls
    )

    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Task 1 Confusion Matrix")
    plt.tight_layout()
    plt.savefig("task1_confusion_matrix.png")

if __name__ == "__main__":
    main()