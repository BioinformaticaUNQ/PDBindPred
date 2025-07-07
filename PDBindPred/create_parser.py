import argparse
from argparse import RawTextHelpFormatter


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
