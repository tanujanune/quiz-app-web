# utils.py
import json
import random
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.csv")

def load_questions(filename="questions.json"):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_questions(questions, num_questions=5):
    """
    Pick random num_questions from questions list.
    """
    return random.sample(questions, num_questions)  # random.sample ensures no repeats in selection

def save_result(name, email, score, total, details=None):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "email": email,
        "score": score,
        "total": total,
        "details": json.dumps(details, ensure_ascii=False) if details else ""
    }
    df_row = pd.DataFrame([row])
    if not os.path.exists(RESULTS_FILE):
        df_row.to_csv(RESULTS_FILE, index=False)
    else:
        df_row.to_csv(RESULTS_FILE, mode="a", header=False, index=False)
