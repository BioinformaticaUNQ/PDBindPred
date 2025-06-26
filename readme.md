# PDBindPred

Herramienta de línea de comandos para recuperar información básica de estructuras del PDB.

## Uso

```bash
python PDBindPred/main.py --pdb 6IK4
```

#### Decisiones tomadas
- Para mapear la id de PDB ingresada, se utilizó la API 
de Uniprot; a partir de la id PDB, se busca la id de Uniprot, 
y a partir de la id de Uniprot se busca la id de ChEMBL 
(Uniprot no deja mapear directamente de PDB a ChEMBL). 
