# src/config.py

# Límite de IDs permitidos por consulta
MAX_UNIPROT_IDS_PER_QUERY = 1000  # Límite de UniProt (documentado)
MAX_PDB_IDS_PER_QUERY = MAX_UNIPROT_IDS_PER_QUERY  # Usamos el mismo límite por simplicidad

# Máximo de afinidades por request a ChEMBL (aunque limitadas por diseño)
MAX_CHEMBL_AFFINITY_TYPES = 1000  # No suele ser un problema en tu caso

# Tiempo de espera entre requests para evitar rate limits (en segundos)
UNIPROT_REQUEST_DELAY = 0.5  # Medio segundo
CHEMBL_REQUEST_DELAY = 0.5  # Opcional, si querés regular

# ¿Habilitar cacheo local? Si es True, se usa el JSON local si ya existe
ENABLE_LOCAL_CACHE = True