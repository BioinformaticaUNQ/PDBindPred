import os


"Extrae las PDB id introducidas en una consulta y devuelve una lista con las mismas."
def get_pdb_ids_from_arguments(args):
    pdb_ids = []
    if args.pdb:
        pdb_ids += [p.strip() for p in args.pdb.split(",") if p.strip()]
    if args.pdb_file:
        pdb_ids += cargar_ids_desde_archivo(args.pdb_file, "PDB")
    pdb_ids = validar_pdb_ids(pdb_ids)
    return pdb_ids


def cargar_ids_desde_archivo(filepath, descripcion):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe ({descripcion})")
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]


def validar_pdb_ids(ids):
    valid = []
    for pdb_id in ids:
        if len(pdb_id) == 4 and pdb_id.isalnum():
            valid.append(pdb_id.upper())
        else:
            print(f"⚠️ ID PDB inválido: {pdb_id} (se ignorará)")
    return list(set(valid))
