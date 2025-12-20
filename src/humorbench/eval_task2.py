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
            results.append([])
            continue

        # Extract the first array object in the block
        matches = re.findall(r"\{.*\}", block, re.DOTALL)
        if not matches:
            results.append([])
            continue

        json_str = matches[-1]

        try:
            parsed = json.loads(json_str)
            if 'ANSWER' not in parsed:
                results.append([])
            else:
                results.append(parsed['ANSWER'])
        except (json.JSONDecodeError, KeyError):
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
    y_true = []
    y_pred = []

    confusion_matrix = {}
    for label in labels:
        confusion_matrix[label] = {}
        for l in labels:
            confusion_matrix[label][l] = 0

    for completion, truths in zip(completions, ground_truths):
        for i in range(len(truths)):
            truth = truths[i]
            truth = truth.strip().lower()
            if truth == 'surreal' or truth == 'absurdism':
                truth = 'surreal/absurdism'
            if truth == 'observational' or truth == 'anecdotal':
                truth = 'observational/anecdotal'
            if 'escalation' in truth or 'counter-escalation' in truth:
                truth = 'escalation'
            if "context" in truth or 'establishing' in truth:
                truth = 'establishing context'
            if "setup" in truth or 'continuation' in truth:
                truth = 'setup'
            if 'reaction' in truth or 'interruption' in truth or 'interaction' in truth:
                truth = 'timing'
            if "punchline" in truth:
                truth = 'punchline'
            if "transition" in truth or 'reflection' in truth:
                truth = 'redirection'
            correct = False
            while len(completion) < k:
                completion.append([])
            for j in range(k):
                if j < len(completion):
                    comp = completion[j]
                else:
                    comp = []
                if i < len(comp):
                    pred = comp[i].strip().lower()
                else:
                    pred = 'NA'
                if pred == 'surreal' or pred == 'absurdism':
                    pred = 'surreal/absurdism'
                if pred == 'observational' or pred == 'anecdotal':
                    pred = 'observational/anecdotal'
                if truth in confusion_matrix:
                    sub_matrix = confusion_matrix[truth]
                else:
                    sub_matrix = confusion_matrix['NA']
                    truth = 'NA'
                if pred in sub_matrix:
                    sub_matrix[pred] += 1
                else:
                    sub_matrix['NA'] += 1
                    pred = 'NA'
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

def eval_task2(dataset_path, run_path, save_path, joke_col_name, model):
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
    task2 = dataset[[joke_col_name, 'Task2 Label']].copy().dropna()
    truths = task2['Task2 Label'].apply(lambda x: x.split("\\n")).tolist()[:len(comp1)]

    num_correct, total, cm, f1, auc = eval_pass_at_k(out, truths, 1)
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
    plt.title(f"Task 2 Confusion Matrix {model} Pass@1")
    plt.tight_layout()
    plt.savefig(f"{save_path}_pass@1.png")
    plt.close()

    num_correct, total, cm, f1, auc = eval_pass_at_k(out, truths, 5)
    print("===== Pass@5 =====")
    print("Correct: ", num_correct)
    print("Total: ", total)
    print("Accuracy: ", num_correct / total)
    print("F1 Score: ", f1)
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
    plt.title(f"Task 2 Confusion Matrix {model} Pass@5")
    plt.tight_layout()
    plt.savefig(f"{save_path}_pass@5.png")
    plt.close()
    return pass_at_1_metrics, pass_at_5_metrics