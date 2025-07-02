import argparse
import requests
import json
import os
import xml.etree.ElementTree as ET
from argparse import RawTextHelpFormatter
from PDBindPred.pdb_handler import process_pdb
from PDBindPred.get_ids import get_uniprot_id_from_pdb_id, get_chembl_id_from_uniprot_id

class CustomArgumentParser(argparse.ArgumentParser):
    def _get_optionals_title(self):
        return 'Opciones'

def main():
    parser = CustomArgumentParser(
        description="PDBindPred - Anotación básica de estructuras PDB",
        epilog="""
    Ejemplos de uso:
    python -m PDBindPred.main --pdb 1MQ8
    python -m PDBindPred.main --pdb 1MQ8,2VDU --aff Ki,Kd
    python -m PDBindPred.main --pdb-file ids.txt
    """,
        formatter_class=RawTextHelpFormatter
    )


    parser.add_argument("--pdb", help="Uno o más IDs PDB separados por coma (ej: 1MQ8,2VDU)")
    parser.add_argument("--pdb-file", help="Archivo con una lista de IDs PDB, uno por línea")
    parser.add_argument("--aff", help="Tipos de afinidad a incluir, separados por coma (ej: Ki,Kd,IC50)")
    args = parser.parse_args()

    if not args.pdb and not args.pdb_file:
        parser.error("Debe proporcionar --pdb o --pdb-file")

    pdb_ids = []

    if args.pdb:
        pdb_ids.extend([p.strip() for p in args.pdb.split(",") if p.strip()])

    if args.pdb_file:
        if not os.path.isfile(args.pdb_file):
            parser.error(f"El archivo {args.pdb_file} no existe")
        with open(args.pdb_file, "r") as f:
            pdb_ids.extend([line.strip() for line in f if line.strip()])


    affinity_types = args.aff.split(",") if args.aff else None

    for pdb_id in pdb_ids:
        try:
            process_pdb(pdb_id, affinity_types)
        except Exception as e:
            print(f"❌ Error procesando {pdb_id}: {e}")

if __name__ == "__main__":
    main()