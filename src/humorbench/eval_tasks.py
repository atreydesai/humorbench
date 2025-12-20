from eval_task1 import eval_task1
from eval_task2 import eval_task2
import pandas as pd

if __name__ == "__main__":

    task_1_results_dict = {
        "model": [],
        "pass@1_acc": [],
        "pass@1_f1": [],
        "pass@1_auc": [],
        "pass@5_acc": [],
        "pass@5_f1": [],
        "pass@5_auc": [],
    }

    task_2_results_dict = {
        "model": [],
        "pass@1_acc": [],
        "pass@1_f1": [],
        "pass@1_auc": [],
        "pass@5_acc": [],
        "pass@5_f1": [],
        "pass@5_auc": [],
    }

    models = [
        "qwen3-8b", 
        "qwen3-32b", 
        "olmo3-7b",
        "olmo3-1-32b",
        "falcon3-10b",
        "apertus-8b",
        "ministral-8b"
    ]
    dataset_path = "../../datasets/labeled/es_labelled.tsv"
    # run_path_pref = "/nfshomes/ldu0040/humorbench/completions/es/"
    # out_path = "/nfshomes/ldu0040/humorbench/results/es/csvs/es"
    # cm_save_path = "/nfshomes/ldu0040/humorbench/results/es/confusion_matrices/"
    run_path_pref = "/fs/clip-projects/rlab/atrey/humorbench/completions/es/"
    out_path = "/fs/clip-projects/rlab/atrey/humorbench/results/es/csvs/es"
    cm_save_path = "/fs/clip-projects/rlab/atrey/humorbench/results/es/confusion_matrices/"
    joke_col_name = "Joke"

    for model in models:
        print("Evaluating model: ", model)
        task1_run_path = run_path_pref + f"{model}/es_task1_{model}"
        task1_cm_save_path = cm_save_path + f"task1_confusion_matrix_{model}"
        task2_run_path = run_path_pref + f"{model}/es_task2_{model}"
        task2_cm_save_path = cm_save_path + f"task2_confusion_matrix_{model}"
    
        pass_at_1_task1, pass_at_5_task1 = eval_task1(dataset_path, task1_run_path, task1_cm_save_path, joke_col_name, model)

        task_1_results_dict['model'].append(model)
        task_1_results_dict['pass@1_acc'].append(pass_at_1_task1[0])
        task_1_results_dict['pass@1_f1'].append(pass_at_1_task1[1])
        task_1_results_dict['pass@1_auc'].append(pass_at_1_task1[2])
        task_1_results_dict['pass@5_acc'].append(pass_at_5_task1[0])
        task_1_results_dict['pass@5_f1'].append(pass_at_5_task1[1])
        task_1_results_dict['pass@5_auc'].append(pass_at_5_task1[2])

        pass_at_1_task2, pass_at_5_task2 = eval_task2(dataset_path, task2_run_path, task2_cm_save_path, joke_col_name, model)

        task_2_results_dict['model'].append(model)
        task_2_results_dict['pass@1_acc'].append(pass_at_1_task2[0])
        task_2_results_dict['pass@1_f1'].append(pass_at_1_task2[1])
        task_2_results_dict['pass@1_auc'].append(pass_at_1_task2[2])
        task_2_results_dict['pass@5_acc'].append(pass_at_5_task2[0])
        task_2_results_dict['pass@5_f1'].append(pass_at_5_task2[1])
        task_2_results_dict['pass@5_auc'].append(pass_at_5_task2[2])

    task1_res_df = pd.DataFrame(task_1_results_dict)
    task2_res_df = pd.DataFrame(task_2_results_dict)

    task1_res_df.to_csv(f"{out_path}_task1_res.csv", index=False)
    task2_res_df.to_csv(f"{out_path}_task2_res.csv", index=False)