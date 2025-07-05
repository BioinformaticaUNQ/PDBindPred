import argparse
import os
from argparse import RawTextHelpFormatter
from PDBindPred.pdb_handler import process_pdb, process_uniprot
from PDBindPred import config
import time

class CustomArgumentParser(argparse.ArgumentParser):
    def _get_optionals_title(self):
        return 'Opciones'

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

def validar_uniprot_ids(ids):
    valid = []
    for uniprot_id in ids:
        if (6 <= len(uniprot_id) <= 10) and all(c.isalnum() for c in uniprot_id):
            valid.append(uniprot_id.upper())
        else:
            print(f"⚠️ ID UniProt inválido: {uniprot_id} (se ignorará)")
    return list(set(valid))

def main():
    parser = CustomArgumentParser(
        description="PDBindPred - Anotación básica de estructuras PDB",
        epilog="""
    Ejemplos de uso:
    python -m PDBindPred.main --pdb 1MQ8
    python -m PDBindPred.main --pdb 1MQ8,2VDU --aff Ki,Kd
    python -m PDBindPred.main --pdb-file ids_pdb.txt
    python -m PDBindPred.main --uniprot P12345,Q8N163
    python -m PDBindPred.main --uniprot-file ids_uniprot.txt
    """,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("--pdb", help="Uno o más IDs PDB separados por coma (ej: 1MQ8,2VDU)")
    parser.add_argument("--pdb-file", help="Archivo con una lista de IDs PDB, uno por línea")
    parser.add_argument("--uniprot", help="Uno o más IDs UniProt separados por coma (ej: P12345,Q8N163)")
    parser.add_argument("--uniprot-file", help="Archivo con una lista de IDs UniProt, uno por línea")
    parser.add_argument("--aff", help="Tipos de afinidad a incluir, separados por coma (ej: Ki,Kd,IC50)")
    args = parser.parse_args()

    if not any([args.pdb, args.pdb_file, args.uniprot, args.uniprot_file]):
        parser.error("Debe proporcionar al menos uno de: --pdb, --pdb-file, --uniprot o --uniprot-file")

    # Leer IDs PDB
    pdb_ids = []
    if args.pdb:
        pdb_ids += [p.strip() for p in args.pdb.split(",") if p.strip()]
    if args.pdb_file:
        pdb_ids += cargar_ids_desde_archivo(args.pdb_file, "PDB")

    pdb_ids = validar_pdb_ids(pdb_ids)

    # Leer IDs UniProt
    uniprot_ids = []
    if args.uniprot:
        uniprot_ids += [u.strip() for u in args.uniprot.split(",") if u.strip()]
    if args.uniprot_file:
        uniprot_ids += cargar_ids_desde_archivo(args.uniprot_file, "UniProt")

    uniprot_ids = validar_uniprot_ids(uniprot_ids)

    affinity_types = args.aff.split(",") if args.aff else None

    # Validar límite de IDs permitidos (configurable)
    if len(uniprot_ids) > config.MAX_UNIPROT_IDS_PER_QUERY:
        print(f"⚠️ Límite excedido: Máximo permitido de IDs UniProt por consulta: {config.MAX_UNIPROT_IDS_PER_QUERY}.")
        print("🔗 Por favor, divida sus consultas en partes más pequeñas.")
        return

    if len(pdb_ids) > config.MAX_PDB_IDS_PER_QUERY:
        print(f"⚠️ Límite excedido: Máximo permitido de IDs PDB por consulta: {config.MAX_PDB_IDS_PER_QUERY}.")
        print("🔗 Por favor, divida sus consultas en partes más pequeñas.")
        return

    if pdb_ids:
        print(f"🔍 Procesando {len(pdb_ids)} ID(s) de PDB...")
        for pdb_id in pdb_ids:
            try:
                process_pdb(pdb_id, affinity_types)
                time.sleep(config.CHEMBL_REQUEST_DELAY)
            except Exception as e:
                print(f"❌ Error procesando PDB {pdb_id}: {e}")

    if uniprot_ids:
        print(f"🔍 Procesando {len(uniprot_ids)} ID(s) de UniProt...")
        for uniprot_id in uniprot_ids:
            try:
                process_uniprot(uniprot_id, affinity_types)
                time.sleep(config.UNIPROT_REQUEST_DELAY)
            except Exception as e:
                print(f"❌ Error procesando UniProt {uniprot_id}: {e}")

if __name__ == "__main__":
    main()
