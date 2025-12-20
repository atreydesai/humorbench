import argparse
import os
import pandas as pd

<<<<<<< HEAD

def make_prompt_task1(joke: str) -> str:
    prompt = (
        'Classify the following joke into one of these types: satire, parody, irony, aggressive, '
        'dry, self-deprecating, surreal/absurdism, wordplay, witty, topical, observational, '
        'anecdotal, dark. Output valid JSON of the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END for the joke: '
        + joke
        + ' Your final answer should take the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END'
    )
    return prompt


def make_prompt_task2(joke: str) -> str:
    prompt = (
        'Here is a joke: ' + joke + ' END OF JOKE. '
        'Classify each newline-separated line of a multi-line joke by its role, assigning exactly one label from '
        'establishing context, setup, escalation, subversion, callback, misdirection, timing, meta-humor, '
        'punchline, redirection, non-line, wrap-up, repetition. '
        'Your final answer should take the form {"ANSWER":["label1", "label2",...]}### END.'
    )
    return prompt


def _choose_joke_column(df: pd.DataFrame, prefer: str | None = None) -> str:
    if prefer and prefer in df.columns:
        return prefer
    # common names
    for cand in ["Joke", "joke", "perturbed_joke", "perturbed_joke_semantic_preserving"]:
        if cand in df.columns:
            return cand
    # fallback: find first column that looks like a joke column
    for c in df.columns:
        if "joke" in c.lower():
            return c
    # otherwise use first column
    return df.columns[0]


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate prompts from a TSV of jokes")
    ap.add_argument("--input", required=True, help="Input TSV file path")
    ap.add_argument("--joke-col", default=None, help="Column name containing joke text")
    ap.add_argument("--outdir", default='.', help="Output directory for prompt files")
    ap.add_argument("--task", choices=['1','2','both'], default='both', help="Which task prompts to generate")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.input, sep='\t')
    joke_col = _choose_joke_column(df, args.joke_col)

    base = os.path.splitext(os.path.basename(args.input))[0]

    if args.task in ('1','both'):
        out_path = os.path.join(args.outdir, f'prompts_task1_{base}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            for j in df[joke_col].fillna(''):
                f.write(make_prompt_task1(str(j)) + '\n')

    if args.task in ('2','both'):
        out_path = os.path.join(args.outdir, f'prompts_task2_{base}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            for j in df[joke_col].fillna(''):
                f.write(make_prompt_task2(str(j)) + '\n')


if __name__ == '__main__':
    main()
=======
joke_key = 'Joke'

def make_prompt_task1(row):
    joke = row[joke_key]
    prompt = 'Classify the following joke in spanish into one of these types: satire, parody, irony, aggressive, dry, self-deprecating, surreal/absurdism, wordplay, witty, topical, observational, anecdotal, dark. Output valid JSON of the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END for the joke: ' + joke + 'Your final answer should take the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END If you do not output your final answer in this format, you will not receive any credit.'
    row['prompt'] = prompt
    return row

def make_prompt_task2(row):
    joke = row[joke_key]
    prompt = 'Here is a joke in spanish: ' + joke + ' END OF JOKE. Classify each newline-separated line in this multi-line joke by its role, assigning exactly one label from establishing context, setup, escalation, subversion, callback, misdirection, timing, meta-humor, punchline, redirection, non-line, wrap-up, repetition. Your final answer should take the form {"ANSWER":["label1", "label2",...]}### END. If you do not output your final answer in this format, you will not receive any credit.' 
    row['prompt'] = prompt
    return row

dataset = pd.read_csv('../../datasets/labeled/es_labelled.tsv', sep='\t')
task1 = dataset[[joke_key, 'Task1 Label']].copy().dropna()
task2 = dataset[[joke_key, 'Task2 Label']].copy().dropna()

task1_prompts = task1.apply(make_prompt_task1, axis=1)
prompts = task1_prompts['prompt']
with open('prompts_task1_es.txt', 'w') as f:
    for prompt in prompts:
        f.write(prompt + "\n")

task2_prompts = task2.apply(make_prompt_task2, axis=1)
prompts = task2_prompts['prompt']
with open('prompts_task2_es.txt', 'w') as f:
    for prompt in prompts:
        f.write(prompt + "\n")
>>>>>>> origin/main
