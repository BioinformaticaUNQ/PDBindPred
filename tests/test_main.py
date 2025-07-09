import unittest

import src.create_parser
import src.main
from src.main import validate_input


class TestsMain(unittest.TestCase):
    def test_validate_correct_pdb_input_arguments(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--pdb', '1MQ7'])
        self.assertEqual('1MQ7', args.pdb)

    def test_validate_correct_uniprot_input_arguments(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--uniprot', 'Q9Y2H6'])
        self.assertEqual('Q9Y2H6', args.uniprot)

    def test_validate_correct_pdb_and_uniprot_input_arguments(self):
        parser = src.create_parser.create_parser()
        args = parser.parse_args(['--uniprot', 'Q9Y2H6', '--pdb', '1MQ7', '--aff', 'Ki'])
        self.assertEqual('1MQ7', args.pdb)
        self.assertEqual('Q9Y2H6', args.uniprot)
        self.assertEqual('Ki', args.aff)

    def test_checks_incorrect_input_and_fails(self):
        parser = src.create_parser.create_parser()
        with self.assertRaises(Exception):
            parser.parse_args(['--pd', '1MQ7'])

    def test_checks_missing_input_and_fails(self):
        parser = src.create_parser.create_parser()
        with self.assertRaises(Exception):
            parser.parse_args(['--pdb'])

    def test_validate_input_arguments_without_any_id_and_fails(self):
        parser = src.create_parser.create_parser()
        parser.parse_args(['--aff', 'Ki'])
        with self.assertRaises(Exception):
            validate_input(parser)


if __name__ == '__main__':
    unittest.main()