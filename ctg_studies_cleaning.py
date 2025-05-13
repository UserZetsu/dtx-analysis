import json
import pandas as pd

def clean_json(path): 
    # Load Json
    with open(path, 'r') as file:
        studies = json.load(file)
        
    rows = list()
    for study in studies:
        # Protocol Data
        protocol = study.get('protocolSection', {})
        
        # Identification Module
        identification = protocol.get('identificationModule', {})
        nct_id = identification.get('nctId')
        org_name = identification.get('organization', {}).get('fullName')
        org_class = identification.get('organization', {}).get('class')
        brief_title = identification.get('briefTitle')

        # Status Module
        status = protocol.get('statusModule', {})
        overall_status = status.get('overallStatus')
        why_stopped = status.get('whyStopped')

        # Sponsor/Collaborators Module
        sponsors = protocol.get('sponsorCollaboratorsModule', {})
        collaborators = sponsors.get('collaborators')

        # Oversight Module
        oversight = protocol.get('oversightModule', {})
        has_dmc = oversight.get('oversightHasDmc')
        fda_regulated_drug = oversight.get('isFdaRegulatedDrug')
        fda_regulated_device = oversight.get('isFdaRegulatedDevice')

        # Design Module
        design = protocol.get('designModule', {})
        phases = design.get('phases', [])
        phase = phases[0] if phases else None

        # Conditions Module
        conditions_module = protocol.get('conditionsModule', {})
        conditions = conditions_module.get('conditions')
        keywords = conditions_module.get('keywords')  

        rows.append({
            'nct_id': nct_id,
            'org_name': org_name,
            'org_class': org_class,
            'brief_title': brief_title,
            'overall_status': overall_status,
            'why_stopped': why_stopped,
            'collaborators': collaborators,
            'has_dmc': has_dmc,
            'fda_regulated_drug': fda_regulated_drug,
            'fda_regulated_device': fda_regulated_device,
            'phase': phase,
            'conditions': conditions,
            'keywords': keywords  
        })

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    
    return df
    
if __name__ == "__main__":
    path = 'data/ctg-studies.json'
    df = clean_json(path)
    
    # Save to CSV
    df.to_csv(f'{path[::-5]}.csv', index=False)
