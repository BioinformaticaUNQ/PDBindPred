import argparse
from argparse import RawTextHelpFormatter


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Subclase personalizada de ArgumentParser que cambia el título de las opciones
    y redefine el comportamiento por defecto ante errores de argumentos.
    """
    def _get_optionals_title(self):
        """
        Redefine el título por defecto del grupo de argumentos opcionales.
        """
        return 'Opciones'
    def error(self, message):
        """
        Lanza una excepción con un mensaje personalizado cuando hay un error de argumentos.
        """
        raise Exception("Los argumentos posibles son: --pdb, "
                        "--pdb-file, --uniprot, --uniprot-file, --aff "
                        "--lig, --lig-file. Para más "
                        "información revise el archivo README o consulte "
                        "la ayuda de este programa escribiendo: python -m "
                        "src.main --help")


def create_parser():
    """
    Crea y configura un parser de argumentos para la línea de comandos,
    con ayuda extendida y ejemplos de uso.
    Retorna:
        CustomArgumentParser: Parser configurado con los argumentos disponibles.
    """
    parser = CustomArgumentParser(
        exit_on_error=False,
        description="src - Anotación básica de estructuras PDB",
        epilog="""
    Ejemplos de uso:
    python -m src.main --pdb 1MQ8
    python -m src.main --pdb 1MQ8,2VDU --aff Ki,Kd
    python -m src.main --pdb-file ids_pdb.txt
    python -m src.main --uniprot P12345,Q8N163
    python -m src.main --uniprot-file ids_uniprot.txt
    
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
    parser.add_argument("--lig", help="IDs Uniprot de ligandos sobre los cuales se quiere conocer la afinidad, separados por coma")
    parser.add_argument("--lig-file", help="Archivo con una lista de IDs Uniprot de ligandos sobre los cuales se quiere conocer la afinidad, uno por línea")
    return parser
