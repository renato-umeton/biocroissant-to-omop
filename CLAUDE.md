# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BioCromop (Bio-Croissant OMOP) is a project focused on creating a Croissant metadata format specification for OMOP CDM (Observational Medical Outcomes Partnership Common Data Model) healthcare datasets. The Croissant format is a standardized high-level format for machine learning datasets that combines metadata, resource descriptions, data structure, and ML semantics into a single file.

This project bridges two important healthcare/ML standards:
- OMOP CDM v5.4: A standardized healthcare data model for observational databases
- Croissant: An ML dataset metadata format built on schema.org standards

## Key Resources in This Repository

### Project Structure

```
biocromop/
├── src/                    # Source code
│   ├── biocroissant_to_omop.py      # Bio-Croissant → OMOP CDM converter
│   └── generate_synthetic_dataset.py # Synthetic OMOP data generator
├── tests/                  # Test suite (16 tests, 100% passing)
├── scripts/                # Validation utilities
├── docs/                   # Documentation
│   ├── specifications/     # Bio-Croissant specs (v0.1, v0.2, v0.3)
│   ├── guides/            # Implementation guides
│   ├── examples/          # Bio-Croissant example files
│   ├── Croissant specs 1.0/    # MLCommons Croissant reference specs
│   └── OMOP CDM specs 5.4/     # OMOP CDM reference documentation
├── data/                   # Generated synthetic data and metadata
├── schema/                 # JSON-LD contexts, JSON Schemas, value domains
└── README.md              # Project documentation
```

### Bio-Croissant Specifications

- `docs/specifications/BIO_CROISSANT_SPECIFICATION.md` - v0.1 specification
- `docs/specifications/BIO_CROISSANT_SPECIFICATION_v0.2.md` - v0.2 with quality metrics and foreign keys
- `docs/specifications/BIO_CROISSANT_SPECIFICATION_v0.3.md` - v0.3 with ISO 11179 metadata registry
  - Extends MLCommons Croissant for biomedical/healthcare datasets
  - OMOP CDM v5.4 support with clinical data patterns
  - ISO 11179 data element concepts and value domains
  - Bioimaging extensions for microscopy and OME-Zarr
  - Whole slide imaging (WSI) support for digital pathology
  - Security, privacy, and de-identification requirements
  - BioSchemas alignment for semantic interoperability

### Bio-Croissant Examples

- `docs/examples/` - Example Bio-Croissant metadata files:
  - `omop_cdm_synthetic.json` - Synthetic OMOP CDM dataset (v0.2)
  - `omop_cdm_iso11179.json` - OMOP with ISO 11179 metadata (v0.3)
  - `microscopy_ome_zarr.json` - Multi-channel fluorescence microscopy
  - `digital_pathology_wsi.json` - Breast cancer whole slide images
  - `README.md` - Examples documentation and usage patterns

### Reference Specifications (External)

- `docs/Croissant specs 1.0/` - MLCommons Croissant reference documentation:
  - Croissant Format Specification (HTML)
  - Croissant RAI Specification (HTML)
- `docs/OMOP CDM specs 5.4/` - OMOP CDM v5.4 reference materials:
  - OMOP Common Data Model documentation (HTML)
  - SQL DDL files (PostgreSQL): ddl, primary keys, indices, constraints
  - CSV field/table level specifications
  - Oncology extension metadata

### Generated Data

- `data/generated/` - Synthetic OMOP CDM data (1,000 patients, 3,043 conditions)
- `data/metadata/` - Bio-Croissant metadata files (v0.2 and v0.3)

## OMOP CDM v5.4 Architecture

The OMOP CDM organizes healthcare data into several categories:

### Clinical Data Tables (Person-Centric)
Tables distributed on `person_id` for optimal query performance:
- `PERSON` - Demographics and basic patient information
- `OBSERVATION_PERIOD` - Time periods when patient data is observed
- `VISIT_OCCURRENCE` / `VISIT_DETAIL` - Healthcare visits and encounters
- `CONDITION_OCCURRENCE` - Diagnoses and conditions
- `DRUG_EXPOSURE` - Medication records
- `PROCEDURE_OCCURRENCE` - Medical procedures
- `DEVICE_EXPOSURE` - Medical devices used
- `MEASUREMENT` - Laboratory tests and vital signs
- `OBSERVATION` - Clinical facts not captured elsewhere
- `NOTE` - Clinical notes and documentation
- `SPECIMEN` - Biological specimens
- `DEATH` - Death records

### Health System Tables
Tables distributed randomly:
- `LOCATION` - Geographic locations
- `CARE_SITE` - Healthcare facilities
- `PROVIDER` - Healthcare providers

### Health Economics Tables
- `PAYER_PLAN_PERIOD` - Insurance coverage periods (person-centric)
- `COST` - Healthcare costs (distributed randomly)

### Derived Tables
- `DRUG_ERA` / `DOSE_ERA` - Continuous drug exposure periods
- `CONDITION_ERA` - Continuous condition periods
- `EPISODE` / `EPISODE_EVENT` - Clinical episodes

### Vocabulary/Metadata Tables
Standardized terminologies and concepts:
- `CONCEPT` - Standard vocabulary concepts
- `VOCABULARY` - Vocabulary metadata
- `DOMAIN` - Domain classifications
- `CONCEPT_CLASS` - Concept classifications
- `CONCEPT_RELATIONSHIP` - Relationships between concepts
- `RELATIONSHIP` - Relationship type definitions
- `CONCEPT_SYNONYM` - Alternative concept names
- `CONCEPT_ANCESTOR` - Hierarchical concept relationships
- `SOURCE_TO_CONCEPT_MAP` - Source to standard concept mappings
- `DRUG_STRENGTH` - Drug ingredient information

