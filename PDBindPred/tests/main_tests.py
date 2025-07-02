import PDBindPred.get_ids
import unittest

class Tests(unittest.TestCase):
    def test_get_uniprot_id_from_existing_pdb_id(self):
        pdb_id = "6IK4"
        uniprot_id = PDBindPred.get_ids.get_uniprot_id_from_pdb_id(pdb_id)
        self.assertEqual("E7D102", uniprot_id)

    def test_get_chembl_id_from_uniprot_id(self):
        uniprot_id = "P61812"
        chembl_id = PDBindPred.get_ids.get_chembl_id_from_uniprot_id(uniprot_id)
        self.assertEqual("CHEMBL3217393", chembl_id)

    def test_get_chembl_id_from_pdb_id(self):
        pdb_id = "1CY0"
        chembl_id = PDBindPred.get_ids.get_chembl_id_from_pdb_id(pdb_id)
        self.assertEqual("CHEMBL3259513", chembl_id)

if __name__ == '__main__':
    unittest.main()