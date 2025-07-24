import os
from pathlib import Path

import numpy as np
import pandas as pd

def read_nppes_data() -> pd.DataFrame:
    """Reads public NPPES data and performs basic cleaning"""
    project_root = Path(__file__).parent.parent.parent
    filename = 'nppes_data.csv'
    input_path = project_root / 'data' / 'raw' / filename
    pickle_path = project_root / 'data' / 'cache' / filename

    col_names = [
        "NPI",
        "Entity Type Code",
        "Provider Business Practice Location Address State Name",
        "Provider Enumeration Date",
        "NPI Deactivation Date",
        "Is Sole Proprietor"
    ]

    taxonomy_switch_cols = [f'Healthcare Provider Primary Taxonomy Switch_{i}' for i in range(1, 16)]
    taxonomy_code_cols = [f'Healthcare Provider Taxonomy Code_{i}' for i in range(1, 16)]
    taxonomy_cols = taxonomy_code_cols + taxonomy_switch_cols
    try:
        if os.path.exists(pickle_path):
            nppes_df = pd.read_pickle(pickle_path)
        else:
            nppes_df = pd.read_csv(input_path, usecols=col_names+taxonomy_cols, dtype=str)
            os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
            nppes_df.to_pickle(pickle_path)

        # save sample nppes data
        sample_path = "../../data/sample/sample_nppes_data.csv"
        if not os.path.exists(sample_path):
            sample_nppes_df = nppes_df.sample(n=100)
            os.makedirs(os.path.dirname(sample_path), exist_ok=True)
            sample_nppes_df.to_csv(sample_path)

        # drop empty taxonomies
        nppes_df = nppes_df[nppes_df[taxonomy_cols].notna().any(axis=1)]

        # rename columns
        nppes_df = nppes_df.rename(
            columns={
                "NPI": "npi",
                "Entity Type Code": "entity_type_code",
                "Provider Business Practice Location Address State Name": "provider_business_practice_location",
                "Provider Enumeration Date": "provider_enumeration_date",
                "NPI Deactivation Date": "npi_deactivation_date",
                "Is Sole Proprietor": "is_sole_proprietor"
            }
        )

        primary_taxonomy = np.full(len(nppes_df), None, dtype=object)

        # Iterate through the 15 column pairs
        for i in range(1, 16):
            switch_col = f'Healthcare Provider Primary Taxonomy Switch_{i}'
            code_col = f'Healthcare Provider Taxonomy Code_{i}'

            is_primary = (nppes_df[switch_col] == 'Y') & pd.isna(primary_taxonomy)
            primary_taxonomy[is_primary] = nppes_df.loc[is_primary, code_col]

        nppes_df['primary_taxonomy_code'] = primary_taxonomy

        # keep Primary Taxonomy only
        nppes_df = nppes_df.drop(taxonomy_cols, axis=1)

        return nppes_df
    except FileNotFoundError:
        raise FileNotFoundError(f"File {input_path} not found.")
def main():
    read_nppes_data()

if __name__ == '__main__':
    main()

