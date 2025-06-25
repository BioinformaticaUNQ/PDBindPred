import argparse
import requests
import json
import os

def fetch_pdb_info(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error al obtener datos para {pdb_id}")
    
    data = response.json()
    
    # Extraer campos básicos
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0]
    year = data.get("rcsb_accession_info", {}).get("initial_release_date", "")[:4]
    ligand_info = [chem["chem_comp_id"] for chem in data.get("rcsb_nonpolymer_instance_feature_summary", [])]
    
    return {
        "pdb_id": pdb_id,
        "resolution": resolution,
        "year": year,
        "ligands": ligand_info,
        "source": "RCSB PDB"
    }

def main():
    parser = argparse.ArgumentParser(description="PDBindPred - Anotación básica de estructuras PDB")
    parser.add_argument("--pdb", required=True, help="ID de entrada PDB (ej: 6IK4)")
    args = parser.parse_args()

    result = fetch_pdb_info(args.pdb)

    os.makedirs("output", exist_ok=True)
    output_path = f"output/output_{args.pdb}.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)
    
    print(f"✅ Datos descargados para PDB ID {args.pdb}")
    print(f"💾 Resultado guardado en {output_path}")

if __name__ == "__main__":
    main()