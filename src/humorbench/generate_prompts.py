import pandas as pd

def make_prompt_task1(row):
    joke = row['Joke']
    prompt = 'Classify the following joke into one of these types: satire, parody, irony, aggressive, dry, self-deprecating, surreal/absurdism, wordplay, witty, topical, observational, anecdotal, dark. Output valid JSON of the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END for the joke: ' + joke + 'Your final answer should take the form {"category": "<one type>", "reasoning": "<1–2 sentence explanation>"}### END If you do not output your final answer in this format, you will not receive any credit.'
    row['prompt'] = prompt
    return row

def make_prompt_task2(row):
    joke = row['Joke']
    prompt = 'Here is a joke: ' + joke + ' END OF JOKE. Classify each newline-separated line of a multi-line joke by its role, assigning exactly one label from establishing context, setup, escalation, subversion, callback, misdirection, timing, meta-humor, punchline, redirection, non-line, wrap-up, repetition. Your final answer should take the form {"ANSWER":["label1", "label2",...]}### END. If you do not output your final answer in this format, you will not receive any credit.' 
    row['prompt'] = prompt
    return row

dataset = pd.read_csv('../../datasets/labeled/a-e labels.tsv', sep='\t')
task1 = dataset[['Joke', 'Task1 Label']].copy()
task2 = dataset[['Joke', 'Task2 Label']].copy().dropna()

task1_prompts = task1.apply(make_prompt_task1, axis=1)
prompts = task1_prompts['prompt']
with open('prompts_task1.txt', 'w') as f:
    for prompt in prompts:
        f.write(prompt + "\n")

task2_prompts = task2.apply(make_prompt_task2, axis=1)
prompts = task2_prompts['prompt']
with open('prompts_task2.txt', 'w') as f:
    for prompt in prompts:
        f.write(prompt + "\n")
