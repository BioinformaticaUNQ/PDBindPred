# PDBindPred

**PDBindPred** es una herramienta de línea de comandos desarrollada en Python que permite anotar estructuras de proteínas disponibles en el PDB, enriqueciendo la información con datos experimentales como resoluciones, año de publicación y afinidades de unión de ligandos, integrando datos de RCSB PDB, UniProt y ChEMBL.

---

## 📦 Requisitos

- Python 3.11 o superior  
- Dependencias (ver `requirements.txt`)

Instalación de dependencias:
```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

Ejecutar el script desde la raíz del proyecto con:

```bash
python -m PDBindPred.main --pdb <PDB_ID> [--aff <tipos_de_afinidad>]
```

### Argumentos

| Parámetro   | Descripción                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `--pdb`     | ID del complejo PDB a analizar (por ejemplo: `1MQ8`)                       |
| `--aff`     | (Opcional) Filtro de tipos de afinidad (por ejemplo: `Ki,Kd,IC50`)         |

### Ejemplos

```bash
# Búsqueda sin filtrar afinidades
python -m PDBindPred.main --pdb 1MQ8

# Búsqueda solo de afinidades tipo Ki y IC50
python -m PDBindPred.main --pdb 1MQ8 --aff Ki,IC50
```

---

## 🧪 Output

El resultado se guarda como un archivo `.json` dentro de la carpeta `output/`, con el siguiente formato:

```json
{
    "pdb_id": "1MQ8",
    "resolution": 2.3,
    "year": "2007",
    "ligands": [
        {
            "chembl_id": "CHEMBLxxxx",
            "type": "IC50",
            "value": "70.0",
            "unit": "nM",
            "year": "2008"
        }
    ],
    "source": "RCSB PDB",
    "uniprot_id": "P12345",
    "chembl_id": "CHEMBLxxxx"
}
```

---

## 🧠 Cómo funciona

1. Consulta a RCSB PDB para obtener metadatos del complejo (`resolution`, `year`, etc.).
2. Mapea el PDB ID a UniProt ID usando la API de UniProt.
3. Mapea el UniProt ID a ChEMBL Target ID.
4. Consulta ChEMBL y obtiene actividades de tipo `Binding` (`assay_type__exact=B`), filtrando por tipo de afinidad si se especifica.
5. Guarda el resultado anotado en un archivo JSON.

---

## 🗂️ Estructura del proyecto

```
PDBindPred/
├── PDBindPred/
│   ├── __init__.py
│   ├── main.py
│   ├── get_ids.py
│   └── output/
├── tests/
│   └── ... (por implementar)
├── requirements.txt
└── README.md
```

---

## 📌 TODO (pendientes)

- [ ] Agregar casos de error más robustos (IDs inválidos, sin conexión, etc.)
- [ ] Implementar tests unitarios (en carpeta `tests/`)
- [ ] Mejorar estructura modular separando lógica de ChEMBL en archivo aparte
- [ ] Traducir completamente el `--help` al español (custom help formatter)
- [ ] Ampliar filtros avanzados (por unidad, rango de valores, año, etc.)
- [ ] Agregar setup.py y posibilidad de instalar como CLI (`pip install -e .`)