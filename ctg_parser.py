import json
import pandas as pd
import os

def clean_json(path, save_path=None):
    """
    Load and clean a ClinicalTrials.gov JSON export and return a structured DataFrame.
    
    Parameters:
        path (str): Path to the input JSON file.
        save_path (str or None): If provided, saves the DataFrame to this CSV path.
    
    Returns:
        pd.DataFrame: Cleaned trial data.
    """
    with open(path, 'r') as file:
        studies = json.load(file)

    rows = []
    for study in studies:
        protocol = study.get('protocolSection', {})
        identification = protocol.get('identificationModule', {})
        status = protocol.get('statusModule', {})
        sponsors = protocol.get('sponsorCollaboratorsModule', {})
        oversight = protocol.get('oversightModule', {})
        design = protocol.get('designModule', {})
        conditions_module = protocol.get('conditionsModule', {})

        rows.append({
            'nct_id': identification.get('nctId'),
            'org_name': identification.get('organization', {}).get('fullName'),
            'org_class': identification.get('organization', {}).get('class'),
            'brief_title': identification.get('briefTitle'),
            'overall_status': status.get('overallStatus'),
            'why_stopped': status.get('whyStopped'),
            'collaborators': sponsors.get('collaborators'),
            'has_dmc': oversight.get('oversightHasDmc'),
            'fda_regulated_drug': oversight.get('isFdaRegulatedDrug'),
            'fda_regulated_device': oversight.get('isFdaRegulatedDevice'),
            'phase': design.get('phases', [None])[0],
            'conditions': conditions_module.get('conditions'),
            'keywords': conditions_module.get('keywords')
        })

    df = pd.DataFrame(rows)

    # Save to CSV if requested
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Saved CSV to {save_path}")

    return df
