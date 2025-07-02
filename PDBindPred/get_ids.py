import sys
import requests

"""
Recibe una id PDB como string. Realiza un request para mapear la id 
en Uniprot y devuelve la id Uniprot como string para el mismo elemento.
"""
def get_uniprot_id_from_pdb_id(pdb_id : str):
    uniprot_id_mapping_url = "https://rest.uniprot.org/idmapping/run"
    params_pdb_to_uniprot = {
        "from": "PDB",
        "to": "UniProtKB",
        "ids": pdb_id
    }
    result_from_uniprot_id_mapping = requests.post(uniprot_id_mapping_url, data=params_pdb_to_uniprot)
    pdb_to_uniprot_job_id = result_from_uniprot_id_mapping.json().get('jobId')
    pdb_to_uniprot_job_url = "https://rest.uniprot.org/idmapping/results/" + pdb_to_uniprot_job_id

    pdb_to_uniprot_job = requests.get(pdb_to_uniprot_job_url)
    if not pdb_to_uniprot_job.ok:
        pdb_to_uniprot_job.raise_for_status()
        sys.exit()

    pdb_to_uniprot_data = pdb_to_uniprot_job.json()
    id_uniprot = pdb_to_uniprot_data.get("results")[0].get("to")

    return(id_uniprot)

"""
Recibe una id Uniprot como string. Realiza un request para mapear la id 
en Uniprot y devuelve la id ChEMBL como string para el mismo elemento.
"""
def get_chembl_id_from_uniprot_id(uniprot_id : str):
    uniprot_id_mapping_url = "https://rest.uniprot.org/idmapping/run"
    params_uniprot_to_chembl = {
        "from": "UniProtKB_AC-ID",
        "to": "ChEMBL",
        "ids": uniprot_id
    }
    result_from_uniprot_id_mapping = requests.post(uniprot_id_mapping_url, data=params_uniprot_to_chembl)
    uniprot_to_chembl_job_id = result_from_uniprot_id_mapping.json().get('jobId')
    uniprot_to_chembl_job_url = "https://rest.uniprot.org/idmapping/results/" + uniprot_to_chembl_job_id

    uniprot_to_chembl_job = requests.get(uniprot_to_chembl_job_url)
    if not uniprot_to_chembl_job.ok:
        uniprot_to_chembl_job.raise_for_status()
        sys.exit()

    uniprot_to_chembl_data = uniprot_to_chembl_job.json()
    id_chembl = uniprot_to_chembl_data.get("results")[0].get("to")

    return(id_chembl)


def get_chembl_id_from_pdb_id(pdb_id : str):
    id_uniprot = get_uniprot_id_from_pdb_id(pdb_id)
    id_chembl = get_chembl_id_from_uniprot_id(id_uniprot)
    return id_chembl
