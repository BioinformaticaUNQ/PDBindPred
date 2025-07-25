from src.create_parser import create_parser
from src.get_ids_from_input import get_pdb_ids_from_arguments, get_uniprot_ids_from_arguments, \
    get_ligands_from_arguments
from src.pdb_handler import process_pdb, process_uniprot
from src import config
import time


def main():
    """
    Función principal del programa.
    Se encarga de:
    - Parsear los argumentos de entrada.
    - Validar los IDs ingresados.
    - Procesar cada ID de PDB o UniProt, consultando fuentes externas.
    - Guardar los resultados en archivos JSON.
    """
    print("\n🚀 Inicio de ejecución de src\n")
    parser = create_parser()

    args = validate_input(parser)

    # Leer IDs PDB
    pdb_ids = get_pdb_ids_from_arguments(args)

    # Leer IDs UniProt
    uniprot_ids = get_uniprot_ids_from_arguments(args)

    # Toma la afinidad
    affinity_types = args.aff.split(",") if args.aff else None

    # Leer los ligandos
    ligands_ids = get_ligands_from_arguments(args) if (args.lig or args.lig_file) else None

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
                process_pdb(pdb_id, affinity_types, ligands_ids)
                time.sleep(config.CHEMBL_REQUEST_DELAY)
            except Exception as e:
                print(f"❌ Error procesando PDB {pdb_id}: {e}")

    if uniprot_ids:
        print(f"🔍 Procesando {len(uniprot_ids)} ID(s) de UniProt...")
        for uniprot_id in uniprot_ids:
            try:
                process_uniprot(uniprot_id, affinity_types, ligands_ids)
                time.sleep(config.UNIPROT_REQUEST_DELAY)
            except Exception as e:
                print(f"❌ Error procesando UniProt {uniprot_id}: {e}")
    
    print("\n🏁 Ejecución completada\n")


def validate_input(parser):
    """
    Valida que al menos uno de los argumentos requeridos haya sido ingresado. 
    Lanza un error si no se proporciona ningún ID de PDB o UniProt.
    """
    args = parser.parse_args()
    if not any([args.pdb, args.pdb_file, args.uniprot, args.uniprot_file]):
        parser.error()
    return args

if __name__ == "__main__":
    """
    Punto de entrada del script cuando se ejecuta directamente.
    """
    try:
        main()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
