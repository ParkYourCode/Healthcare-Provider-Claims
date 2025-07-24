import os
from pathlib import Path
import pandas as pd

def read_taxonomy_data():
    project_root = Path(__file__).parent.parent.parent
    filename = 'taxonomy_data.csv'
    input_path = project_root / 'data' / 'raw' / filename
    pickle_path = project_root / 'data' / 'cache' / filename

    try:
        if os.path.exists(pickle_path):
            taxonomy_df = pd.read_pickle(pickle_path)
        else:
            taxonomy_df = pd.read_csv(input_path, dtype=str)
            taxonomy_df.to_pickle(pickle_path)

        # save sample taxonomy data
        sample_path = "../../data/sample/sample_taxonomy_data.csv"
        if not os.path.exists(sample_path):
            sample_taxonomy_df = taxonomy_df.sample(n=100)
            os.makedirs(os.path.dirname(sample_path), exist_ok=True)
            sample_taxonomy_df.to_csv(sample_path)

        taxonomy_df = taxonomy_df.drop(["MEDICARE SPECIALTY CODE","MEDICARE PROVIDER/SUPPLIER TYPE DESCRIPTION"], axis=1)

        taxonomy_df = taxonomy_df.rename(
            columns={
                "PROVIDER TAXONOMY CODE": "taxonomy_code",
                "PROVIDER TAXONOMY DESCRIPTION:  TYPE, CLASSIFICATION, SPECIALIZATION": "description"
            }
        )

        return taxonomy_df.to_dict(orient='records')
    except FileNotFoundError:
        raise FileNotFoundError(f"File {input_path} not found.")

def main():
    read_taxonomy_data()

if __name__ == '__main__':
    main()

