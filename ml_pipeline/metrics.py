# ml_pipeline/metrics.py
from .utils import save_csv, get_timestamp
import pandas as pd

def save_metrics(model_results: dict, output_path: str):
    df = pd.DataFrame({
        'model_type': ['full_model', 'top5_model'],
        'train_accuracy': [model_results['train_full'], model_results['train_top5']],
        'test_accuracy': [model_results['test_full'], model_results['test_top5']],
        'features_count': [model_results['n_full'], model_results['n_top5']],
        'run_timestamp': [get_timestamp(), get_timestamp()]
    })
    save_csv(df, output_path)

def save_feature_importance(importance_df: pd.DataFrame, output_path: str):
    importance_df['run_timestamp'] = get_timestamp()
    save_csv(importance_df, output_path)