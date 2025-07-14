import os


def get_pdb_ids_from_arguments(args):
    "Extrae las PDB id introducidas en una consulta y devuelve una lista con las mismas."
    pdb_ids = []
    if args.pdb:
        pdb_ids += [p.strip() for p in args.pdb.split(",") if p.strip()]
    if args.pdb_file:
        pdb_ids += cargar_ids_desde_archivo(args.pdb_file, "PDB")
    pdb_ids = validar_pdb_ids(pdb_ids)
    return pdb_ids


def get_uniprot_ids_from_arguments(args):
    """
    Extrae y valida los IDs UniProt desde los argumentos proporcionados (por línea de comandos o archivo).
    Devuelve una lista de IDs UniProt válidos, en mayúsculas y sin repeticiones.
    """
    uniprot_ids = []
    if args.uniprot:
        uniprot_ids += [u.strip() for u in args.uniprot.split(",") if u.strip()]
    if args.uniprot_file:
        uniprot_ids += cargar_ids_desde_archivo(args.uniprot_file, "UniProt")
    uniprot_ids = validar_uniprot_ids(uniprot_ids)
    return uniprot_ids

def get_ligands_from_arguments(args):
    """
    Extrae los IDs de ligandos desde los argumentos proporcionados (por línea de comandos o archivo).
    Devuelve una lista de IDs de ligandos en el formato original.
    """
    ligands = []
    if args.lig:
        ligands += [u.strip() for u in args.lig.split(",") if u.strip()]
    if args.lig_file:
        ligands += cargar_ids_desde_archivo(args.lig_file, "Ligands")
    return ligands

def cargar_ids_desde_archivo(filepath, descripcion):
    """
    Carga una lista de IDs desde un archivo de texto (uno por línea).
    Lanza FileNotFoundError si el archivo no existe.
    Devuelve una lista de strings sin líneas vacías.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe ({descripcion})")
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]


def validar_pdb_ids(ids):
    """
    Filtra y normaliza una lista de posibles IDs PDB, descartando los que no cumplen
    con el formato (4 caracteres alfanuméricos).
    Devuelve una lista única en mayúsculas con los IDs válidos.
    """
    valid = []
    for pdb_id in ids:
        if len(pdb_id) == 4 and pdb_id.isalnum():
            valid.append(pdb_id.upper())
        else:
            print(f"⚠️ ID PDB inválido: {pdb_id} (se ignorará)")
    return list(set(valid))


def validar_uniprot_ids(ids):
    """
    Filtra y normaliza una lista de posibles IDs UniProt, descartando los que no cumplen
    con el formato esperado (6 a 10 caracteres alfanuméricos).
    Devuelve una lista única en mayúsculas con los IDs válidos.
    """
    valid = []
    for uniprot_id in ids:
        if (6 <= len(uniprot_id) <= 10) and all(c.isalnum() for c in uniprot_id):
            valid.append(uniprot_id.upper())
        else:
            print(f"⚠️ ID UniProt inválido: {uniprot_id} (se ignorará)")
    return list(set(valid))
