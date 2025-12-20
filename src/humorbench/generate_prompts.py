import pandas as pd

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
