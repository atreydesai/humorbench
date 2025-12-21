from eval_task1 import eval_task1
from eval_task2 import eval_task2
import pandas as pd
import os

if __name__ == "__main__":

    # Define perturbation types and their corresponding dataset column names
    perturb_types = {
        "ortho_typo": "perturbed_joke_ortho_typo",
        "semantic_drift": "perturbed_joke_semantic_drift",
        "semantic_preserving": "perturbed_joke_semantic_preserving"
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

    base_dataset_path = "/fs/clip-projects/rlab/atrey/humorbench/datasets/labeled/jokes_es"
    base_run_path = "/fs/clip-projects/rlab/atrey/humorbench/completions/perturbed_es"
    base_out_path = "/fs/clip-projects/rlab/atrey/humorbench/results/perturbed_es"
    base_cm_save_path = "/fs/clip-projects/rlab/atrey/humorbench/results/perturbed_es"

    # Process each perturbation type
    for perturb_type, joke_col_name in perturb_types.items():
        print(f"\n{'='*80}")
        print(f"Processing perturbation type: {perturb_type}")
        print(f"{'='*80}\n")

        # Set up paths for this perturbation type
        dataset_path = os.path.join(base_dataset_path, f"jokes_{perturb_type}.tsv")
        run_path_pref = os.path.join(base_run_path, f"{perturb_type}")
        out_path = os.path.join(base_out_path, f"{perturb_type}/csvs/{perturb_type}")
        cm_save_path = os.path.join(base_cm_save_path, f"{perturb_type}/confusion_matrices/")

        # Create output directories
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        os.makedirs(cm_save_path, exist_ok=True)

        # Initialize results dictionaries for this perturbation type
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

        # Evaluate each model
        for model in models:
            print(f"Evaluating model: {model} for {perturb_type}")
            
            task1_run_path = os.path.join(run_path_pref, f"{model}/{perturb_type}_task1_{model}")
            task1_cm_save_path = os.path.join(cm_save_path, f"task1_confusion_matrix_{model}")
            task2_run_path = os.path.join(run_path_pref, f"{model}/{perturb_type}_task2_{model}")
            task2_cm_save_path = os.path.join(cm_save_path, f"task2_confusion_matrix_{model}")

            # Check if run files exist
            if not os.path.exists(f"{task1_run_path}_run1.txt"):
                print(f"Warning: Task1 run files not found for {model} at {task1_run_path}")
                continue

            if not os.path.exists(f"{task2_run_path}_run1.txt"):
                print(f"Warning: Task2 run files not found for {model} at {task2_run_path}")
                continue

            # Evaluate Task 1
            try:
                pass_at_1_task1, pass_at_5_task1 = eval_task1(
                    dataset_path, task1_run_path, task1_cm_save_path, joke_col_name, model
                )

                task_1_results_dict['model'].append(model)
                task_1_results_dict['pass@1_acc'].append(pass_at_1_task1[0])
                task_1_results_dict['pass@1_f1'].append(pass_at_1_task1[1])
                task_1_results_dict['pass@1_auc'].append(pass_at_1_task1[2])
                task_1_results_dict['pass@5_acc'].append(pass_at_5_task1[0])
                task_1_results_dict['pass@5_f1'].append(pass_at_5_task1[1])
                task_1_results_dict['pass@5_auc'].append(pass_at_5_task1[2])
            except Exception as e:
                print(f"Error evaluating Task1 for {model}: {e}")
                continue

            # Evaluate Task 2
            try:
                pass_at_1_task2, pass_at_5_task2 = eval_task2(
                    dataset_path, task2_run_path, task2_cm_save_path, joke_col_name, model
                )

                task_2_results_dict['model'].append(model)
                task_2_results_dict['pass@1_acc'].append(pass_at_1_task2[0])
                task_2_results_dict['pass@1_f1'].append(pass_at_1_task2[1])
                task_2_results_dict['pass@1_auc'].append(pass_at_1_task2[2])
                task_2_results_dict['pass@5_acc'].append(pass_at_5_task2[0])
                task_2_results_dict['pass@5_f1'].append(pass_at_5_task2[1])
                task_2_results_dict['pass@5_auc'].append(pass_at_5_task2[2])
            except Exception as e:
                print(f"Error evaluating Task2 for {model}: {e}")
                continue

        # Save results for this perturbation type
        if task_1_results_dict['model']:
            task1_res_df = pd.DataFrame(task_1_results_dict)
            task1_res_df.to_csv(f"{out_path}_task1_res.csv", index=False)
            print(f"Saved Task1 results to {out_path}_task1_res.csv")

        if task_2_results_dict['model']:
            task2_res_df = pd.DataFrame(task_2_results_dict)
            task2_res_df.to_csv(f"{out_path}_task2_res.csv", index=False)
            print(f"Saved Task2 results to {out_path}_task2_res.csv")

    print("\n" + "="*80)
    print("Evaluation complete for all perturbation types!")
    print("="*80)

