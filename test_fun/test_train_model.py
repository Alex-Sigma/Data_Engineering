# test_train_model.py
import os
from ml.train_model import train_model_from_features

def main():
    print("🧠 Training model using generated features...")
    train_model_from_features()

    metrics_path = "data/db/iris_model_metrics.csv"
    importance_path = "data/db/iris_feature_importance.csv"

    if os.path.exists(metrics_path):
        print(f"✅ Metrics saved to {metrics_path}")
        import pandas as pd
        df = pd.read_csv(metrics_path)
        print("📈 Model Metrics Preview:")
        print(df.head())
    else:
        print("❌ Model metrics file not found.")

    if os.path.exists(importance_path):
        print(f"✅ Feature importances saved to {importance_path}")
        import pandas as pd
        df = pd.read_csv(importance_path)
        print("📊 Feature Importance Preview:")
        print(df.head())
    else:
        print("❌ Feature importance file not found.")

if __name__ == "__main__":
    main()
