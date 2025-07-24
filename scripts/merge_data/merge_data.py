import pandas as pd
from scripts.read_data.read_medicare_data import read_medicare_data
from scripts.read_data.read_nppes_data import read_nppes_data
from scripts.read_data.read_taxonomy_data import read_taxonomy_data

def create_taxonomy_lookup(taxonomy_data):
    """Create a dictionary lookup for taxonomy codes to descriptions"""
    taxonomy_lookup = {}
    for record in taxonomy_data:
        taxonomy_lookup[record['taxonomy_code']] = record['description']
    return taxonomy_lookup

def determine_enrollment_status(row):
    if row['has_active_npi'] and row['has_recent_claims'] and row['has_consistent_info']:
        return 'Likely Enrolled'
    elif row['has_active_npi'] and row['has_recent_claims']:
        return 'Possibly Enrolled'
    elif row['has_active_npi']:
        return 'NPI Valid - Enrollment Unknown'
    else:
        return 'Not Enrolled'

def process_merged_data(merged_df, taxonomy_lookup):
    """Clean merged data and add business logic flags for Excel analysis"""
    # convert to numeric
    merged_df['total_claim_count'] = pd.to_numeric(merged_df['total_claim_count'], errors='coerce').fillna(0)

    # convert to datetime
    merged_df['provider_enumeration_date'] = pd.to_datetime(merged_df['provider_enumeration_date'], errors='coerce')
    merged_df['npi_deactivation_date'] = pd.to_datetime(merged_df['npi_deactivation_date'], errors='coerce')

    # create business logic flags

    # enrollment status
    # 3 proxies: has_active_npi, has_recent_claims, and has_consistent_info
    merged_df['has_active_npi'] = (
            merged_df['provider_enumeration_date'].notna() &
            merged_df['npi_deactivation_date'].isna()
    )

    merged_df['has_recent_claims'] = merged_df['total_claim_count'] > 0

    merged_df['has_consistent_info'] = (
            merged_df['provider_business_practice_location'].notna() &
            merged_df['primary_taxonomy_code'].notna()
    )

    merged_df['enrollment_status'] = merged_df.apply(determine_enrollment_status, axis=1)

def merge_medicare_and_nppes_data():
    medicare_df = read_medicare_data()
    nppes_df = read_nppes_data()
    taxonomy_map = read_taxonomy_data()


    merged = medicare_df.merge(nppes_df, how='left', on='npi')

    print(merged.dtypes)

def main():
    merge_medicare_and_nppes_data()

if __name__ == '__main__':
    main()