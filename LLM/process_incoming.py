# import pandas as pd 
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np 
# import joblib 
# import requests


# def create_embedding(text_list):
#     # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
#     r = requests.post("http://localhost:11434/api/embed", json={
#         "model": "bge-m3",
#         "input": text_list
#     })

#     embedding = r.json()["embeddings"] 
#     return embedding

# def inference(prompt):
#     r = requests.post("http://localhost:11434/api/generate", json={
#         # "model": "deepseek-r1",
#         "model": "gemma3:1b",
#         "prompt": prompt,
#         "stream": False
#     })

#     response = r.json()
#     print(response)
#     return response

# df = joblib.load('embeddings.joblib')


# incoming_query = input("Ask a Question: ")
# question_embedding = create_embedding([incoming_query])[0] 

# # Find similarities of question_embedding with other embeddings
# # print(np.vstack(df['embedding'].values))
# # print(np.vstack(df['embedding']).shape)
# similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# # print(similarities)
# top_results = 3
# max_indx = similarities.argsort()[::-1][0:top_results]
# # print(max_indx)
# new_df = df.loc[max_indx].copy()
# # print(new_df[["title", "number", "text"]])
# def format_time(seconds):
#     minutes = int(seconds // 60)
#     secs = int(seconds % 60)
#     return f"{minutes:02d}:{secs:02d}"

# new_df["start"] = new_df["start"].apply(format_time)
# new_df["end"] = new_df["end"].apply(format_time)

# prompt = f"""
# You are an AI teaching assistant for a web development course.

# You are given video transcript chunks in JSON format.

# Context:
# {new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

# ---------------------------------
# Question: "{incoming_query}"
# ---------------------------------

# Instructions:

# 1. Answer using the given context, but EXPLAIN the concept in your own words.
# 2. Keep explanation simple, clear, and human-friendly (1–2 lines).
# 3. Do NOT copy raw transcript text directly unless necessary.
# 4. Do NOT use outside knowledge beyond what is implied in the context.
# 5. If the answer is partially present, try to infer and explain briefly.

# Only say "Not found in the course content" if there is absolutely no relevant information in the context.

# 6. Convert timestamps into MM:SS format.
# 7. Search carefully across all chunks before concluding.

# ---------------------------------

# Output format (STRICT):

# <Short explanation in 1–2 lines>

# Video: <video number> (<video title>)  
# Timestamp: <MM:SS>
# """
# with open("prompt.txt", "w") as f:
#     f.write(prompt)

# response = inference(prompt)["response"]
# print(response)

# with open("response.txt", "w", encoding="utf-8") as f:
#     f.write(response)
# # for index, item in new_df.iterrows():
# #     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

# -------------------------------
# 🔹 EMBEDDING FUNCTION
# -------------------------------
def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    return r.json()["embeddings"]

# -------------------------------
# 🔹 LLM INFERENCE
# -------------------------------
def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3:latest",   # upgraded model
        "prompt": prompt,
        "stream": False
    })
    return r.json()

# -------------------------------
# 🔹 LOAD DATA
# -------------------------------
df = joblib.load('embeddings.joblib')

# -------------------------------
# 🔹 USER QUERY
# -------------------------------
incoming_query = input("Ask a Question: ")

# -------------------------------
# 🔹 CREATE QUERY EMBEDDING
# -------------------------------
question_embedding = create_embedding([incoming_query])[0]

# -------------------------------
# 🔹 SIMILARITY SEARCH
# -------------------------------
embeddings_matrix = np.vstack(df['embedding'].values)
similarities = cosine_similarity(embeddings_matrix, [question_embedding]).flatten()

# -------------------------------
# 🔹 FILTER LOW-QUALITY MATCHES
# -------------------------------
threshold = 0.55

filtered_idx = [i for i, score in enumerate(similarities) if score > threshold]

if not filtered_idx:
    print("❌ No strong match found")
    exit()

# Top-K results
top_k = 5
max_indx = sorted(filtered_idx, key=lambda i: similarities[i], reverse=True)[:top_k]

new_df = df.loc[max_indx].copy()

# -------------------------------
# 🔹 DEBUG (VERY IMPORTANT)
# -------------------------------
DEBUG = False  # change to True when needed

if DEBUG:
    print("\n🔍 Retrieved Chunks:\n")
    for i in max_indx:
        print(f"""
Video: {df.iloc[i]['number']}
Title: {df.iloc[i]['title']}
Score: {similarities[i]:.4f}
Text: {df.iloc[i]['text'][:120]}
-------------------------
""")

# -------------------------------
# 🔹 FORMAT TIMESTAMP
# -------------------------------
def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

new_df["start"] = new_df["start"].apply(format_time)
new_df["end"] = new_df["end"].apply(format_time)

# -------------------------------
# 🔹 PROMPT
# -------------------------------
prompt = f"""
You are an AI teaching assistant for a web development course.

You are given multiple video transcript chunks.

Context:
{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

----------------------------------
Question: "{incoming_query}"
---------------------------------

Instructions:

1. Read all context carefully.
2. Choose the most relevant video.
3. Ignore unrelated content.
4. Explain WHAT the concept is and WHY it is used (3–4 lines).
5. Do NOT copy raw text.
6. The explanation MUST define the concept clearly.
7. If no relevant info → "Not found in the course content"

8. Return ONLY ONE answer.
9. Never include raw context, scores, or debug info.

---------------------------------

Output (STRICT — follow exactly):

<Short explanation>

Video: <number> (<title>)
Timestamp: <MM:SS>

Do NOT include anything else.
"""

# Save prompt (optional debug)
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

# -------------------------------
# 🔹 LLM RESPONSE
# -------------------------------
response = inference(prompt)["response"]

print("\n🤖 Answer:\n")
print(response)

# Save response
with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)