#!/usr/bin/env python3
"""Bio-Croissant to OMOP CDM converter.

Converts Bio-Croissant metadata and data files to OMOP Common Data Model format.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
from datetime import datetime


class BioCroissantParser:
    """Parse Bio-Croissant metadata."""

    def parse(self, metadata: Dict) -> Dict:
        """Parse Bio-Croissant metadata.

        Args:
            metadata: Bio-Croissant metadata dictionary

        Returns:
            Parsed metadata dictionary
        """
        return metadata

    def extract_recordsets(self, metadata: Dict) -> List[Dict]:
        """Extract recordSets from metadata.

        Args:
            metadata: Bio-Croissant metadata dictionary

        Returns:
            List of recordSet dictionaries
        """
        return metadata.get('recordSet', [])

    def extract_fields(self, recordset: Dict) -> List[Dict]:
        """Extract fields from a recordSet.

        Args:
            recordset: RecordSet dictionary

        Returns:
            List of field dictionaries
        """
        return recordset.get('field', [])

    def extract_distributions(self, metadata: Dict) -> List[Dict]:
        """Extract file distributions from metadata.

        Args:
            metadata: Bio-Croissant metadata dictionary

        Returns:
            List of distribution dictionaries
        """
        return metadata.get('distribution', [])

    def get_distribution_by_id(self, metadata: Dict, dist_id: str) -> Optional[Dict]:
        """Get distribution by @id reference.

        Args:
            metadata: Bio-Croissant metadata dictionary
            dist_id: Distribution @id to find

        Returns:
            Distribution dictionary or None
        """
        distributions = self.extract_distributions(metadata)
        for dist in distributions:
            if dist.get('@id') == dist_id:
                return dist
        return None


class OMOPTableMapper:
    """Map Bio-Croissant recordSets to OMOP CDM tables."""

    # OMOP CDM required fields by table
    REQUIRED_FIELDS = {
        'PERSON': ['person_id', 'gender_concept_id', 'year_of_birth', 'race_concept_id', 'ethnicity_concept_id'],
        'CONDITION_OCCURRENCE': ['condition_occurrence_id', 'person_id', 'condition_concept_id', 'condition_start_date', 'condition_type_concept_id'],
        'PROCEDURE_OCCURRENCE': ['procedure_occurrence_id', 'person_id', 'procedure_concept_id', 'procedure_date', 'procedure_type_concept_id'],
        'DRUG_EXPOSURE': ['drug_exposure_id', 'person_id', 'drug_concept_id', 'drug_exposure_start_date', 'drug_type_concept_id'],
        'VISIT_OCCURRENCE': ['visit_occurrence_id', 'person_id', 'visit_concept_id', 'visit_start_date', 'visit_type_concept_id'],
        'OBSERVATION': ['observation_id', 'person_id', 'observation_concept_id', 'observation_date', 'observation_type_concept_id']
    }

    def map_table(self, recordset: Dict) -> Dict:
        """Map a Bio-Croissant recordSet to an OMOP table.

        Args:
            recordset: RecordSet dictionary

        Returns:
            Mapping dictionary with omop_table and field_mappings
        """
        omop_table = recordset.get('omop:cdmTable') or recordset.get('name')
        fields = recordset.get('field', [])

        field_mappings = []
        for field in fields:
            field_mappings.append({
                'bio_field': field.get('name'),
                'omop_field': field.get('omop:cdmField', field.get('name')),
                'data_type': field.get('dataType'),
                'is_primary_key': field.get('omop:isPrimaryKey', False),
                'foreign_key_table': field.get('omop:foreignKeyTable')
            })

        return {
            'omop_table': omop_table,
            'field_mappings': field_mappings,
            'recordset_id': recordset.get('@id'),
            'description': recordset.get('description')
        }

    def identify_primary_key(self, fields: List[Dict]) -> Optional[str]:
        """Identify the primary key field.

        Args:
            fields: List of field dictionaries

        Returns:
            Primary key field name or None
        """
        for field in fields:
            if field.get('omop:isPrimaryKey'):
                return field.get('name')
        return None

    def identify_foreign_keys(self, fields: List[Dict]) -> List[Dict]:
        """Identify foreign key fields.

        Args:
            fields: List of field dictionaries

        Returns:
            List of foreign key dictionaries
        """
        foreign_keys = []
        for field in fields:
            fk_table = field.get('omop:foreignKeyTable')
            if fk_table:
                foreign_keys.append({
                    'field': field.get('name'),
                    'references_table': fk_table,
                    'references_field': field.get('references', {}).get('@id', '').split('/')[-1]
                })
        return foreign_keys

    def get_required_fields(self, table_name: str) -> List[str]:
        """Get required fields for an OMOP table.

        Args:
            table_name: OMOP table name

        Returns:
            List of required field names
        """
        return self.REQUIRED_FIELDS.get(table_name, [])


class DataExtractor:
    """Extract data from CSV files."""

    def read_csv(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file into DataFrame.

        Args:
            file_path: Path to CSV file

        Returns:
            DataFrame with CSV data
        """
        return pd.read_csv(file_path)

    def extract_from_distribution(self, distribution: Dict, base_path: Optional[Path] = None) -> pd.DataFrame:
        """Extract data from a file distribution.

        Args:
            distribution: Distribution dictionary
            base_path: Base path for relative URLs

        Returns:
            DataFrame with extracted data
        """
        content_url = distribution.get('contentUrl')
        if not content_url:
            raise ValueError(f"Distribution missing contentUrl: {distribution.get('@id')}")

        file_path = Path(content_url)
        if base_path and not file_path.is_absolute():
            file_path = base_path / file_path

        encoding_format = distribution.get('encodingFormat', 'text/csv')
        if 'csv' in encoding_format.lower():
            return self.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported encoding format: {encoding_format}")


