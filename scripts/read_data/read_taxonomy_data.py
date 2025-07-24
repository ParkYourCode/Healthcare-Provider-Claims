import os
from pathlib import Path
import pandas as pd

def read_taxonomy_data():
    project_root = Path(__file__).parent
    input_path = project_root / 'data' / 'raw' / 'Medicare_Provider_and_Supplier_Taxonomy_Crosswalk_Jan_2025.csv'

    try:
        taxonomy_df = pd.read_csv(input_path, dtype=str)
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

