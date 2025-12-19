import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.preprocessing import label_binarize

def extract_answers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on === Prompt i ===
    blocks = re.split(r"=== Prompt \d+ ===", text)

    results = []

    for block in blocks:
        block = block.strip()
        if not block:
            results.append("")
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
            results.append("")
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

    y_true = []
    y_pred = []

    confusion_matrix = {}
    for label in labels:
        confusion_matrix[label] = {}
        for l in labels:
            confusion_matrix[label][l] = 0

    for completion, truth in zip(completions, ground_truths):
        truth = truth.strip()
        if truth == 'surreal' or truth == 'absurdism':
            truth = 'surreal/absurdism'
        if truth == 'observational' or truth == 'anecdotal':
            truth = 'observational/anecdotal'
        correct = False
        while len(completion) < k:
            completion.append("")
        for i in range(k):
            if i < len(completion):
                pred = completion[i].strip()
            else:
                pred = 'NA'
            if truth in confusion_matrix:
                sub_matrix = confusion_matrix[truth]
            else:
                sub_matrix = confusion_matrix['NA']
                truth = 'NA'
            if pred == 'surreal' or pred == 'absurdism':
                pred = 'surreal/absurdism'
            if pred == 'observational' or pred == 'anecdotal':
                pred = 'observational/anecdotal'
            if pred in sub_matrix:
                sub_matrix[pred] += 1
            else:
                sub_matrix['NA'] += 1
            y_true.append(truth)
            y_pred.append(pred)
            correct = correct or (truth == pred)
        if correct:
            num_correct += 1
        total += 1
    f1 = f1_score(y_true, y_pred, average="macro")

    classes = np.unique(y_true)
    y_true_bin = label_binarize(y_true, classes=classes)
    y_pred_bin = label_binarize(y_pred, classes=classes)

    auc = roc_auc_score(
        y_true_bin,
        y_pred_bin,
        average="macro",
        multi_class="ovr"
    )

    return num_correct, total, confusion_matrix, f1, auc

def eval_task1(dataset_path, run_path, save_path, joke_col_name):
    print("Extracting Run 1")
    comp1 = extract_answers(f"{run_path}_run1.txt")
    print("Extracting Run 2")
    comp2 = extract_answers(f"{run_path}_run2.txt")
    print("Extracting Run 3")
    comp3 = extract_answers(f"{run_path}_run3.txt")
    print("Extracting Run 4")
    comp4 = extract_answers(f"{run_path}_run4.txt")
    print("Extracting Run 5")
    comp5 = extract_answers(f"{run_path}_run5.txt")
    out = insert_answers([], comp1)
    out = insert_answers(out, comp2)
    out = insert_answers(out, comp3)
    out = insert_answers(out, comp4)
    out = insert_answers(out, comp5)
    dataset = pd.read_csv(dataset_path, sep='\t')
    task1 = dataset[[joke_col_name, 'Task1 Label']].copy().dropna()
    labels = task1['Task1 Label'].tolist()[:len(comp1)]
    num_correct, total, cm, f1, auc = eval_pass_at_k(out, labels, 1)
    print("===== Pass@1 =====")
    print("Correct: ", num_correct)
    print("Total: ", total)
    print("Accuracy: ", num_correct / total)
    print("F1 Score: ", f1)
    print("AUC: ", auc)
    pass_at_1_metrics = (num_correct / total, f1, auc)
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
    plt.title("Task 1 Confusion Matrix Qwen3-8b Pass@1")
    plt.tight_layout()
    plt.savefig(f"{save_path}_pass@1.png")
    plt.close()

    num_correct, total, cm, f1, auc = eval_pass_at_k(out, labels, 5)
    print("===== Pass@5 =====")
    print("Correct: ", num_correct)
    print("Total: ", total)
    print("Accuracy: ", num_correct / total)
    print("F1: ", f1)
    print("AUC: ", auc)
    pass_at_5_metrics = (num_correct / total, f1, auc)
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
    plt.title("Task 1 Confusion Matrix Qwen3-8b Pass@5")
    plt.tight_layout()
    plt.savefig(f"{save_path}_pass@5.png")
    plt.close()

    return pass_at_1_metrics, pass_at_5_metrics