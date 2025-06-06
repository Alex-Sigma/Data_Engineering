import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer, RobustScaler, MaxAbsScaler, MinMaxScaler, StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from itertools import combinations
import os

def generate_features_iris():
    df = pd.read_csv("data/iris_data.csv")
    
    numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    result = df[numeric_cols].copy()

    # K-bins discretization
    for strategy in ['quantile', 'uniform']:
        kbins = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy=strategy)
        result[[f"{col}_{strategy}_bin" for col in numeric_cols]] = kbins.fit_transform(df[numeric_cols])

    # Scaling
    result[[f"{col}_robust_scaled" for col in numeric_cols]] = RobustScaler().fit_transform(df[numeric_cols])
    result[[f"{col}_max_absolute_scaled" for col in numeric_cols]] = MaxAbsScaler().fit_transform(df[numeric_cols])
    result[[f"{col}_max_min_max_scaled" for col in numeric_cols]] = MinMaxScaler((0, 1)).fit_transform(df[numeric_cols])

    # Log transformation (add small constant to avoid log(0))
    log_transformer = FunctionTransformer(func=np.log1p)
    result[[f"{col}_logged" for col in numeric_cols]] = log_transformer.fit_transform(df[numeric_cols])

    # Binarization: greater than median (0.5 percentile)
    for col in numeric_cols:
        threshold = df[col].quantile(0.5)
        result[f"{col}_binarized"] = (df[col] > threshold).astype(int)

    # Standardization
    result[[f"{col}_standardized" for col in numeric_cols]] = StandardScaler().fit_transform(df[numeric_cols])

    # Interactions
    for col1, col2 in combinations(numeric_cols, 2):
        result[f"{col1}_x_{col2}_interaction"] = df[col1] * df[col2]
        result[f"{col1}_plus_{col2}_interaction"] = df[col1] + df[col2]

    # Target
    result['species'] = df['species']
    result['species_label_encoded'] = LabelEncoder().fit_transform(df['species'])

    # One-hot
    ohe = OneHotEncoder(sparse=False, drop=None)
    ohe_result = ohe.fit_transform(df[['species']])
    ohe_cols = ohe.get_feature_names_out(['species'])
    result[ohe_cols] = ohe_result

    # Сохраняем
    os.makedirs("data/db", exist_ok=True)
    result.to_csv("data/db/features_iris.csv", index=False)
    print("✅ Features saved to data/db/features_iris.csv")

if __name__ == "__main__":
    generate_features_iris()
