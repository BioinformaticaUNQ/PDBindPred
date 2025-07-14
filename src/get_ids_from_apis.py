import sys
import requests
import json

"""
Recibe una id PDB como string. Realiza un request para mapear la id 
en UniProt y devuelve la id UniProt como string para el mismo elemento.
"""
def get_uniprot_id_from_pdb_id(pdb_id: str):
    params_pdb_to_uniprot = {
        "from": "PDB",
        "to": "UniProtKB",
        "ids": pdb_id
    }
    result = post_request_in_uniprot_idmapping(params_pdb_to_uniprot)
    data = get_result_from_uniprot_idmapping_job(result)
    id_uniprot = data.get("results")[0].get("to")

    print(f"✅ UniProt ID obtenido para PDB ID '{pdb_id}': {id_uniprot}")
    return id_uniprot


"""
Recibe una id UniProt como string. Realiza un request para mapear la id 
en ChEMBL y devuelve la id ChEMBL como string para el mismo elemento.
"""
def get_data_from_uniprot_id(uniprot_id: str):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}?fields=xref_pdb%2Cxref_chembl%2Cdate_created%2Clit_doi_id"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data

"""
Dado un diccionario de parámetros estructurado según las indicaciones de 
UniProt IdMapping ("from", "to", "ids"), envía un post request a dicho 
sitio para convertir la id indicada en los parámetros de un formato (from) 
hacia otro formato (to).
Devuelve un response con el id del job del post request.
"""
def post_request_in_uniprot_idmapping(params):
    uniprot_id_mapping_url = "https://rest.uniprot.org/idmapping/run"
    print(f"📡 Enviando consulta para mapear ID " + params["ids"] + " a UniProt...")
    try:
        result = requests.post(uniprot_id_mapping_url, data=params, timeout=10)
        result.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al solicitar el mapeo " + params["from"] + " -> " + params["to"] + ": {e}")
        sys.exit()
    return result

"""
Dado una consulta (un job) a UniProt IdMapping, hace un request en 
dicha API con el id del job para recuperar los datos de la consulta. 
Devuelve un json con los resultados. 
"""
def get_result_from_uniprot_idmapping_job(result):
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
    return data


