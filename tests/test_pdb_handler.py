import unittest

from src.pdb_handler import fetch_pdb_info


class TestsPdbHandler(unittest.TestCase):
    def test_fetch_pdb_info_successfully(self):
        pdb_id = '1MQ8'
        pdb_id_data = fetch_pdb_info(pdb_id)
        self.assertEqual('1MQ8', pdb_id_data['pdb_id'])
        self.assertEqual(3.3, pdb_id_data['resolution'])
        self.assertEqual('2003', pdb_id_data['publication_year'])
        self.assertEqual('10.1016/S0092-8674(02)01257-6', pdb_id_data['doi'])
        self.assertEqual([], pdb_id_data['ligands'])

if __name__ == '__main__':
    unittest.main()