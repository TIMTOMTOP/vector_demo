#%%
from datasets import load_dataset
import json

ds_text_corpus = load_dataset("rag-datasets/rag-mini-wikipedia", "text-corpus")
ds_question_answer = load_dataset("rag-datasets/rag-mini-wikipedia", "question-answer")

passages_data = []
for i, passage in enumerate(ds_text_corpus['passages']):
    passages_data.append({
        'id': i,
        'text': passage['passage']
    })

with open('passages.json', 'w') as f:
    json.dump(passages_data, f, indent=2)


question_answer_data = []
for i, question_answer in enumerate(ds_question_answer['test']):
    question_answer_data.append({
        'id': i,
        'question': question_answer['question'],
        'answer': question_answer['answer']
    })
with open('question_answer.json', 'w') as f:
    json.dump(question_answer_data, f, indent=2)

# %%
import json

# Read the text file
with open('cat_Qs.txt', 'r') as file:
    lines = file.readlines()

# Initialize a list to hold the question-answer pairs
qa_pairs = []

# Iterate over the lines and extract question-answer pairs
for i in range(0, len(lines), 2):
    question = lines[i].strip().replace('Q: ', '')
    answer = lines[i+1].strip().replace('A: ', '')
    qa_pairs.append({'question': question, 'answer': answer})

# Write the list to a JSON file
with open('cat_Qs.json', 'w') as json_file:
    json.dump(qa_pairs, json_file, indent=4)

print("Conversion complete! The JSON file has been created.")
# %%
