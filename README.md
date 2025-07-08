# 🧬 PDBindPred

Herramienta de anotación básica de estructuras PDB. Permite 
obtener datos estructurales y de afinidad molecular desde 
**RCSB PDB**, **UniProt** y **ChEMBL**.

## 📋 Descripción
Este script permite consultar información de proteínas y sus 
ligandos desde ChEMBL, a partir de IDs de **PDB** o **UniProt**. 
Los datos obtenidos incluyen:

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

### Algunas decisiones tomadas para el desarrollo de esta aplicación
- Este trabajo se inició estudiando tres bases de datos: 
[ChEMBL](https://www.ebi.ac.uk/chembl/), 
[PDBbind](https://www.pdbbind-plus.org.cn/) 
(que ofrece datos de manera gratuita sólo del año 2020 para atrás) y 
[BindingDB](https://www.bindingdb.org/rwd/bind/index.jsp). 
Sin embargo, debido a las diferencias en las estructuras 
de dichas bases de datos, la consulta a las tres bases en simultáneo y 
la posterior unificación de sus resultados resultó imposible. Se 
decidió por tanto restringir la aplicación a una sola base de datos,
ChEMBL, para priorizar que los datos obtenidos no generen ambigüedades 
para quienes los usen.
- ChEMBL permite consultas en su base de datos a través de sus propios 
identificadores, por lo que las IDs de PDB o UniProt ingresadas en las 
consultas a este programa deben ser traducidas a IDs de ChEMBL. Para 
dicha tarea de decidió utilizar por su velocidad y practicidad la API 
[IDMapping de UniProt](https://www.uniprot.org/id-mapping). En el 
caso de las IDs de PDB, se hacen dos 
consultas: primero se traduce la ID de PDB a ID Uniprot, y luego de 
Uniprot a ID ChEMBL.

## 🔗 Referencias Útiles

- [RCSB PDB API](https://data.rcsb.org)
- [UniProt ID Mapping API](https://www.uniprot.org/help/id_mapping)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/ws)

---

> ⚠️ Esta herramienta fue desarrollada con fines educativos y puede requerir adaptaciones para uso productivo.