### Analysis Support Tables
- `COHORT` / `COHORT_DEFINITION` - Patient cohorts for analysis
- `FACT_RELATIONSHIP` - Cross-domain relationships
- `METADATA` - CDM instance metadata
- `CDM_SOURCE` - Source database information
- `NOTE_NLP` - NLP-extracted information from notes

## Python Environment

### Setup
```bash
pipenv install --dev   # Install dependencies including dev tools
pipenv shell           # Activate virtual environment
```

### Requirements
- Python 3.14
- Dependencies defined in Pipfile:
  - **Runtime:** faker, pandas, numpy, jsonschema
  - **Development:** pytest
  - **Optional:** ipykernel (for Jupyter notebook support)

### Running Tests
```bash
pipenv run python -m pytest tests/ -v    # Run all tests (16 tests)
pipenv run python3 scripts/validate_examples.py      # Validate v0.2 examples
pipenv run python3 scripts/validate_v0.3.py          # Validate v0.3 examples
pipenv run python3 scripts/validate_generated.py     # Validate generated data
```

### Generating Synthetic Data
```bash
pipenv run python3 src/generate_synthetic_dataset.py
# Outputs:
#   data/generated/person.csv (1,000 patients)
#   data/generated/condition_occurrence.csv (3,043 conditions)
#   data/metadata/synthetic_dataset_v0.2.json
#   data/metadata/synthetic_dataset_v0.3.json
```

### Converting Bio-Croissant to OMOP CDM
```bash
pipenv run python3 src/biocroissant_to_omop.py \
  data/metadata/synthetic_dataset_v0.2.json \
  output_directory \
  --format both --dialect postgresql
```

## Key Concepts for Development

### OMOP Vocabulary System
All clinical concepts in OMOP CDM reference standardized vocabularies through `concept_id` fields. The vocabulary system enables:
- Standardized terminology across different source systems
- Hierarchical relationships between concepts
- Mapping from source codes to standard concepts

### Data Distribution Strategy
The SQL files include distribution hints:
- `HINT DISTRIBUTE ON KEY (person_id)` - Person-centric tables distributed by patient
- `HINT DISTRIBUTE ON RANDOM` - Reference/vocabulary tables distributed randomly

### Primary Design Pattern
- Each clinical event table has an `_id` field as primary key
- Most clinical tables reference `person_id` (foreign key to PERSON)
- Many clinical tables reference `visit_occurrence_id` to link to visits
- Concept fields (ending in `_concept_id`) reference the CONCEPT table
- Source value fields preserve original source data values

## Bio-Croissant Format Development

### Specification Structure

The Bio-Croissant specification (`BIO_CROISSANT_SPECIFICATION.md`) is organized into:

1. **Core Extensions** - Base Bio-Croissant vocabulary and data types
2. **Domain Extensions** - OMOP, Bioimaging, and WSI specific extensions
3. **Cross-cutting Concerns** - Security, privacy, BioSchemas alignment

### Key Namespaces

When working with Bio-Croissant metadata:

- `bio:` - Core Bio-Croissant vocabulary (`http://mlcommons.org/croissant/bio/`)
- `omop:` - OMOP CDM extensions (`http://mlcommons.org/croissant/bio/omop/`)
- `bioimg:` - Bioimaging extensions (`http://mlcommons.org/croissant/bio/imaging/`)
- `wsi:` - Whole slide imaging extensions (`http://mlcommons.org/croissant/bio/wsi/`)

### Creating Bio-Croissant Metadata

To create new Bio-Croissant metadata files:

1. Start with an example file from `examples/` directory
2. Ensure conformance declaration includes both Croissant and Bio-Croissant URIs
3. Use appropriate namespace prefixes for domain-specific properties
4. Include de-identification metadata for human subjects data
5. Reference vocabulary systems for clinical concepts
6. Validate against JSON-LD schema

### Common Patterns

**OMOP Clinical Table RecordSet:**
```json
{
  "@type": "cr:RecordSet",
  "omop:cdmTable": "TABLE_NAME",
  "omop:tableDomain": "Clinical",
  "omop:distributionKey": "person_id",
  "field": [
    {
      "dataType": "bio:ConceptID",
      "omop:foreignKeyTable": "CONCEPT",
      "omop:conceptDomain": "Drug|Condition|..."
    }
  ]
}
```

**Multi-Dimensional Imaging Field:**
```json
{
  "@type": "cr:Field",
  "dataType": "bioimg:MultiDimensionalArray",
  "bioimg:dimensions": { "T": 10, "C": 4, "Z": 50, "Y": 1024, "X": 1024 },
  "bioimg:dimensionOrder": "TCZYX",
  "bioimg:physicalSizeX": 0.065,
  "bioimg:physicalSizeUnit": "micrometer"
}
```

**Whole Slide Image Field:**
```json
{
  "@type": "cr:Field",
  "dataType": "wsi:WholeSlideImage",
  "wsi:pyramidLevels": 8,
  "wsi:baseMagnification": 40,
  "wsi:mppX": 0.25,
  "wsi:mppY": 0.25
}
```

### Validation Checklist

Before submitting Bio-Croissant metadata:

- [ ] Valid JSON-LD syntax
- [ ] Conforms to both Croissant 1.0 and Bio-Croissant 0.1
- [ ] De-identification method declared (for human data)
- [ ] Access control specified (if authenticated)
- [ ] Concept fields reference vocabularies with versions
- [ ] Foreign key relationships properly defined
- [ ] Physical units specified for imaging data
- [ ] File checksums provided (recommended)
