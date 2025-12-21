from eval_task1 import eval_task1
from eval_task2 import eval_task2
import pandas as pd
import os

if __name__ == "__main__":

    # Define perturbation type mappings
    # English perturbation type (directory name) -> (Spanish perturbation type, English dataset file, English dataset column, Spanish dataset column)
    perturb_mappings = {
        "ortho": ("ortho_typo", "jokes_ortho_typo", "perturbed_joke_ortho_typo", "perturbed_joke_ortho_typo"),
        "sem_drift": ("semantic_drift", "jokes_semantic_drift", "perturbed_joke_semantic_drift", "perturbed_joke_semantic_drift"),
        "sem_pres": ("semantic_preserving", "jokes_semantic_preserving", "perturbed_joke_semantic_preserving", "perturbed_joke_semantic_preserving")
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

    # Base paths
    en_dataset_base = "/fs/clip-projects/rlab/atrey/humorbench/datasets/labeled/jokes_en"
    es_dataset_base = "/fs/clip-projects/rlab/atrey/humorbench/datasets/labeled/jokes_es"
    en_run_path_base = "/fs/clip-projects/rlab/atrey/humorbench/completions/perturbed"
    es_run_path_base = "/fs/clip-projects/rlab/atrey/humorbench/completions/perturbed_es"
    out_path_base = "/fs/clip-projects/rlab/atrey/humorbench/results/perturbed_combined"
    cm_save_path_base = "/fs/clip-projects/rlab/atrey/humorbench/results/perturbed_combined"

    # Process each perturbation type
    for en_perturb_type, (es_perturb_type, en_dataset_file, en_joke_col, es_joke_col) in perturb_mappings.items():
        print(f"\n{'='*80}")
        print(f"Processing combined perturbation type: {en_perturb_type} (EN) + {es_perturb_type} (ES)")
        print(f"{'='*80}\n")

        # Load English dataset
        en_dataset_path = os.path.join(en_dataset_base, f"{en_dataset_file}.tsv")
        print(f"Loading English dataset from {en_dataset_path}...")
        en_dataset = pd.read_csv(en_dataset_path, sep='\t')
        # Rename joke column to standardize
        en_dataset = en_dataset.rename(columns={en_joke_col: "Joke"})
        print(f"English dataset size: {len(en_dataset)}")

        # Load Spanish dataset
        es_dataset_path = os.path.join(es_dataset_base, f"jokes_{es_perturb_type}.tsv")
        print(f"Loading Spanish dataset from {es_dataset_path}...")
        es_dataset = pd.read_csv(es_dataset_path, sep='\t')
        # Rename joke column to standardize
        es_dataset = es_dataset.rename(columns={es_joke_col: "Joke"})
        print(f"Spanish dataset size: {len(es_dataset)}")

        # Combine datasets
        print("Combining English and Spanish datasets...")
        combined_dataset = pd.concat([en_dataset, es_dataset], ignore_index=True)
        print(f"Combined dataset size: {len(combined_dataset)} (EN: {len(en_dataset)}, ES: {len(es_dataset)})")

        # Set up output paths
        out_path = os.path.join(out_path_base, f"{en_perturb_type}/csvs/{en_perturb_type}")
        cm_save_path = os.path.join(cm_save_path_base, f"{en_perturb_type}/confusion_matrices/")

        # Create output directories
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        os.makedirs(cm_save_path, exist_ok=True)

        # Initialize results dictionaries
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
            print(f"Evaluating model: {model} for {en_perturb_type} (combined EN+ES)")

            # Create paths for both languages
            en_task1_run_path = os.path.join(en_run_path_base, f"{en_perturb_type}/{model}/{en_perturb_type}_task1_{model}")
            es_task1_run_path = os.path.join(es_run_path_base, f"{es_perturb_type}/{model}/{es_perturb_type}_task1_{model}")
            task1_run_paths = [en_task1_run_path, es_task1_run_path]
            task1_cm_save_path = os.path.join(cm_save_path, f"task1_confusion_matrix_{model}")

            en_task2_run_path = os.path.join(en_run_path_base, f"{en_perturb_type}/{model}/{en_perturb_type}_task2_{model}")
            es_task2_run_path = os.path.join(es_run_path_base, f"{es_perturb_type}/{model}/{es_perturb_type}_task2_{model}")
            task2_run_paths = [en_task2_run_path, es_task2_run_path]
            task2_cm_save_path = os.path.join(cm_save_path, f"task2_confusion_matrix_{model}")

            # Check if run files exist
            if not os.path.exists(f"{en_task1_run_path}_run1.txt") and not os.path.exists(f"{es_task1_run_path}_run1.txt"):
                print(f"Warning: Task1 run files not found for {model} (neither EN nor ES)")
                continue

            if not os.path.exists(f"{en_task2_run_path}_run1.txt") and not os.path.exists(f"{es_task2_run_path}_run1.txt"):
                print(f"Warning: Task2 run files not found for {model} (neither EN nor ES)")
                continue

            # Evaluate Task 1
            try:
                pass_at_1_task1, pass_at_5_task1 = eval_task1(
                    None,  # dataset_path not needed when passing dataset
                    None,  # run_path not needed when passing run_paths
                    task1_cm_save_path,
                    "Joke",  # Standardized column name
                    model,
                    run_paths=task1_run_paths,
                    dataset=combined_dataset
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
                import traceback
                traceback.print_exc()
                continue

            # Evaluate Task 2
            try:
                pass_at_1_task2, pass_at_5_task2 = eval_task2(
                    None,  # dataset_path not needed when passing dataset
                    None,  # run_path not needed when passing run_paths
                    task2_cm_save_path,
                    "Joke",  # Standardized column name
                    model,
                    run_paths=task2_run_paths,
                    dataset=combined_dataset
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
                import traceback
                traceback.print_exc()
                continue

        # Save results
        if task_1_results_dict['model']:
            task1_res_df = pd.DataFrame(task_1_results_dict)
            task1_res_df.to_csv(f"{out_path}_task1_res.csv", index=False)
            print(f"Saved Task1 results to {out_path}_task1_res.csv")

        if task_2_results_dict['model']:
            task2_res_df = pd.DataFrame(task_2_results_dict)
            task2_res_df.to_csv(f"{out_path}_task2_res.csv", index=False)
            print(f"Saved Task2 results to {out_path}_task2_res.csv")

    print("\n" + "="*80)
    print("Evaluation complete for all combined perturbation types!")
    print("="*80)

