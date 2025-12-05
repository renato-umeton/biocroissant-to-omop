#!/usr/bin/env python3
"""Validate Bio-Croissant example files against the v0.2 JSON Schema."""

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
    print(f"\nValidating {example_path.name}...")

    try:
        example = load_json(example_path)
        schema = load_json(schema_path)

        # Use Draft 2020-12 validator (as specified in schema)
        validator = Draft202012Validator(schema)

        # Validate
        validator.validate(example)

        print(f"✓ {example_path.name} is valid")
        return True

    except ValidationError as e:
        print(f"✗ {example_path.name} validation failed:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        if e.schema_path:
            print(f"  Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
        return False

    except Exception as e:
        print(f"✗ {example_path.name} validation failed with exception:")
        print(f"  {type(e).__name__}: {e}")
        return False

def main():
    """Main validation function."""
    base_path = Path(__file__).parent
    schema_path = base_path / "schema" / "biocroissant-v0.2-schema.json"
    examples_path = base_path / "examples"

    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

    # Example files to validate
    example_files = [
        "omop_cdm_synthetic.json",
        "microscopy_ome_zarr.json",
        "digital_pathology_wsi.json"
    ]

    print("=" * 60)
    print("Bio-Croissant v0.2 Example Validation")
    print("=" * 60)

    results = []
    for example_file in example_files:
        example_path = examples_path / example_file
        if not example_path.exists():
            print(f"\n✗ {example_file} not found")
            results.append(False)
        else:
            results.append(validate_file(example_path, schema_path))

    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("✓ All examples are valid!")
        sys.exit(0)
    else:
        print("✗ Some examples failed validation")
        sys.exit(1)

if __name__ == "__main__":
    main()
