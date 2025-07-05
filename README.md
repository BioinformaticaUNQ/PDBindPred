# 🧬 PDBindPred

Herramienta de anotación básica de estructuras PDB. Permite obtener datos estructurales y de afinidad molecular desde **RCSB PDB**, **UniProt** y **ChEMBL**.

## 📋 Descripción
Este script permite consultar información de proteínas y sus ligandos desde diversas bases de datos públicas, a partir de IDs de **PDB** o **UniProt**. Los datos obtenidos incluyen:

- Resolución de la estructura
- Año de publicación
- DOI (cuando esté disponible)
- Ligandos asociados (con sus IDs, afinidades y ensayos)

## ⚙️ Requisitos Previos

- **Python 3.11.4** (u otra versión compatible)
- Instalar dependencias necesarias:

```bash
pip install requests
```

## 🚀 Ejemplos de Uso

### 🔹 Consulta simple por PDB ID
```bash
python -m PDBindPred.main --pdb 1MQ8
```
Consulta datos estructurales y ligandos para el PDB ID `1MQ8`.

### 🔹 Consulta múltiple por PDB IDs con afinidades filtradas
```bash
python -m PDBindPred.main --pdb 1MQ8,2VDU --aff Ki,Kd
```
Consulta múltiples PDB IDs, incluyendo solo afinidades tipo **Ki** y **Kd**.

### 🔹 Consulta desde archivo de IDs PDB
```bash
python -m PDBindPred.main --pdb-file ids_pdb.txt
```
Lee IDs de un archivo de texto y realiza las consultas correspondientes.

### 🔹 Consulta por UniProt ID
```bash
python -m PDBindPred.main --uniprot P12345
```
Consulta ligandos y afinidades para el UniProt ID `P12345`.

### 🔹 Consulta desde archivo de IDs UniProt
```bash
python -m PDBindPred.main --uniprot-file ids_uniprot.txt
```
Lee UniProt IDs desde un archivo de texto y procesa cada uno.

## ⚙️ Parámetros Adicionales

- `--aff`: Lista de tipos de afinidad a incluir en los resultados (Ej: `Ki,Kd,IC50`).

Los parámetros pueden combinarse. Por ejemplo, es posible consultar IDs de PDB y UniProt en la misma ejecución.

## 🗃️ Detalles Adicionales

### ✅ Caché Local (Opcional)
- Los resultados se guardan en la carpeta `PDBindPred/output/` para evitar consultas repetidas.
- Si `ENABLE_LOCAL_CACHE` está activado en `config.py`, la herramienta reutiliza los resultados existentes.

Archivos de salida:
- `pdb_<pdb_id>.json` → Datos obtenidos por PDB ID.
- `uniprot_<uniprot_id>.json` → Datos obtenidos por UniProt ID.

### ✅ Límites de IDs por Consulta
- **UniProt IDs**: máximo **1000** por ejecución (ajustable en `config.py`).
- **PDB IDs**: mismo límite.

### ✅ Comunicación en Consola
- Se reportan todos los pasos: envíos de consulta, datos encontrados, uso de caché, y cualquier error (incluyendo timeouts o errores de API).

### ✅ Notas sobre el Campo DOI
- El campo **DOI** solo se incluye cuando la información está disponible en la base RCSB PDB.

## 🔗 Referencias Útiles

- [RCSB PDB API](https://data.rcsb.org)
- [UniProt ID Mapping API](https://www.uniprot.org/help/id_mapping)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/ws)

---

> ⚠️ Esta herramienta fue desarrollada con fines educativos y puede requerir adaptaciones para uso productivo.
