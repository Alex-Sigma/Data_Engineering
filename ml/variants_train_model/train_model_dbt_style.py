import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    KBinsDiscretizer, RobustScaler, MaxAbsScaler,
    MinMaxScaler, FunctionTransformer, Binarizer, StandardScaler,
    LabelEncoder, OneHotEncoder
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from itertools import combinations


def load_iris_df():
    df = pd.read_csv("data/iris_data.csv")
    return df


def engineer_features(df):
    base_vars = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    processed = pd.DataFrame()

    # Original features
    for col in base_vars:
        processed[col] = df[col]

    # Quantile and Uniform Binning
    for strategy in ["quantile", "uniform"]:
        kb = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy=strategy)
        transformed = kb.fit_transform(df[base_vars])
        for i, col in enumerate(base_vars):
            processed[f"{col}_{strategy}_bin"] = transformed[:, i]

    # Robust, MaxAbs, MinMax Scaling
    scalers = {
        "robust": RobustScaler(),
        "maxabs": MaxAbsScaler(),
        "minmax": MinMaxScaler(feature_range=(0.0, 1.0))
    }
    for name, scaler in scalers.items():
        scaled = scaler.fit_transform(df[base_vars])
        for i, col in enumerate(base_vars):
            processed[f"{col}_{name}_scaled"] = scaled[:, i]

    # Log transform
    log = FunctionTransformer(func=np.log1p)
    log_trans = log.fit_transform(df[base_vars])
    for i, col in enumerate(base_vars):
        processed[f"{col}_logged"] = log_trans[:, i]

    # Binarization (threshold by median)
    for col in base_vars:
        thresh = df[col].quantile(0.5)
        binarized = Binarizer(threshold=thresh).fit_transform(df[[col]])
        processed[f"{col}_binarized"] = binarized.flatten()

    # Standardization
    std_scaled = StandardScaler().fit_transform(df[base_vars])
    for i, col in enumerate(base_vars):
        processed[f"{col}_standardized"] = std_scaled[:, i]

    # Feature interactions (multiplicative + additive)
    for col1, col2 in combinations(base_vars, 2):
        processed[f"{col1}_x_{col2}_interaction"] = df[col1] * df[col2]
        processed[f"{col1}_plus_{col2}_interaction"] = df[col1] + df[col2]

    # Label encoding
    le = LabelEncoder()
    processed["species_label_encoded"] = le.fit_transform(df["species"])

    # One-hot encoding
    ohe = OneHotEncoder(sparse=False, drop=None)
    ohe_array = ohe.fit_transform(df[["species"]])
    ohe_df = pd.DataFrame(ohe_array, columns=[f"is_{c}" for c in ohe.categories_[0]])
    processed = pd.concat([processed, ohe_df], axis=1)

    return processed


def train_and_evaluate(df):
    X = df.drop(columns=["species_label_encoded"] + [c for c in df.columns if c.startswith("is_")])
    y = df["species_label_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    acc_train = clf.score(X_train, y_train)
    acc_test = clf.score(X_test, y_test)

    print(f"Accuracy (train): {acc_train:.4f}, Accuracy (test): {acc_test:.4f}")
    return clf


if __name__ == "__main__":
    df = load_iris_df()
    processed = engineer_features(df)
    model = train_and_evaluate(processed)
