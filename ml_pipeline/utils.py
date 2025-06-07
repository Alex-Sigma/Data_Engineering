# ml_pipeline/utils.py
import os
import logging
import pandas as pd
from datetime import datetime

def get_logger(name: str):
    logging.basicConfig(level=logging.INFO, format='🧠 [%(levelname)s] %(message)s')
    return logging.getLogger(name)

def get_timestamp():
    return datetime.now()

def ensure_dir_exists(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def load_csv(path: str):
    return pd.read_csv(path)

def save_csv(df: pd.DataFrame, path: str):
    ensure_dir_exists(path)
    df.to_csv(path, index=False)