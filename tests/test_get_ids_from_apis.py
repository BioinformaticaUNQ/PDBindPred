import src.get_ids_from_apis
import src.main
import unittest


class TestsGetIdsFromApis(unittest.TestCase):

    def test_get_uniprot_id_from_existing_pdb_id(self):
        pdb_id = "6IK4"
        uniprot_id = src.get_ids_from_apis.get_uniprot_id_from_pdb_id(pdb_id)
        self.assertEqual("E7D102", uniprot_id)

    def test_get_id_data_from_uniprot_id(self):
        uniprot_id = "P61812"
        ids_data = src.get_ids_from_apis.get_ids_from_uniprot_id(uniprot_id)
        self.assertEqual(12, len(ids_data))


if __name__ == '__main__':
    unittest.main()