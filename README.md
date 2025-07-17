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

- Tener instalado [**Python 3.11.4**](https://www.python.org/downloads/release/python-3114/) (u otra versión compatible).
- Instalar dependencias necesarias:

```bash
pip install -r requirements.txt
```
## 🚀 Ejemplos de Uso

### 🔹 Consulta simple por PDB ID
```bash
python -m src.main --pdb 1MQ8
```
Consulta datos estructurales y ligandos para el PDB ID `1MQ8`.

### 🔹 Consulta múltiple por PDB IDs con afinidades filtradas
```bash
python -m src.main --pdb 1MQ8,6CCF --aff IC50,Kd
```
Consulta múltiples PDB IDs, incluyendo solo afinidades tipo **Ki** y **Kd**.

### 🔹 Consulta desde archivo de IDs PDB
```bash
python -m src.main --pdb-file ids_pdb.txt
```
Lee IDs de un archivo de texto y realiza las consultas correspondientes.

### 🔹 Consulta por PDB ID en relacion a determinados ligandos
```bash
python -m src.main --pdb 1MQ8 --lig CHEMBL258114,CHEMBL117198
```
Consulta datos estructurales para el PDB ID `1MQ8` y, si posee, 
su afinidad con los ligandos CHEMBL258114 y CHEMBL117198.

### 🔹 Consulta por UniProt ID
```bash
python -m src.main --uniprot P05067 --aff Ki
```
Consulta ligandos y afinidades para el UniProt ID `P05067`.

### 🔹 Consulta desde archivo de IDs UniProt
```bash
python -m src.main --uniprot-file ids_uniprot.txt
```
Lee UniProt IDs desde un archivo de texto y procesa cada uno.

## ⚙️ Parámetros Adicionales

- `--aff`: Lista de tipos de afinidad a incluir en los resultados (Ej: `Ki,Kd,IC50`).

Los parámetros pueden combinarse. Por ejemplo, es posible consultar IDs de PDB y UniProt en la misma ejecución.

## 🧪 Tests

Para correr los tests del proyecto, utilizá el siguiente comando desde la raíz del repositorio:

```bash
python -m unittest discover -s tests
```
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
dicha tarea de decidió utilizar por su velocidad y practicidad las APIs 
de Uniprot: <br/>
a) las IDs de PDB deben ser primero traducidas a IDs de UniProt, y 
para este paso se utiliza el serivico [IDMapping de UniProt](https://www.uniprot.org/id-mapping).<br/> 
b) las IDs de UniProt son pasadas a sus equivalentes en ChEMBL 
usando la [API regular de Uniprot](https://www.uniprot.org/api-documentation/uniprotkb) 
ya que de esta manera se obtienen también (para aquellas consultas 
hechas directamente con ID de Uniprot) sus IDs de PDB y la resolución 
de la proteína para cada una de ellas. 
- Al momento de hacer esta aplicación, no encontramos una base que una 
los IDs de ligandos en ChEMBL a otras de las bases aquí utilizadas como 
UniProt o PDB; al correr muchas de las IDs en UniProt IDMapping no se 
encuentran resultados. Por ese motivo se tomó la decisión de que los 
ligandos sean ingresados en la consulta directamente con su ChEMBL ID.

## 🔗 Referencias Útiles

- [RCSB PDB API](https://data.rcsb.org)
- [UniProt ID Mapping API](https://www.uniprot.org/help/id_mapping)
- [ChEMBL API](https://www.ebi.ac.uk/chembl/ws)

---

> ⚠️ Esta herramienta fue desarrollada con fines educativos y puede requerir adaptaciones para uso productivo.
