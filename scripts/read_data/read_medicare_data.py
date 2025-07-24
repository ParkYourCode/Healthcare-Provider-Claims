import os
from pathlib import Path
import pandas as pd

def read_medicare_data() -> pd.DataFrame:
    """Reads medicare data and performs basic cleaning"""
    project_root = Path(__file__).parent.parent.parent
    filename = 'medicare_data.csv'
    input_path = project_root / 'data' / 'raw' / filename
    pickle_path = project_root / 'data' / 'cache' / filename

    col_names = [
        "Rndrng_NPI",
        "Rndrng_Prvdr_Last_Org_Name",
        "Rndrng_Prvdr_First_Name",
        "Rndrng_Prvdr_State_Abrvtn",
        "Rndrng_Prvdr_Ent_Cd",
        "Place_Of_Srvc",
        "HCPCS_Cd",
        "Tot_Srvcs"
    ]

    try:
        if os.path.exists(pickle_path):
            medicare_df = pd.read_pickle(pickle_path)
        else:
            medicare_df = pd.read_csv(input_path, usecols=col_names, dtype=str)
            os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
            medicare_df.to_pickle(pickle_path)

        # save sample medicare data
        sample_path = "../../data/sample/sample_medicare_data.csv"
        if not os.path.exists(sample_path):
            sample_medicare_df = medicare_df.sample(n=100)
            os.makedirs(os.path.dirname(sample_path), exist_ok=True)
            sample_medicare_df.to_csv(sample_path)

        # drop duplicate npi rows
        medicare_df.drop_duplicates(subset="Rndrng_NPI")

        # rename columns
        medicare_df = medicare_df.rename(
            columns={
                "Rndrng_NPI": "npi",
                "Rndrng_Prvdr_Last_Org_Name": "provider_last_org_name",
                "Rndrng_Prvdr_First_Name": "provider_first_name",
                "Rndrng_Prvdr_State_Abrvtn": "provider_state",
                "Rndrng_Prvdr_Ent_Cd": "provider_type",
                "Place_Of_Srvc": "place_of_service",
                "HCPCS_Cd": "hcpcs_code",
                "Tot_Srvcs": "total_claim_count"
            }
        )

        return medicare_df
    except FileNotFoundError:
        raise FileNotFoundError(f"File {input_path} not found.")
def main():
    read_medicare_data()

if __name__ == '__main__':
    main()

