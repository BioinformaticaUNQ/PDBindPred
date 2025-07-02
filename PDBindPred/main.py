import argparse
import requests
import json
import os
import xml.etree.ElementTree as ET
from PDBindPred.get_ids import get_uniprot_id_from_pdb_id, get_chembl_id_from_uniprot_id


def fetch_pdb_info(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error al obtener datos para {pdb_id}")
    
    data = response.json()
    
    # Extraer campos básicos
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0]
    year = data.get("rcsb_accession_info", {}).get("initial_release_date", "")[:4]
    
    return {
        "pdb_id": pdb_id,
        "resolution": resolution,
        "year": year,
        "ligands": [],
        "source": "RCSB PDB"
    }

def get_ligands_from_chembl_target(chembl_target_id: str, affinity_types=None):
    url = f"https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id={chembl_target_id}&assay_type__exact=B&limit=100"
    headers = {"Accept": "application/xml"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"⚠️ No se pudo obtener datos desde ChEMBL para {chembl_target_id}")
        return []

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"⚠️ Error al parsear XML: {e}")
        return []

    ligands = []
    for activity in root.findall(".//activity"):
        chembl_id_elem = activity.find("molecule_chembl_id")
        value_elem = activity.find("standard_value")
        unit_elem = activity.find("standard_units")
        type_elem = activity.find("standard_type")
        year_elem = activity.find("document_year")

        ligand_id = chembl_id_elem.text if chembl_id_elem is not None else None
        value = value_elem.text if value_elem is not None else None
        unit = unit_elem.text if unit_elem is not None else None
        type_ = type_elem.text if type_elem is not None else None
        year = year_elem.text if year_elem is not None else None

        if ligand_id:
            if affinity_types and type_ not in affinity_types:
                continue
            ligands.append({
                "chembl_id": ligand_id,
                "type": type_,
                "value": value,
                "unit": unit,
                "year": year
            })

    return ligands

def main():
    parser = argparse.ArgumentParser(description="PDBindPred - Anotación básica de estructuras PDB")
    parser.add_argument("--pdb", required=True, help="ID de entrada PDB (ej: 6IK4)")
    parser.add_argument("--aff", help="Tipos de afinidad a incluir (ej: Ki,Kd,IC50)")
    args = parser.parse_args()

    result = fetch_pdb_info(args.pdb)

    # 🔽 Agregamos ID de UniProt y ChEMBL al resultado
    chembl_id = None  # 🔧 Agregado para evitar error si el try falla
    try:
        uniprot_id = get_uniprot_id_from_pdb_id(args.pdb)
        chembl_id = get_chembl_id_from_uniprot_id(uniprot_id)
        result["uniprot_id"] = uniprot_id
        result["chembl_id"] = chembl_id
    except Exception as e:
        print(f"⚠️  No se pudieron obtener los IDs UniProt/ChEMBL: {e}")
        result["uniprot_id"] = None
        result["chembl_id"] = None

    ligands = []
    if chembl_id:
        try:
            affinity_types = args.aff.split(",") if args.aff else None
            ligands = get_ligands_from_chembl_target(chembl_id, affinity_types=affinity_types)
        except Exception as e:
            print(f"⚠️  Error al obtener ligandos desde ChEMBL: {e}")

    # 👇 Agregamos al resultado antes de guardarlo
    result["ligands"] = ligands

    os.makedirs("output", exist_ok=True)
    output_path = f"output/output_{args.pdb}.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"✅ Datos descargados para PDB ID {args.pdb}")
    print(f"💾 Resultado guardado en {output_path}")



if __name__ == "__main__":
    main()