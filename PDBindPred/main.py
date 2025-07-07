import argparse
from argparse import RawTextHelpFormatter

from PDBindPred.get_ids_from_input import get_pdb_ids_from_arguments, get_uniprot_ids_from_arguments
from PDBindPred.pdb_handler import process_pdb, process_uniprot
from PDBindPred import config
import time

class CustomArgumentParser(argparse.ArgumentParser):
    def _get_optionals_title(self):
        return 'Opciones'
    def error(self, message):
        raise Exception("Los argumentos posibles son: --pdb, "
                        "--pdb-file, --uniprot, --uniprot-file, --aff. Para más "
                        "información revise el archivo README o consulte "
                        "la ayuda de este programa escribiendo: python -m "
                        "PDBindPred.main --help")

def create_parser():
    parser = CustomArgumentParser(
        exit_on_error=False,
        description="PDBindPred - Anotación básica de estructuras PDB",
        epilog="""
    Ejemplos de uso:
    python -m PDBindPred.main --pdb 1MQ8
    python -m PDBindPred.main --pdb 1MQ8,2VDU --aff Ki,Kd
    python -m PDBindPred.main --pdb-file ids_pdb.txt
    python -m PDBindPred.main --uniprot P12345,Q8N163
    python -m PDBindPred.main --uniprot-file ids_uniprot.txt
    
    El archivo ingresado debe tener una ID por línea, sin ningún otro 
    separador, y debe encontrarse ubicado en la misma carpeta que el 
    archivo main.py. Formatos testeados para los archivos: txt y csv.
    """,
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("--pdb", help="Uno o más IDs PDB separados por coma (ej: 1MQ8,2VDU)")
    parser.add_argument("--pdb-file", help="Archivo con una lista de IDs PDB, uno por línea")
    parser.add_argument("--uniprot", help="Uno o más IDs UniProt separados por coma (ej: P12345,Q8N163)")
    parser.add_argument("--uniprot-file", help="Archivo con una lista de IDs UniProt, uno por línea")
    parser.add_argument("--aff", help="Tipos de afinidad a incluir, separados por coma (ej: Ki,Kd,IC50)")
    return parser



def main():
    print("\n🚀 Inicio de ejecución de PDBindPred\n")
    parser = create_parser()

    args = validate_input(parser)

    # Leer IDs PDB
    pdb_ids = get_pdb_ids_from_arguments(args)

    # Leer IDs UniProt
    uniprot_ids = get_uniprot_ids_from_arguments(args)

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
    
    print("\n🏁 Ejecución completada\n")


def validate_input(parser):
    args = parser.parse_args()
    if not any([args.pdb, args.pdb_file, args.uniprot, args.uniprot_file]):
        parser.error()
    return args

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
