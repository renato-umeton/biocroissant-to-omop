#!/usr/bin/env python3
"""Validate generated synthetic datasets."""

import sys
from pathlib import Path
import json
from jsonschema import validate, ValidationError, Draft202012Validator

def load_json(file_path):
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

        validator = Draft202012Validator(schema)
        validator.validate(example)

        print(f"✓ Schema validation passed")

        # Check ISO 11179 metadata
        if 'iso11179:steward' in example:
            steward = example.get('iso11179:steward', {})
            print(f"  ✓ Steward: {steward.get('name', 'N/A')}")

        if 'iso11179:registrationStatus' in example:
            print(f"  ✓ Registration Status: {example.get('iso11179:registrationStatus')}")

        print(f"\n✓ {example_path.name} is valid!\n")
        return True

    except ValidationError as e:
        print(f"✗ Schema validation failed:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        return False

    except Exception as e:
        print(f"✗ Validation failed: {type(e).__name__}: {e}")
        return False

def main():
    base_path = Path(__file__).parent.parent
    schema_v03 = base_path / "schema" / "definitions" / "biocroissant-v0.3-schema.json"
    generated_v03 = base_path / "data" / "metadata" / "synthetic_dataset_v0.3.json"

    print("\n" + "="*70)
    print("Validating Generated Synthetic Datasets")
    print("="*70)

    results = []

    # Validate v0.3 generated metadata
    if generated_v03.exists() and schema_v03.exists():
        results.append(validate_file(generated_v03, schema_v03))
    else:
        print(f"\n✗ Missing files for validation")
        results.append(False)

    # Summary
    print("\n" + "="*70)
    print("Validation Summary")
    print("="*70)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All generated datasets are valid!")
        sys.exit(0)
    else:
        print("\n✗ Some validations failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
