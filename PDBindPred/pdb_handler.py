import os
import json
import requests
import xml.etree.ElementTree as ET
from PDBindPred.get_ids import get_uniprot_id_from_pdb_id, get_chembl_id_from_uniprot_id
from PDBindPred import config

def fetch_pdb_info(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    print(f"📡 Enviando consulta a RCSB PDB para obtener datos de PDB ID '{pdb_id}'...")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"❌ Error al obtener datos para PDB ID '{pdb_id}': código {response.status_code}")
    
    data = response.json()
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0]
    year = data.get("rcsb_accession_info", {}).get("initial_release_date", "")[:4]
    doi = data.get("rcsb_primary_citation", {}).get("pdbx_database_id_doi")

    print(f"✅ Datos básicos obtenidos para PDB ID '{pdb_id}'")
    return {
        "pdb_id": pdb_id,
        "resolution": resolution,
        "publication_year": year,
        "doi": doi,
        "ligands": [],
        "source": "RCSB PDB"
    }

def get_ligands_from_chembl_target(chembl_target_id: str, affinity_types=None):
    url = f"https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id={chembl_target_id}&assay_type__exact=B&limit=100"
    headers = {"Accept": "application/xml"}
    print(f"📡 Enviando consulta a ChEMBL para obtener ligandos asociados a ChEMBL ID '{chembl_target_id}'...")
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"⚠️ No se pudo obtener datos desde ChEMBL para {chembl_target_id}")
        return []

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"⚠️ Error al parsear XML de respuesta ChEMBL: {e}")
        return []

    ligands = []
    for activity in root.findall(".//activity"):
        chembl_id_elem = activity.find("molecule_chembl_id")
        value_elem = activity.find("standard_value")
        type_elem = activity.find("standard_type")
        year_elem = activity.find("document_year")
        assay_chembl_id_elem = activity.find("assay_chembl_id")

        ligand_id = chembl_id_elem.text if chembl_id_elem is not None else None
        value = value_elem.text if value_elem is not None else None
        type_ = type_elem.text if type_elem is not None else None
        year = year_elem.text if year_elem is not None else None
        assay_id = assay_chembl_id_elem.text if assay_chembl_id_elem is not None else None

        if not ligand_id or not assay_id or not type_ or not value:
            continue  # ignoramos datos incompletos

        if affinity_types and type_ not in affinity_types:
            continue

        # Buscamos el ligando
        ligand = next((lig for lig in ligands if lig["chembl_id"] == ligand_id), None)
        if ligand is None:
            ligand = {"chembl_id": ligand_id, "assays": []}
            ligands.append(ligand)

        # Buscamos el assay dentro del ligando
        assay = next((assay for assay in ligand["assays"] if assay["assay id"] == assay_id), None)
        if assay is None:
            assay = {"assay id": assay_id, "publication_year": year}
            ligand["assays"].append(assay)

        # Agregamos el tipo como propiedad dinámica
        try:
            assay[type_] = float(value)
        except ValueError:
            assay[type_] = value  # por si no es numérico

    print(f"✅ Ligandos procesados para ChEMBL ID '{chembl_target_id}': {len(ligands)} encontrados")
    return ligands


def process_pdb(pdb_id, affinity_types):

    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"pdb_{pdb_id}.json")

    if config.ENABLE_LOCAL_CACHE and os.path.isfile(output_path):
        print(f"📂 Resultado ya disponible localmente para PDB ID '{pdb_id}'. Se omitirá la consulta.")
        return

    result = fetch_pdb_info(pdb_id)

    try:
        print(f"🔗 Buscando IDs UniProt y ChEMBL para PDB ID '{pdb_id}'...")
        uniprot_id = get_uniprot_id_from_pdb_id(pdb_id)
        chembl_id = get_chembl_id_from_uniprot_id(uniprot_id)
        result["uniprot_id"] = uniprot_id
        result["chembl_id"] = chembl_id
    except Exception as e:
        print(f"⚠️ No se pudieron obtener los IDs UniProt/ChEMBL: {e}")
        result["uniprot_id"] = None
        result["chembl_id"] = None

    ligands = []
    if result.get("chembl_id"):
        try:
            ligands = get_ligands_from_chembl_target(result["chembl_id"], affinity_types=affinity_types)
        except Exception as e:
            print(f"⚠️ Error al obtener ligandos desde ChEMBL: {e}")

    result["ligands"] = ligands

    # Guardar salida
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"pdb_{pdb_id}.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"💾 Resultado guardado en {output_path}")


def process_uniprot(uniprot_id, affinity_types):
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"uniprot_{uniprot_id}.json")

    if config.ENABLE_LOCAL_CACHE and os.path.isfile(output_path):
        print(f"📂 Resultado ya disponible localmente para UniProt ID '{uniprot_id}'. Se omitirá la consulta.")
        return

    print(f"🔗 Procesando UniProt ID '{uniprot_id}'...")
    result = {
        "uniprot_id": uniprot_id,
        "ligands": [],
    }

    try:
        chembl_id = get_chembl_id_from_uniprot_id(uniprot_id)
        result["chembl_id"] = chembl_id
    except Exception as e:
        print(f"⚠️ No se pudo obtener el ID ChEMBL: {e}")
        result["chembl_id"] = None

    ligands = []
    if result.get("chembl_id"):
        try:
            ligands = get_ligands_from_chembl_target(result["chembl_id"], affinity_types=affinity_types)
        except Exception as e:
            print(f"⚠️ Error al obtener ligandos desde ChEMBL: {e}")

    result["ligands"] = ligands

    # Guardar salida
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"uniprot_{uniprot_id}.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"💾 Resultado guardado en {output_path}")
