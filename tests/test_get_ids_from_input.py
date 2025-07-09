import src.create_parser
from src.get_ids_from_input import cargar_ids_desde_archivo, validar_pdb_ids, validar_uniprot_ids
import src.main
import unittest

class TestsGetIdsFromInput(unittest.TestCase):

    def test_load_pdb_ids_from_file_successfully(self):
        pdb_ids_list = cargar_ids_desde_archivo("test_pdb_ids.txt", "PDB ids")
        self.assertEqual(3, len(pdb_ids_list))
        self.assertIn('3at1', pdb_ids_list)

    def test_load_uniprot_ids_from_file_successfully(self):
        pdb_ids_list = cargar_ids_desde_archivo("test_uniprot_ids.txt", "PDB ids")
        self.assertEqual(4, len(pdb_ids_list))
        self.assertIn('Q9Y2H6', pdb_ids_list)

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

    def test_validate_correct_uniprot_ids(self):
        uniprot_ids = ['P15529', 'Q9Y2H6', 'A0A010RRV2']
        validated_uniprot_ids = validar_uniprot_ids(uniprot_ids)
        self.assertEqual(3, len(validated_uniprot_ids))

    def test_validate_correct_pdb_ids_and_ignores_incorrect_ones(self):
        pdb_ids = ['3at1,', '7gc', '2tm*', '7gch']
        validated_pdb_ids = validar_pdb_ids(pdb_ids)
        self.assertEqual(1, len(validated_pdb_ids))
        self.assertIn('7GCH', validated_pdb_ids)

    def test_validate_correct_uniprot_ids_and_ignores_incorrect_ones(self):
        uniprot_ids = ['P155', 'Q9Y2*6', 'A0A010RRV2DD', 'P15529']
        validated_uniprot_ids = validar_uniprot_ids(uniprot_ids)
        self.assertEqual(1, len(validated_uniprot_ids))
        self.assertIn('P15529', validated_uniprot_ids)

    def test_get_individual_pdb_id_from_arguments_successfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8'])
        pdb_ids = src.get_ids_from_input.get_pdb_ids_from_arguments(args)
        self.assertEqual(1, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)

    def test_get_multiple_pdb_ids_from_arguments_succesfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8, 7gch'])
        pdb_ids = src.get_ids_from_input.get_pdb_ids_from_arguments(args)
        self.assertEqual(2, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)
        self.assertIn('7GCH', pdb_ids)

    def test_get_multiple_pdb_ids_from_file_and_arguments_successfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--pdb', '1MQ8, 7gch', '--pdb-file', 'test_pdb_ids.txt'])
        pdb_ids = src.get_ids_from_input.get_pdb_ids_from_arguments(args)
        self.assertEqual(4, len(pdb_ids))
        self.assertIn('1MQ8', pdb_ids)
        self.assertIn('7GCH', pdb_ids)
        self.assertIn('2TMN', pdb_ids)
        self.assertIn('3AT1', pdb_ids)

    def test_get_individual_uniprot_id_from_arguments_successfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--uniprot', 'A0A010RRV2'])
        uniprot_ids = src.get_ids_from_input.get_uniprot_ids_from_arguments(args)
        self.assertEqual(1, len(uniprot_ids))
        self.assertIn('A0A010RRV2', uniprot_ids)

    def test_get_multiple_uniprot_ids_from_arguments_succesfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--uniprot', 'A0A010RRV2, Q9Y2H6'])
        uniprot_ids = src.get_ids_from_input.get_uniprot_ids_from_arguments(args)
        self.assertEqual(2, len(uniprot_ids))
        self.assertIn('A0A010RRV2', uniprot_ids)
        self.assertIn('Q9Y2H6', uniprot_ids)

    def test_get_multiple_uniprot_ids_from_file_and_arguments_successfully(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--uniprot', 'A0A010RRV2, Q9Y2H6', '--uniprot-file', 'test_uniprot_ids.txt'])
        uniprot_ids = src.get_ids_from_input.get_uniprot_ids_from_arguments(args)
        self.assertEqual(5, len(uniprot_ids))
        self.assertIn('A0A010RRV2', uniprot_ids)
        self.assertIn('Q9Y2H6', uniprot_ids)
        self.assertIn('P15529', uniprot_ids)
        self.assertIn('O75970', uniprot_ids)
        self.assertIn('P08648', uniprot_ids)

if __name__ == '__main__':
    unittest.main()