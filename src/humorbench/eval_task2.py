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
            results.append([])
            continue

        json_str = matches[-1]

        try:
            parsed = json.loads(json_str)
            results.append(parsed['ANSWER'])
        except json.JSONDecodeError:
            results.append([])
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
        'establishing context',
        'escalation',
        'subversion',
        'callback',
        'misdirection',
        'timing',
        'meta-humor',
        'punchline',
        'redirection',
        'non-line',
        'wrap-up',
        'repetition',
        'setup',
        'NA'
    ]
    confusion_matrix = {}
    for label in labels:
        confusion_matrix[label] = {}
        for l in labels:
            confusion_matrix[label][l] = 0

    for completion, truths in zip(completions, ground_truths):
        for i in range(len(truths)):
            truth = truths[i]
            correct = False
            while len(completion) < k:
                completion.append([])
            for j in range(k):
                if j < len(completion):
                    comp = completion[j]
                else:
                    comp = []
                if i < len(comp):
                    pred = comp[i]
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
    completions = extract_answers("task2_comps_1.txt")
    dataset = pd.read_csv('../../datasets/labeled/a-e labels.tsv', sep='\t')
    task2 = dataset[['Joke', 'Task2 Label']].copy().dropna()
    truths = task2['Task2 Label'].apply(lambda x: x.split("\\n")).tolist()[:len(completions)]

    out = insert_answers([], completions)

    num_correct, total, cm = eval_pass_at_k(out, truths, 1)
    print(num_correct, total)
    cm_df = pd.DataFrame.from_dict(cm, orient="index")

    labels = sorted(cm_df.columns)
    cm_r = cm_df.reindex(index=labels, columns=labels, fill_value=0)

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm_r,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels
    )

    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Task 2 Confusion Matrix")
    plt.tight_layout()
    plt.savefig("task2_confusion_matrix.png")

if __name__ == '__main__':
    main()