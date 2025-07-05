import sys
import requests

"""
Recibe una id PDB como string. Realiza un request para mapear la id 
en UniProt y devuelve la id UniProt como string para el mismo elemento.
"""
def get_uniprot_id_from_pdb_id(pdb_id: str):
    uniprot_id_mapping_url = "https://rest.uniprot.org/idmapping/run"
    params_pdb_to_uniprot = {
        "from": "PDB",
        "to": "UniProtKB",
        "ids": pdb_id
    }

    print(f"📡 Enviando consulta para mapear PDB ID '{pdb_id}' a UniProt...")
    try:
        result = requests.post(uniprot_id_mapping_url, data=params_pdb_to_uniprot, timeout=10)
        result.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al solicitar el mapeo PDB -> UniProt: {e}")
        sys.exit()

    job_id = result.json().get('jobId')
    job_url = f"https://rest.uniprot.org/idmapping/results/{job_id}"

    print(f"⏳ Recuperando resultados de mapeo (Job ID: {job_id})...")
    try:
        job_result = requests.get(job_url, timeout=10)
        job_result.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al recuperar resultados del mapeo: {e}")
        sys.exit()

    data = job_result.json()
    id_uniprot = data.get("results")[0].get("to")

    print(f"✅ UniProt ID obtenido para PDB ID '{pdb_id}': {id_uniprot}")

    return id_uniprot

"""
Recibe una id UniProt como string. Realiza un request para mapear la id 
en ChEMBL y devuelve la id ChEMBL como string para el mismo elemento.
"""
def get_chembl_id_from_uniprot_id(uniprot_id: str):
    uniprot_id_mapping_url = "https://rest.uniprot.org/idmapping/run"
    params_uniprot_to_chembl = {
        "from": "UniProtKB_AC-ID",
        "to": "ChEMBL",
        "ids": uniprot_id
    }

    print(f"📡 Enviando consulta para mapear UniProt ID '{uniprot_id}' a ChEMBL...")
    try:
        result = requests.post(uniprot_id_mapping_url, data=params_uniprot_to_chembl, timeout=10)
        result.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al solicitar el mapeo UniProt -> ChEMBL: {e}")
        sys.exit()

    job_id = result.json().get('jobId')
    job_url = f"https://rest.uniprot.org/idmapping/results/{job_id}"

    print(f"⏳ Recuperando resultados de mapeo (Job ID: {job_id})...")
    try:
        job_result = requests.get(job_url, timeout=10)
        job_result.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al recuperar resultados del mapeo: {e}")
        sys.exit()

    data = job_result.json()
    id_chembl = data.get("results")[0].get("to")

    print(f"✅ ChEMBL ID obtenido para UniProt ID '{uniprot_id}': {id_chembl}")

    return id_chembl

def get_chembl_id_from_pdb_id(pdb_id: str):
    id_uniprot = get_uniprot_id_from_pdb_id(pdb_id)
    id_chembl = get_chembl_id_from_uniprot_id(id_uniprot)
    return id_chembl