class OMOPValidator:
    """Validate data against OMOP CDM constraints."""

    def __init__(self):
        self.mapper = OMOPTableMapper()

    def validate_table(self, table_name: str, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate table data against OMOP CDM constraints.

        Args:
            table_name: OMOP table name
            df: DataFrame with table data

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Validate required fields
        required_fields = self.mapper.get_required_fields(table_name)
        if required_fields:
            valid, field_errors = self.validate_required_fields(df, required_fields)
            if not valid:
                errors.extend(field_errors)

        # Validate primary key if this is a known table
        if table_name in self.mapper.REQUIRED_FIELDS:
            pk_field = f"{table_name.lower()}_id"
            if pk_field in df.columns:
                valid, pk_errors = self.validate_primary_key(df, pk_field)
                if not valid:
                    errors.extend(pk_errors)

        return len(errors) == 0, errors

    def validate_primary_key(self, df: pd.DataFrame, pk_field: str) -> Tuple[bool, List[str]]:
        """Validate primary key uniqueness.

        Args:
            df: DataFrame with table data
            pk_field: Primary key field name

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if pk_field not in df.columns:
            errors.append(f"Primary key field '{pk_field}' not found")
            return False, errors

        # Check for nulls
        if df[pk_field].isnull().any():
            errors.append(f"Primary key '{pk_field}' contains null values")

        # Check for duplicates
        if df[pk_field].duplicated().any():
            duplicate_count = df[pk_field].duplicated().sum()
            errors.append(f"Primary key '{pk_field}' contains {duplicate_count} duplicate values")

        return len(errors) == 0, errors

    def validate_required_fields(self, df: pd.DataFrame, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Validate that required fields are present.

        Args:
            df: DataFrame with table data
            required_fields: List of required field names

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        missing_fields = [field for field in required_fields if field not in df.columns]

        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")

        return len(errors) == 0, errors

    def validate_foreign_keys(self, df: pd.DataFrame, fk_field: str, ref_table_df: pd.DataFrame, ref_field: str) -> Tuple[bool, List[str]]:
        """Validate foreign key references.

        Args:
            df: DataFrame with table data
            fk_field: Foreign key field name
            ref_table_df: Referenced table DataFrame
            ref_field: Referenced field name

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if fk_field not in df.columns:
            errors.append(f"Foreign key field '{fk_field}' not found")
            return False, errors

        if ref_field not in ref_table_df.columns:
            errors.append(f"Referenced field '{ref_field}' not found in referenced table")
            return False, errors

        # Check for orphaned records
        fk_values = df[fk_field].dropna().unique()
        ref_values = ref_table_df[ref_field].unique()
        orphaned = set(fk_values) - set(ref_values)

        if orphaned:
            errors.append(f"Foreign key '{fk_field}' has {len(orphaned)} orphaned references")

        return len(errors) == 0, errors


class OMOPExporter:
    """Export data to OMOP CDM format."""

    OMOP_DATA_TYPES = {
        'sc:Integer': 'INTEGER',
        'sc:Float': 'FLOAT',
        'sc:Text': 'VARCHAR(255)',
        'sc:Date': 'DATE',
        'sc:DateTime': 'TIMESTAMP',
        'sc:Boolean': 'BOOLEAN'
    }

    def export_csv(self, table_name: str, df: pd.DataFrame, output_path: Path) -> None:
        """Export table to CSV file.

        Args:
            table_name: OMOP table name
            df: DataFrame with table data
            output_path: Output file path
        """
        df.to_csv(output_path, index=False)

    def generate_ddl(self, table_schema: Dict, dialect: str = 'postgresql') -> str:
        """Generate SQL DDL for table creation.

        Args:
            table_schema: Table schema dictionary
            dialect: SQL dialect (postgresql, mysql, sqlite)

        Returns:
            SQL DDL statement
        """
        table_name = table_schema['table_name']
        fields = table_schema['fields']

        ddl = f"CREATE TABLE {table_name} (\n"

        field_definitions = []
        primary_keys = []

        for field in fields:
            field_name = field['name']
            field_type = field['type']
            is_nullable = field.get('nullable', True)
            is_pk = field.get('primary_key', False)

            field_def = f"  {field_name} {field_type}"
            if not is_nullable:
                field_def += " NOT NULL"

            field_definitions.append(field_def)

            if is_pk:
                primary_keys.append(field_name)

        ddl += ",\n".join(field_definitions)

        if primary_keys:
            ddl += f",\n  PRIMARY KEY ({', '.join(primary_keys)})"

        ddl += "\n);"

        return ddl

    def generate_insert_statements(self, table_name: str, df: pd.DataFrame, batch_size: int = 100) -> List[str]:
        """Generate SQL INSERT statements.

        Args:
            table_name: OMOP table name
            df: DataFrame with table data
            batch_size: Number of rows per INSERT statement

        Returns:
            List of SQL INSERT statements
        """
        statements = []
        columns = ', '.join(df.columns)

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            values = []

            for _, row in batch.iterrows():
                row_values = []
                for val in row:
                    if pd.isna(val):
                        row_values.append('NULL')
                    elif isinstance(val, str):
                        row_values.append(f"'{val.replace('\'', '\'\'')}'")
                    else:
                        row_values.append(str(val))
                values.append(f"({', '.join(row_values)})")

            insert = f"INSERT INTO {table_name} ({columns}) VALUES\n  "
            insert += ",\n  ".join(values)
            insert += ";"
            statements.append(insert)

        return statements

    def map_datatype(self, bio_datatype: str) -> str:
        """Map Bio-Croissant datatype to SQL datatype.

        Args:
            bio_datatype: Bio-Croissant datatype

        Returns:
            SQL datatype
        """
        return self.OMOP_DATA_TYPES.get(bio_datatype, 'VARCHAR(255)')


class BioCroissantToOMOPConverter:
    """Main converter class for Bio-Croissant to OMOP CDM."""

    def __init__(self):
        self.parser = BioCroissantParser()
        self.mapper = OMOPTableMapper()
        self.extractor = DataExtractor()
        self.validator = OMOPValidator()
        self.exporter = OMOPExporter()

    def convert(
        self,
        metadata_path: Path,
        output_dir: Path,
        output_format: str = 'csv',
        validate: bool = True,
        sql_dialect: str = 'postgresql',
        base_path: Optional[Path] = None
    ) -> Dict:
        """Convert Bio-Croissant dataset to OMOP CDM format.

        Args:
            metadata_path: Path to Bio-Croissant metadata JSON file
            output_dir: Directory for output files
            output_format: Output format ('csv', 'sql', or 'both')
            validate: Whether to validate data against OMOP constraints
            sql_dialect: SQL dialect for DDL generation
            base_path: Base path for resolving relative file URLs (default: cwd)

        Returns:
            Result dictionary with conversion status
        """
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Use provided base path or current working directory for relative URLs
        if base_path is None:
            base_path = Path.cwd()

        # Parse metadata
        parsed = self.parser.parse(metadata)
        recordsets = self.parser.extract_recordsets(parsed)

        results = {
            'success': True,
            'tables_converted': 0,
            'tables': {},
            'validation_results': {},
            'errors': []
        }

        # Process each recordSet
        for recordset in recordsets:
            table_mapping = self.mapper.map_table(recordset)
            omop_table = table_mapping['omop_table']

            try:
                # Find data file
                df = self._extract_table_data(metadata, recordset, base_path)

                # Validate if requested
                if validate:
                    is_valid, errors = self.validator.validate_table(omop_table, df)
                    results['validation_results'][omop_table] = {
                        'valid': is_valid,
                        'errors': errors
                    }
                    if not is_valid:
                        results['errors'].append(f"Validation failed for {omop_table}: {errors}")

                # Export data
                if output_format in ['csv', 'both']:
                    csv_path = output_dir / f"{omop_table}.csv"
                    self.exporter.export_csv(omop_table, df, csv_path)

                if output_format in ['sql', 'both']:
                    # Generate DDL
                    table_schema = self._create_table_schema(table_mapping, df)
                    ddl = self.exporter.generate_ddl(table_schema, sql_dialect)

                    ddl_path = output_dir / f"{omop_table}_ddl.sql"
                    with open(ddl_path, 'w') as f:
                        f.write(ddl)

                    # Generate INSERT statements
                    inserts = self.exporter.generate_insert_statements(omop_table, df)
                    insert_path = output_dir / f"{omop_table}_data.sql"
                    with open(insert_path, 'w') as f:
                        f.write('\n\n'.join(inserts))

                results['tables_converted'] += 1
                results['tables'][omop_table] = {
                    'rows': len(df),
                    'columns': len(df.columns)
                }

            except Exception as e:
                results['success'] = False
                results['errors'].append(f"Error processing {omop_table}: {str(e)}")

        return results

    def _extract_table_data(self, metadata: Dict, recordset: Dict, base_path: Path) -> pd.DataFrame:
        """Extract data for a recordSet.

        Args:
            metadata: Bio-Croissant metadata
            recordset: RecordSet dictionary
            base_path: Base path for relative file paths

        Returns:
            DataFrame with table data
        """
        # Find the distribution referenced by this recordSet
        fields = recordset.get('field', [])
        if not fields:
            raise ValueError(f"RecordSet {recordset.get('name')} has no fields")

        # Get source reference from first field
        first_field = fields[0]
        source = first_field.get('source', {})
        file_obj = source.get('fileObject', {})
        dist_id = file_obj.get('@id')

        if not dist_id:
            raise ValueError(f"No distribution reference found for {recordset.get('name')}")

        # Get distribution
        distribution = self.parser.get_distribution_by_id(metadata, dist_id)
        if not distribution:
            raise ValueError(f"Distribution {dist_id} not found")

        # Extract data
        return self.extractor.extract_from_distribution(distribution, base_path)

    def _create_table_schema(self, table_mapping: Dict, df: pd.DataFrame) -> Dict:
        """Create table schema for DDL generation.

        Args:
            table_mapping: Table mapping dictionary
            df: DataFrame with table data

        Returns:
            Table schema dictionary
        """
        fields = []
        for field_map in table_mapping['field_mappings']:
            omop_field = field_map['omop_field']
            bio_datatype = field_map.get('data_type', 'sc:Text')

            # Infer SQL type from pandas dtype if bio_datatype not available
            if omop_field in df.columns:
                pandas_dtype = df[omop_field].dtype
                if pandas_dtype == 'int64':
                    sql_type = 'INTEGER'
                elif pandas_dtype == 'float64':
                    sql_type = 'FLOAT'
                elif pandas_dtype == 'bool':
                    sql_type = 'BOOLEAN'
                else:
                    sql_type = self.exporter.map_datatype(bio_datatype)
            else:
                sql_type = self.exporter.map_datatype(bio_datatype)

            fields.append({
                'name': omop_field,
                'type': sql_type,
                'primary_key': field_map.get('is_primary_key', False),
                'nullable': not field_map.get('is_primary_key', False)
            })

        return {
            'table_name': table_mapping['omop_table'],
            'fields': fields
        }


def main():
    """Command-line interface for converter."""
    import argparse

    parser = argparse.ArgumentParser(description='Convert Bio-Croissant to OMOP CDM format')
    parser.add_argument('metadata', type=Path, help='Path to Bio-Croissant metadata JSON')
    parser.add_argument('output_dir', type=Path, help='Output directory')
    parser.add_argument('--format', choices=['csv', 'sql', 'both'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--no-validate', action='store_true',
                        help='Skip validation')
    parser.add_argument('--dialect', choices=['postgresql', 'mysql', 'sqlite'], default='postgresql',
                        help='SQL dialect for DDL generation (default: postgresql)')

    args = parser.parse_args()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Run conversion
    converter = BioCroissantToOMOPConverter()
    result = converter.convert(
        args.metadata,
        args.output_dir,
        output_format=args.format,
        validate=not args.no_validate,
        sql_dialect=args.dialect
    )

    # Print results
    print(f"\nConversion {'succeeded' if result['success'] else 'failed'}")
    print(f"Tables converted: {result['tables_converted']}")

    if result['validation_results']:
        print("\nValidation Results:")
        for table, val_result in result['validation_results'].items():
            status = "✓" if val_result['valid'] else "✗"
            print(f"  {status} {table}")
            if val_result['errors']:
                for error in val_result['errors']:
                    print(f"      - {error}")

    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  - {error}")


if __name__ == '__main__':
    main()
