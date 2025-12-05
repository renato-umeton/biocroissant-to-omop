#!/usr/bin/env python3
"""Test suite for Bio-Croissant to OMOP CDM converter."""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import pandas as pd
from src.biocroissant_to_omop import (
    BioCroissantParser,
    OMOPTableMapper,
    DataExtractor,
    OMOPValidator,
    OMOPExporter,
    BioCroissantToOMOPConverter
)


class TestBioCroissantParser(unittest.TestCase):
    """Test Bio-Croissant metadata parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_metadata = {
            "@context": "https://mlcommons.org/croissant/bio/0.2/context",
            "@type": ["sc:Dataset"],
            "name": "Test Dataset",
            "recordSet": [
                {
                    "@type": "cr:RecordSet",
                    "@id": "person",
                    "name": "PERSON",
                    "omop:cdmTable": "PERSON",
                    "field": [
                        {
                            "@id": "person/person_id",
                            "name": "person_id",
                            "dataType": "sc:Integer",
                            "omop:cdmField": "person_id",
                            "omop:isPrimaryKey": True
                        }
                    ]
                }
            ],
            "distribution": [
                {
                    "@id": "person_csv",
                    "contentUrl": "data/person.csv",
                    "encodingFormat": "text/csv"
                }
            ]
        }
        self.parser = BioCroissantParser()

    def test_parse_metadata(self):
        """Test parsing Bio-Croissant metadata."""
        result = self.parser.parse(self.test_metadata)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "Test Dataset")

    def test_extract_recordsets(self):
        """Test extracting recordSets from metadata."""
        recordsets = self.parser.extract_recordsets(self.test_metadata)
        self.assertEqual(len(recordsets), 1)
        self.assertEqual(recordsets[0]['name'], 'PERSON')

    def test_extract_fields(self):
        """Test extracting fields from recordSet."""
        recordset = self.test_metadata['recordSet'][0]
        fields = self.parser.extract_fields(recordset)
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]['name'], 'person_id')

    def test_extract_distributions(self):
        """Test extracting file distributions."""
        distributions = self.parser.extract_distributions(self.test_metadata)
        self.assertEqual(len(distributions), 1)
        self.assertEqual(distributions[0]['contentUrl'], 'data/person.csv')


class TestOMOPTableMapper(unittest.TestCase):
    """Test mapping Bio-Croissant recordSets to OMOP tables."""

    def setUp(self):
        """Set up test fixtures."""
        self.mapper = OMOPTableMapper()

    def test_map_person_table(self):
        """Test mapping PERSON recordSet to OMOP PERSON table."""
        recordset = {
            "name": "PERSON",
            "omop:cdmTable": "PERSON",
            "field": [
                {"name": "person_id", "omop:cdmField": "person_id"},
                {"name": "gender_concept_id", "omop:cdmField": "gender_concept_id"}
            ]
        }
        mapping = self.mapper.map_table(recordset)
        self.assertEqual(mapping['omop_table'], 'PERSON')
        self.assertEqual(len(mapping['field_mappings']), 2)

    def test_identify_primary_key(self):
        """Test identifying primary key fields."""
        fields = [
            {"name": "person_id", "omop:isPrimaryKey": True},
            {"name": "gender_concept_id"}
        ]
        pk = self.mapper.identify_primary_key(fields)
        self.assertEqual(pk, 'person_id')

    def test_identify_foreign_keys(self):
        """Test identifying foreign key relationships."""
        fields = [
            {"name": "person_id", "omop:foreignKeyTable": "PERSON"},
            {"name": "condition_id"}
        ]
        fks = self.mapper.identify_foreign_keys(fields)
        self.assertEqual(len(fks), 1)
        self.assertEqual(fks[0]['field'], 'person_id')
        self.assertEqual(fks[0]['references_table'], 'PERSON')


class TestDataExtractor(unittest.TestCase):
    """Test extracting data from CSV files."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / "person.csv"

        # Create test CSV
        df = pd.DataFrame({
            'person_id': [1, 2, 3],
            'gender_concept_id': [8507, 8532, 8507],
            'year_of_birth': [1980, 1990, 1975]
        })
        df.to_csv(self.test_csv, index=False)

        self.extractor = DataExtractor()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_read_csv_file(self):
        """Test reading CSV file."""
        df = self.extractor.read_csv(self.test_csv)
        self.assertEqual(len(df), 3)
        self.assertIn('person_id', df.columns)

    def test_extract_from_distribution(self):
        """Test extracting data using distribution metadata."""
        distribution = {
            "@id": "person_csv",
            "contentUrl": str(self.test_csv),
            "encodingFormat": "text/csv"
        }
        df = self.extractor.extract_from_distribution(distribution)
        self.assertEqual(len(df), 3)


