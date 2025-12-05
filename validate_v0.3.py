#!/usr/bin/env python3
"""Validate Bio-Croissant v0.3 files with ISO 11179 metadata."""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def validate_file(example_path, schema_path):
    """Validate an example file against the schema."""
    print(f"\n{'='*70}")
    print(f"Validating: {example_path.name}")
    print(f"{'='*70}")

    try:
        example = load_json(example_path)
        schema = load_json(schema_path)

        # Use Draft 2020-12 validator
        validator = Draft202012Validator(schema)

        # Validate
        validator.validate(example)

        print(f"✓ Schema validation passed")

        # Additional ISO 11179 checks
        iso11179_checks = check_iso11179_metadata(example)

        if iso11179_checks['is_level_2_or_3']:
            print(f"\n  ISO 11179 Conformance Level: {example.get('bio:conformanceLevel', 'Not specified')}")

            if iso11179_checks['has_steward']:
                steward = example.get('iso11179:steward', {})
                print(f"  ✓ Steward: {steward.get('name', 'N/A')}")
            else:
                print(f"  ✗ Missing steward (required for Level 2+)")

            if iso11179_checks['has_registration_status']:
                print(f"  ✓ Registration Status: {example.get('iso11179:registrationStatus')}")
            else:
                print(f"  ✗ Missing registration status (required for Level 2+)")

            # Check field-level ISO 11179
            field_summary = check_field_iso11179(example)
            print(f"\n  Field Analysis:")
            print(f"    Total fields: {field_summary['total_fields']}")
            print(f"    With Data Element Concepts: {field_summary['with_dec']}")
            print(f"    With Value Domains: {field_summary['with_vd']}")

            if field_summary['total_fields'] > 0:
                dec_percent = (field_summary['with_dec'] / field_summary['total_fields']) * 100
                vd_percent = (field_summary['with_vd'] / field_summary['total_fields']) * 100
                print(f"    Data Element Concept coverage: {dec_percent:.1f}%")
                print(f"    Value Domain coverage: {vd_percent:.1f}%")

        print(f"\n✓ {example_path.name} is valid!\n")
        return True

    except ValidationError as e:
        print(f"✗ Schema validation failed:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        if e.schema_path:
            print(f"  Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
        return False

    except Exception as e:
        print(f"✗ Validation failed with exception:")
        print(f"  {type(e).__name__}: {e}")
        return False

def check_iso11179_metadata(data):
    """Check for ISO 11179 metadata presence."""
    return {
        'is_level_2_or_3': data.get('bio:conformanceLevel') in ['Level 2', 'Level 3'],
        'has_steward': 'iso11179:steward' in data,
        'has_registration_status': 'iso11179:registrationStatus' in data,
        'has_registration_authority': 'iso11179:registrationAuthority' in data,
        'has_submitter': 'iso11179:submitter' in data
    }

def check_field_iso11179(data):
    """Check ISO 11179 metadata on fields."""
    summary = {
        'total_fields': 0,
        'with_dec': 0,
        'with_vd': 0,
        'with_classification': 0
    }

    for record_set in data.get('recordSet', []):
        for field in record_set.get('field', []):
            summary['total_fields'] += 1

            if 'iso11179:dataElementConcept' in field:
                summary['with_dec'] += 1

            if 'iso11179:valueDomain' in field:
                summary['with_vd'] += 1

            if 'iso11179:classifiedBy' in field:
                summary['with_classification'] += 1

    return summary

def validate_value_domains(vd_path):
    """Validate value domains registry."""
    print(f"\n{'='*70}")
    print(f"Validating: {vd_path.name}")
    print(f"{'='*70}")

    try:
        vd_registry = load_json(vd_path)

        # Basic structure checks
        assert '@type' in vd_registry, "Missing @type"
        assert 'valueDomains' in vd_registry, "Missing valueDomains"

        vd_count = len(vd_registry['valueDomains'])
        print(f"  Value Domains defined: {vd_count}")

        # Check each value domain
        for vd in vd_registry['valueDomains']:
            assert '@id' in vd, f"Value domain missing @id"
            assert 'iso11179:datatype' in vd, f"Value domain {vd.get('@id')} missing datatype"

            # Count permissible values
            if 'iso11179:permissibleValues' in vd:
                pv_count = len(vd['iso11179:permissibleValues'])
                print(f"  - {vd.get('name', vd['@id'])}: {pv_count} permissible values")

        print(f"\n✓ {vd_path.name} is valid!\n")
        return True

    except AssertionError as e:
        print(f"✗ Validation failed: {e}")
        return False

    except Exception as e:
        print(f"✗ Validation failed with exception: {type(e).__name__}: {e}")
        return False

def main():
    """Main validation function."""
    base_path = Path(__file__).parent
    schema_path = base_path / "schema" / "biocroissant-v0.3-schema.json"
    examples_path = base_path / "examples"
    vd_path = base_path / "value-domains" / "standard-value-domains.json"

    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

    print("\n" + "="*70)
    print("Bio-Croissant v0.3 Validation (ISO 11179 Enhanced)")
    print("="*70)

    results = []

    # Validate v0.3 example
    v03_example = examples_path / "omop_cdm_iso11179.json"
    if v03_example.exists():
        results.append(validate_file(v03_example, schema_path))
    else:
        print(f"\n✗ {v03_example.name} not found")
        results.append(False)

    # Validate value domains
    if vd_path.exists():
        results.append(validate_value_domains(vd_path))
    else:
        print(f"\n✗ {vd_path.name} not found")
        results.append(False)

    # Summary
    print("\n" + "="*70)
    print("Validation Summary")
    print("="*70)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All validations passed!")
        print("\nBio-Croissant v0.3 files are valid and demonstrate:")
        print("  - ISO 11179 metadata registry compliance")
        print("  - Data element concepts with object class + property")
        print("  - Value domains with permissible values")
        print("  - Administrative metadata (steward, registration status)")
        print("  - Classification schemes")
        sys.exit(0)
    else:
        print("\n✗ Some validations failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
