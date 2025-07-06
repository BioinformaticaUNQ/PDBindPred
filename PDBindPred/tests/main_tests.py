import PDBindPred.get_ids
import PDBindPred.main
import unittest

from PDBindPred.main import cargar_ids_desde_archivo, validar_pdb_ids


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

    def test_load_pdb_ids_from_file_successfully(self):
        pdb_ids_list = cargar_ids_desde_archivo("test_pdb_ids.txt", "PDB ids")
        self.assertEqual(3, len(pdb_ids_list))
        self.assertIn('3at1', pdb_ids_list)

    def test_load_pdb_ids_from_csv_file_successfully(self):
        pdb_ids_list = cargar_ids_desde_archivo("test_pdb_ids.csv", "PDB ids")
        self.assertEqual(3, len(pdb_ids_list))
        self.assertIn('3at1', pdb_ids_list)

    def test_load_pdb_ids_from_unexisting_file_fails(self):
        with self.assertRaises(FileNotFoundError):
            cargar_ids_desde_archivo("test_pdb.txt", "PDB ids")

    def test_validate_correct_pdb_ids(self):
        pdb_ids = ['3at1', '7gch', '2tmn']
        validated_pdb_ids = validar_pdb_ids(pdb_ids)
        self.assertEqual(3, len(validated_pdb_ids))

    def test_validate_correct_pdb_ids_and_ignores_incorrect_ones(self):
        pdb_ids = ['3at1,', '7gc', '2tm*', '7gch']
        validated_pdb_ids = validar_pdb_ids(pdb_ids)
        self.assertEqual(1, len(validated_pdb_ids))
        self.assertIn('7GCH', validated_pdb_ids)

    def test_get_individual_pdb_id_from_arguments_successfully(self):
        parser = PDBindPred.main.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8'])
        pdb_ids = PDBindPred.main.get_pdb_ids_from_arguments(args)
        self.assertEqual(1, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)

    def test_get_multiple_pdb_ids_from_arguments_succesfully(self):
        parser = PDBindPred.main.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8, 7gch'])
        pdb_ids = PDBindPred.main.get_pdb_ids_from_arguments(args)
        self.assertEqual(2, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)
        self.assertIn('7GCH', pdb_ids)

    def test_get_multiple_pdb_ids_from_file_and_arguments_successfully(self):
        parser = PDBindPred.main.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8, 7gch', '--pdb-file', 'test_pdb_ids.txt'])
        pdb_ids = PDBindPred.main.get_pdb_ids_from_arguments(args)
        self.assertEqual(4, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)
        self.assertIn('7GCH', pdb_ids)
        self.assertIn('2TMN', pdb_ids)
        self.assertIn('3AT1', pdb_ids)

if __name__ == '__main__':
    unittest.main()