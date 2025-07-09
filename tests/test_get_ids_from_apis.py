import src.get_ids_from_apis
import src.main
import unittest


class TestsGetIdsFromApis(unittest.TestCase):

    def test_get_uniprot_id_from_existing_pdb_id(self):
        pdb_id = "6IK4"
        uniprot_id = src.get_ids_from_apis.get_uniprot_id_from_pdb_id(pdb_id)
        self.assertEqual("E7D102", uniprot_id)

    def test_get_chembl_id_from_uniprot_id(self):
        uniprot_id = "P61812"
        chembl_id = src.get_ids_from_apis.get_chembl_id_from_uniprot_id(uniprot_id)
        self.assertEqual("CHEMBL3217393", chembl_id)

    def test_get_chembl_id_from_pdb_id(self):
        pdb_id = "1CY0"
        chembl_id = src.get_ids_from_apis.get_chembl_id_from_pdb_id(pdb_id)
        self.assertEqual("CHEMBL3259513", chembl_id)

if __name__ == '__main__':
    unittest.main()