class TestOMOPValidator(unittest.TestCase):
    """Test OMOP CDM validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = OMOPValidator()

    def test_validate_person_table(self):
        """Test validating PERSON table data."""
        df = pd.DataFrame({
            'person_id': [1, 2, 3],
            'gender_concept_id': [8507, 8532, 8507],
            'year_of_birth': [1980, 1990, 1975],
            'race_concept_id': [8527, 8527, 8516],
            'ethnicity_concept_id': [38003563, 38003563, 38003564]
        })
        is_valid, errors = self.validator.validate_table('PERSON', df)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_primary_key_unique(self):
        """Test validating primary key uniqueness."""
        df = pd.DataFrame({
            'person_id': [1, 1, 3],  # Duplicate ID
            'gender_concept_id': [8507, 8532, 8507]
        })
        is_valid, errors = self.validator.validate_primary_key(df, 'person_id')
        self.assertFalse(is_valid)
        self.assertIn('duplicate', errors[0].lower())

    def test_validate_required_fields(self):
        """Test validating required fields are present."""
        df = pd.DataFrame({
            'person_id': [1, 2, 3]
            # Missing required field: gender_concept_id
        })
        required_fields = ['person_id', 'gender_concept_id']
        is_valid, errors = self.validator.validate_required_fields(df, required_fields)
        self.assertFalse(is_valid)
        self.assertIn('gender_concept_id', errors[0])


class TestOMOPExporter(unittest.TestCase):
    """Test exporting to OMOP CDM format."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.exporter = OMOPExporter()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_export_to_csv(self):
        """Test exporting table to CSV."""
        df = pd.DataFrame({
            'person_id': [1, 2, 3],
            'gender_concept_id': [8507, 8532, 8507],
            'year_of_birth': [1980, 1990, 1975]
        })
        output_path = Path(self.temp_dir) / "PERSON.csv"
        self.exporter.export_csv('PERSON', df, output_path)

        self.assertTrue(output_path.exists())
        result_df = pd.read_csv(output_path)
        self.assertEqual(len(result_df), 3)

    def test_generate_ddl(self):
        """Test generating SQL DDL for table."""
        table_schema = {
            'table_name': 'PERSON',
            'fields': [
                {'name': 'person_id', 'type': 'INTEGER', 'primary_key': True},
                {'name': 'gender_concept_id', 'type': 'INTEGER', 'nullable': False}
            ]
        }
        ddl = self.exporter.generate_ddl(table_schema, dialect='postgresql')
        self.assertIn('CREATE TABLE PERSON', ddl)
        self.assertIn('person_id', ddl)
        self.assertIn('PRIMARY KEY', ddl)


class TestBioCroissantToOMOPConverter(unittest.TestCase):
    """Test end-to-end conversion."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

        # Create test CSV
        self.test_csv = Path(self.temp_dir) / "person.csv"
        df = pd.DataFrame({
            'person_id': [1, 2, 3],
            'gender_concept_id': [8507, 8532, 8507],
            'year_of_birth': [1980, 1990, 1975],
            'race_concept_id': [8527, 8527, 8516],
            'ethnicity_concept_id': [38003563, 38003563, 38003564]
        })
        df.to_csv(self.test_csv, index=False)

        # Create test metadata
        self.test_metadata_path = Path(self.temp_dir) / "metadata.json"
        metadata = {
            "@context": "https://mlcommons.org/croissant/bio/0.2/context",
            "name": "Test Dataset",
            "recordSet": [{
                "name": "PERSON",
                "omop:cdmTable": "PERSON",
                "field": [
                    {
                        "name": "person_id",
                        "omop:cdmField": "person_id",
                        "omop:isPrimaryKey": True,
                        "source": {"fileObject": {"@id": "person_csv"}}
                    },
                    {
                        "name": "gender_concept_id",
                        "omop:cdmField": "gender_concept_id",
                        "source": {"fileObject": {"@id": "person_csv"}}
                    },
                    {
                        "name": "year_of_birth",
                        "omop:cdmField": "year_of_birth",
                        "source": {"fileObject": {"@id": "person_csv"}}
                    },
                    {
                        "name": "race_concept_id",
                        "omop:cdmField": "race_concept_id",
                        "source": {"fileObject": {"@id": "person_csv"}}
                    },
                    {
                        "name": "ethnicity_concept_id",
                        "omop:cdmField": "ethnicity_concept_id",
                        "source": {"fileObject": {"@id": "person_csv"}}
                    }
                ]
            }],
            "distribution": [{
                "@id": "person_csv",
                "contentUrl": str(self.test_csv),
                "encodingFormat": "text/csv"
            }]
        }
        with open(self.test_metadata_path, 'w') as f:
            json.dump(metadata, f)

        self.converter = BioCroissantToOMOPConverter()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_convert_to_csv(self):
        """Test converting Bio-Croissant to OMOP CSV files."""
        output_dir = Path(self.temp_dir) / "omop_output"
        output_dir.mkdir()

        result = self.converter.convert(
            self.test_metadata_path,
            output_dir,
            output_format='csv'
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['tables_converted'], 1)

        # Check output file exists
        output_file = output_dir / "PERSON.csv"
        self.assertTrue(output_file.exists())

    def test_convert_with_validation(self):
        """Test conversion with validation enabled."""
        output_dir = Path(self.temp_dir) / "omop_output"
        output_dir.mkdir()

        result = self.converter.convert(
            self.test_metadata_path,
            output_dir,
            validate=True
        )

        self.assertTrue(result['success'])
        self.assertIn('validation_results', result)


if __name__ == '__main__':
    unittest.main()
