import unittest

from src.pdb_handler import fetch_pdb_info, get_binding_activities_for_target_from_chembl, \
    get_ligands_from_chembl_target


class TestsPdbHandler(unittest.TestCase):
    def test_fetch_pdb_info_successfully(self):
        pdb_id = '1MQ8'
        pdb_id_data = fetch_pdb_info(pdb_id)
        self.assertEqual('1MQ8', pdb_id_data['pdb_id'])
        self.assertEqual(3.3, pdb_id_data['resolution'])
        self.assertEqual('2003', pdb_id_data['publication_year'])
        self.assertEqual('10.1016/S0092-8674(02)01257-6', pdb_id_data['doi'])
        self.assertEqual([], pdb_id_data['ligands'])

    "Testea que la aplicación lanza una excepción si se ingresa una PDB id inexistente."
    def test_fetch_pdb_info_with_unexisting_pdb_id(self):
        pdb_id = 'F6HI'
        with self.assertRaises(Exception):
            fetch_pdb_info(pdb_id)

    """
    Testea que para una dada ChEMBL ID, la consulta traiga la cantidad correcta de actividades 
      de binding y que en todas las actividades el target sea la ChEMBL ID correspondiente.
    """
    def test_get_binding_activities_for_target_from_chembl_successfully(self):
        chembl_id = 'CHEMBL2079'
        activities = get_binding_activities_for_target_from_chembl(chembl_id, None)
        activity_target_is_chembl_id = True
        for activity in activities:
            activity_target_is_chembl_id = activity_target_is_chembl_id and activity.find("target_chembl_id").text == chembl_id
        self.assertEqual(14, len(activities))
        self.assertTrue(activity_target_is_chembl_id)

    """Testea que para una ChEMBL ID se recupere la lista de ligandos que posean todos 
    los datos (id de ligando, valor de afinidad, tipo de afinidad o id de ensayo)"""
    def test_get_ligands_with_complete_data_from_chembl_target(self):
        chembl_id = 'CHEMBL2095'
        ligands = get_ligands_from_chembl_target(chembl_id, None)
        complete_data = True
        for ligand in ligands:
            complete_data = complete_data and not (None in ligand.values())
        self.assertEqual(17, len(ligands))

    """Testea que para una ChEMBL ID se recupere la lista de ligandos que posean todos 
    los datos (id de ligando, valor de afinidad, tipo de afinidad o id de ensayo) 
    y que coloque juntos los datos de ensayo de un mismo ligando"""
    def test_get_ligands_from_chembl_target_nesting_assays_from_same_ligand(self):
        chembl_id = 'CHEMBL2365'
        ligands = get_ligands_from_chembl_target(chembl_id, None)
        activities = get_binding_activities_for_target_from_chembl(chembl_id, None)
        complete_data = True
        assays = 0
        for ligand in ligands:
            complete_data = complete_data and not (None in ligand.values())
            assays += len(ligand['assays'])
        self.assertEqual(32, len(ligands))
        self.assertEqual(35, len(activities))
        self.assertEqual(35, assays)

    """Dada una ChEMBL ID testea que se obtengan los ligandos correspondientes a la misma,
    ignorando las activities que tengan datos incompletos (id de ligando, valor de 
    afinidad, tipo de afinidad o id de ensayo)"""
    def test_get_ligands_from_chembl_target_ignoring_ligands_with_incomplete_data(self):
        chembl_id = 'CHEMBL2077'
        ligands = get_ligands_from_chembl_target(chembl_id, None)
        self.assertEqual(3, len(ligands))


if __name__ == '__main__':
    unittest.main()