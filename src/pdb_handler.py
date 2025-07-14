import os
import json
from xml.etree.ElementTree import Element

import requests
import xml.etree.ElementTree as ET
from src.get_ids_from_apis import get_uniprot_id_from_pdb_id, get_data_from_uniprot_id
from src import config

def fetch_pdb_info(pdb_id):
    """Consulta a la API de RCSB PDB para obtener información básica de una estructura, incluyendo resolución, año de publicación y DOI."""
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
        "pdb_ids": [{'pdb_id': pdb_id, 'resolution': resolution}],
        "publication_year": year,
        "doi": doi,
        "uniprot_id": None,
        "chembl_id": None,
        "sources": "RCSB PDB, ChEMBL, UniProt",
        "ligands": []
    }

def get_binding_activities_for_target_from_chembl(chembl_target_id: str, affinity_types=None, ligands=None):
    """Consulta la API de ChEMBL para obtener las actividades de unión (binding) de un target dado, filtrando opcionalmente por tipos de afinidad y ligandos."""
    url = "https://www.ebi.ac.uk"
    query = f'/chembl/api/data/activity?target_chembl_id={chembl_target_id}&assay_type__exact=B'
    if ligands != None:
        query += '&molecule_chembl_id__in='
        query += ','.join(ligands)
    if affinity_types != None:
        query += '&standard_type__in='
        query += ','.join(affinity_types)
    headers = {"Accept": "application/xml"}
    print(f"📡 Enviando consulta a ChEMBL para obtener ligandos asociados a ChEMBL ID '{chembl_target_id}'...")

    activities = []
    while query is not None:
        url_query = url + query
        response = requests.get(url_query, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ No se pudo obtener datos desde ChEMBL para {chembl_target_id}")
            return []
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            print(f"⚠️ Error al parsear XML de respuesta ChEMBL: {e}")
            return []
        activities += root.findall(".//activity")
        query = root.find('.//next').text
    return activities

def get_ligands_from_chembl_target(chembl_target_id: str, affinity_types=None, ligands=None):
    """Procesa las actividades de un target de ChEMBL para agrupar información sobre los ligandos asociados, como sus afinidades, SMILES y año de publicación."""
    activities = get_binding_activities_for_target_from_chembl(chembl_target_id, affinity_types, ligands)
    ligands = []
    for activity in activities:
        ligand_id = get_ligand_id_from_activity(activity)
        canonical_smiles = get_canonical_smiles_from_activity(activity)
        value = get_affinity_value_from_activity(activity)
        type_ = get_affinity_value_type_from_activity(activity)
        value_unit = get_affinity_value_unit_from_activity(activity)
        year = get_document_year_from_activity(activity)
        assay_id = get_assay_id_from_activity(activity)

        if not ligand_id or not assay_id or not type_ or not value:
            continue  # ignoramos datos incompletos
        """
        if affinity_types and type_ not in affinity_types:
            continue"""

        ligand_assay_data = get_ligand_assay_data(assay_id, type_, value, value_unit, year)

        # Buscamos el ligando
        ligand = next((lig for lig in ligands if lig["chembl_id"] == ligand_id), None)
        if ligand is None:
            ligand = {"chembl_id": ligand_id,"canonical_smiles": canonical_smiles, "assays": [ligand_assay_data]}
            ligands.append(ligand)
        else:
            ligand["assays"].append(ligand_assay_data)

    print(f"✅ Ligandos procesados para ChEMBL ID '{chembl_target_id}': {len(ligands)} encontrados")
    return ligands


def get_ligand_assay_data(assay_id, type_, value, value_unit, year):
    """Crea un diccionario con los datos de un ensayo para un ligando, incluyendo tipo de afinidad, valor, unidad y año."""
    ligand_assay_data = {"assay id": assay_id, "publication_year": year}
    # Agregamos el tipo como propiedad dinámica
    value_type = type_
    if value_unit != None:
        value_type += " (" + value_unit + ")"
    try:
        ligand_assay_data[value_type] = float(value)
    except ValueError:
        ligand_assay_data[type_] = value  # por si no es numérico
    return ligand_assay_data


def get_ligand_id_from_activity(activity: Element):
    """Extrae el ID ChEMBL del ligando desde una actividad en formato XML."""
    chembl_id_elem = activity.find("molecule_chembl_id")
    ligand_id = chembl_id_elem.text if chembl_id_elem is not None else None
    return ligand_id

def get_canonical_smiles_from_activity(activity: Element):
    """Extrae el SMILES canónico del ligando desde una actividad en formato XML."""
    canonical_smiles_elem = activity.find("canonical_smiles")
    canonical_smiles = canonical_smiles_elem.text if canonical_smiles_elem is not None else None
    return canonical_smiles

def get_affinity_value_from_activity(activity: Element):
    """Extrae el valor de afinidad desde una actividad en formato XML."""
    value_elem = activity.find("standard_value")
    value = value_elem.text if value_elem is not None else None
    return value

def get_affinity_value_type_from_activity(activity: Element):
    """Extrae la unidad del valor de afinidad desde una actividad en formato XML (ej. nM)."""
    type_elem = activity.find("standard_type")
    type_ = type_elem.text if type_elem is not None else None
    return type_

def get_affinity_value_unit_from_activity(activity: Element):
    """Extrae la unidad del valor de afinidad desde una actividad en formato XML (ej. nM)."""
    unit_elem = activity.find("standard_units")
    unit = unit_elem.text if unit_elem is not None else None
    return unit

def get_document_year_from_activity(activity: Element):
    """Extrae el año de publicación del documento asociado a una actividad en formato XML."""
    year_elem = activity.find("document_year")
    year = year_elem.text if year_elem is not None else None
    return (year)

def get_assay_id_from_activity(activity: Element):
    """Extrae el ID del ensayo (assay) desde una actividad en formato XML."""
    assay_chembl_id_elem = activity.find("assay_chembl_id")
    assay_id = assay_chembl_id_elem.text if assay_chembl_id_elem is not None else None
    return assay_id

def process_pdb(pdb_id, affinity_types, ligands_ids):
    """Procesa una ID de PDB: obtiene información estructural, mapea a UniProt y ChEMBL, consulta ligandos asociados y guarda el resultado en un archivo JSON."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"pdb_{pdb_id}")
    if affinity_types != None:
        output_path += '_'
        output_path += ','.join(affinity_types)
    if ligands_ids != None:
        output_path += '_'
        output_path += ','.join(ligands_ids)
    output_path += '.json'

    if config.ENABLE_LOCAL_CACHE and os.path.isfile(output_path):
        print(f"📂 Resultado ya disponible localmente para PDB ID '{pdb_id}'. Se omitirá la consulta.")
        return

    result = fetch_pdb_info(pdb_id)

    try:
        print(f"🔗 Buscando IDs UniProt y ChEMBL para PDB ID '{pdb_id}'...")
        uniprot_id = get_uniprot_id_from_pdb_id(pdb_id)
        data_from_uniprot = get_data_from_uniprot_id(uniprot_id)
        id_data_from_uniprot = data_from_uniprot.get('uniProtKBCrossReferences')
        chembl_ids_data = next((id for id in id_data_from_uniprot if id['database'] == "ChEMBL"), None)
        chembl_id = chembl_ids_data.get('id')
        result["uniprot_id"] = uniprot_id
        result["chembl_id"] = chembl_id
    except Exception as e:
        print(f"⚠️ No se pudieron obtener los IDs UniProt/ChEMBL: {e}")

    ligands = []
    success = False
    if result.get("chembl_id"):
        try:
            ligands = get_ligands_from_chembl_target(result["chembl_id"], affinity_types=affinity_types, ligands = ligands_ids)
            success = True
        except Exception as e:
            print(f"⚠️ Error al obtener ligandos desde ChEMBL: {e}")

    result["ligands"] = ligands
    

    """
    # Guardar salida
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"pdb_{pdb_id}.json")
    """
    if success or ligands:
        try:
            with open(output_path, "w") as f:
                json.dump(result, f, indent=4)
            print(f"💾 Resultado guardado en {output_path}")
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"⚠️ Error al guardar el archivo {output_path}. Archivo eliminado. Detalles: {e}")
    else:
        print(f"⚠️ No se generó archivo para {pdb_id} porque no se obtuvieron datos.")

    print(f"💾 Resultado guardado en {output_path}")


def process_uniprot(uniprot_id, affinity_types, ligands_ids):
    """Procesa una ID de UniProt: obtiene mapeos a PDB y ChEMBL, consulta ligandos asociados y guarda el resultado en un archivo JSON."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"uniprot_{uniprot_id}")
    if affinity_types != None:
        output_path += '_'
        output_path += ','.join(affinity_types)
    if ligands_ids != None:
        output_path += '_'
        output_path += ','.join(ligands_ids)
    output_path += '.json'

    if config.ENABLE_LOCAL_CACHE and os.path.isfile(output_path):
        print(f"📂 Resultado ya disponible localmente para UniProt ID '{uniprot_id}'. Se omitirá la consulta.")
        return

    print(f"🔗 Procesando UniProt ID '{uniprot_id}'...")
    result = {
        "pdb_ids": [],
        "publication_year": "",
        "doi": "",
        "uniprot_id": uniprot_id,
        "chembl_id": None,
        "sources": "RCSB PDB, ChEMBL, UniProt",
        "ligands": []
    }

    try:
        data_from_uniprot = get_data_from_uniprot_id(uniprot_id)
        id_data_from_uniprot = data_from_uniprot.get('uniProtKBCrossReferences')
        chembl_ids_data = next((id for id in id_data_from_uniprot if id['database'] == "ChEMBL"), None)
        chembl_id = chembl_ids_data.get('id')
        pdb_ids_data = [id for id in id_data_from_uniprot if id['database'] == "PDB"]
        pdb_ids = []
        for pdb_data in pdb_ids_data:
            pdb = {}
            pdb['pdb_id'] = pdb_data['id']
            pdb['resolution'] =  next((properties for properties in pdb_data['properties'] if properties['key'] == "Resolution"), None)['value']
            pdb_ids.append(pdb)
        result["chembl_id"] = chembl_id
        result["pdb_ids"] = pdb_ids

        year_data_from_uniprot = data_from_uniprot.get('entryAudit')
        result["publication_year"] = year_data_from_uniprot["firstPublicDate"]

        pub_data_from_uniprot = data_from_uniprot.get('references')[0]["citation"]
        pub_doi_from_uniprot = next((cites for cites in pub_data_from_uniprot["citationCrossReferences"] if cites['database'] == "DOI"), None)['id']
        result["doi"] = pub_doi_from_uniprot
    except Exception as e:
        print(f"⚠️ No se pudo obtener el ID ChEMBL: {e}")

    ligands = []
    success = False

    if result.get("chembl_id"):
        try:
            ligands = get_ligands_from_chembl_target(result["chembl_id"], affinity_types=affinity_types, ligands=ligands_ids)
            success = True
        except Exception as e:
            print(f"⚠️ Error al obtener ligandos desde ChEMBL: {e}")

    result["ligands"] = ligands
    """
    # Guardar salida
    package_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(package_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"uniprot_{uniprot_id}.json")
    """
    if success or ligands:
        try:
            with open(output_path, "w") as f:
                json.dump(result, f, indent=4)
            print(f"💾 Resultado guardado en {output_path}")
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"⚠️ Error al guardar el archivo {output_path}. Archivo eliminado. Detalles: {e}")
    else:
        print(f"⚠️ No se generó archivo para {pdb_id} porque no se obtuvieron datos.")

    print(f"💾 Resultado guardado en {output_path}")
