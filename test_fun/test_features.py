# test_features.py
import os
from prc.features_generator import generate_features_iris

def main():
    print("📊 Generating features for iris dataset...")
    generate_features_iris()

    output_file = "data/db/features_iris.csv"
    if os.path.exists(output_file):
        print(f"✅ Features file successfully created at: {output_file}")
        print("📄 Preview:")
        import pandas as pd
        df = pd.read_csv(output_file)
        print(df.head())
    else:
        print("❌ Failed to create features file.")

if __name__ == "__main__":
    main()
