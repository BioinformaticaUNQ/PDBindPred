# 🧬 PDBindPred

**PDBindPred** es una herramienta de línea de comandos que permite anotar estructuras PDB con información relevante proveniente de bases de datos como RCSB PDB, UniProt y ChEMBL. El resultado se guarda en formato JSON.

## 📦 Instalación

Clonar el repositorio y asegurarse de tener Python 3.11+:

```bash
git clone https://github.com/tu_usuario/PDBindPred.git
cd PDBindPred
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

## 🚀 Uso

Ejecutá el script desde la raíz del paquete:

```bash
python -m PDBindPred.main --pdb 1MQ8
```

### Argumentos disponibles

```bash
$ python -m PDBindPred.main --help

PDBindPred - Anotación básica de estructuras PDB

Opciones:
  --pdb        Uno o más IDs PDB separados por coma (ej: 1MQ8,2VDU)
  --pdb-file   Archivo con una lista de IDs PDB. El archivo ingresado debe tener una ID por línea, sin ningún otro separador, y debe encontrarse ubicado en la misma carpeta que el archivo main.py. Formatos testeados para los archivos: txt y csv.
  --aff        Tipos de afinidad a incluir, separados por coma (ej: Ki,Kd,IC50)


Ejemplos de uso:
  python -m PDBindPred.main --uniprot P05067
  python -m PDBindPred.main --pdb 1MQ7
  python -m PDBindPred.main --pdb 1MQ8,2VDU --aff Ki,Kd
  python -m PDBindPred.main --pdb-file ids.txt
```

## 📂 Salida

Los archivos generados se guardan automáticamente en el directorio:

```
PDBindPred/output/
```

Cada archivo de salida se llama:  
`output_<ID>.json` 

## 🧪 Tests

Próximamente.
