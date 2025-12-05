# Bio-Croissant Examples

This directory contains example Bio-Croissant metadata files demonstrating the specification in practice.

## Example Files

### 1. OMOP CDM Synthetic Dataset (v0.2)
**File:** `omop_cdm_synthetic.json`

Demonstrates:
- OMOP CDM v5.4 table representations
- Clinical data RecordSets (PERSON, CONDITION_OCCURRENCE, DRUG_EXPOSURE, CONCEPT)
- Foreign key relationships between clinical tables
- Concept ID fields with vocabulary references
- Synthetic/de-identified data declarations
- OMOP-specific metadata properties

**Key Features:**
- Dataset-level OMOP CDM version and vocabulary declarations
- Table-level distribution key specifications
- Field-level foreign key and concept domain mappings
- Proper relationship modeling between patient events and vocabulary tables

### 2. OMOP CDM with ISO 11179 Metadata (v0.3)
**File:** `omop_cdm_iso11179.json`

Demonstrates:
- **ISO 11179 metadata registry** features
- **Data element concepts** (object class + property)
- **Value domains** with permissible values
- **Administrative metadata** (steward, registration status)
- **Conceptual domains** for semantic meanings
- **Classification schemes** for organizing metadata
- Level 3 conformance with complete ISO 11179 metadata

**Key Features:**
- Registration authority and steward attribution
- Data element concepts for all fields (e.g., Person.GenderAtBirth)
- Value domains with controlled vocabularies (e.g., OMOP Gender concept IDs)
- Detailed definitions following ISO 11179-4 principles
- Classification scheme membership (Demographics, Clinical Events)
- Deidentification notes on synthetic data

**Example Data Element Concept:**
```json
{
  "iso11179:dataElementConcept": {
    "@id": "dec:Person.GenderAtBirth",
    "iso11179:objectClass": "Person",
    "iso11179:property": "Gender at Birth",
    "iso11179:definition": "The biological sex of a person as determined or assumed at birth"
  }
}
```

### 3. Microscopy with OME-Zarr (v0.2)
**File:** `microscopy_ome_zarr.json`

Demonstrates:
- Multi-dimensional array imaging data (5D: TCZYX)
- OME-Zarr format integration
- Multi-channel fluorescence microscopy
- Segmentation masks as separate RecordSets
- Single-cell measurements linked to images
- Physical dimension specifications (micrometers, timepoints)

**Key Features:**
- Detailed dimensional metadata for 5D microscopy data
- Channel-specific properties (names, colors, wavelengths)
- Integration of image data, segmentation masks, and quantitative measurements
- OME-Zarr specific properties and extraction paths

### 4. Digital Pathology Whole Slide Images (v0.2)
**File:** `digital_pathology_wsi.json`

Demonstrates:
- Whole slide imaging (WSI) with multi-resolution pyramids
- H&E stained tissue sections
- Pathologist polygon annotations in GeoJSON format
- Tile extraction manifests for patch-based training
- Clinical metadata integration (tumor grade, receptor status)
- Authenticated access and data access committee information

**Key Features:**
- WSI-specific technical metadata (magnification, MPP, pyramid levels)
- Spatial annotations with different tissue classes
- Pre-computed tile locations for ML training
- De-identification and access control specifications
- Integration with clinical pathology metadata

## Validating Examples

To validate these examples against the Bio-Croissant specification:

```bash
# Using a JSON-LD validator
jsonld validate omop_cdm_synthetic.json

# Check conformance to Croissant schema
croissant validate omop_cdm_synthetic.json
```

## Using Examples

These examples can serve as templates for creating your own Bio-Croissant metadata files:

1. Copy the relevant example file
2. Update dataset-level metadata (name, description, creators, etc.)
3. Modify distribution to point to your actual data files
4. Adjust RecordSets and Fields to match your data structure
5. Add domain-specific properties as needed

## Common Patterns

### OMOP Pattern
```json
{
  "omop:cdmTable": "TABLE_NAME",
  "omop:tableDomain": "Clinical|Vocabulary|...",
  "omop:distributionKey": "person_id|RANDOM",
  "field": [
    {
      "omop:cdmField": "field_name",
      "omop:foreignKeyTable": "REFERENCED_TABLE"
    }
  ]
}
```

### Imaging Pattern
```json
{
  "dataType": "bioimg:MultiDimensionalArray",
  "bioimg:dimensions": { "T": 10, "C": 4, "Z": 50, "Y": 1024, "X": 1024 },
  "bioimg:dimensionOrder": "TCZYX",
  "bioimg:physicalSizeX": 0.065,
  "bioimg:physicalSizeUnit": "micrometer"
}
```

### WSI Pattern
```json
{
  "dataType": "wsi:WholeSlideImage",
  "wsi:pyramidLevels": 8,
  "wsi:baseMagnification": 40,
  "wsi:mppX": 0.25,
  "wsi:mppY": 0.25
}
```

## Contributing Examples

To contribute additional examples:

1. Create a new JSON file following the Bio-Croissant specification
2. Ensure all required fields are present
3. Validate against the schema
4. Add documentation to this README
5. Submit via pull request

## Bio-Croissant Versions

### v0.3 (Latest - ISO 11179 Enhanced)
Bio-Croissant v0.3 adds **ISO/IEC 11179 metadata registry** capabilities for standardized data governance:

- **Data element concepts** separating semantics from representation
- **Value domains** with controlled vocabularies
- **Administrative metadata** (steward, registration authority, lifecycle status)
- **Conceptual domains** for vendor-neutral value meanings
- **Classification schemes** for organizing biomedical metadata
- **Three conformance levels** (Basic, Enhanced, Full Registry)

**When to use v0.3:**
- You need formal data governance and stewardship
- Your dataset requires controlled vocabularies
- You want semantic interoperability with ISO 11179 registries
- You need clear separation between meaning and representation

### v0.2 (Stable)
Bio-Croissant v0.2 provides comprehensive biomedical metadata without ISO 11179:

- Core Bio-Croissant properties (data category, deidentification, quality metrics)
- OMOP CDM, bioimaging, and WSI extensions
- Conditional requirements based on data type
- Complete JSON-LD context and JSON Schema

**When to use v0.2:**
- You need stable, production-ready biomedical metadata
- ISO 11179 governance features are not required
- You want simpler metadata without registry overhead

**Migration:** v0.3 is fully backward compatible with v0.2. Simply update namespace versions.

## Resources

### v0.3 Resources
- [Bio-Croissant Specification v0.3](../BIO_CROISSANT_SPECIFICATION_v0.3.md)
- [JSON Schema v0.3](../schema/biocroissant-v0.3-schema.json)
- [JSON-LD Context v0.3](../context/biocroissant-v0.3-context.jsonld)
- [Standard Value Domains](../value-domains/standard-value-domains.json)
- [v0.3 Revision Summary](../REVISION_SUMMARY_v0.3.md)

### v0.2 Resources
- [Bio-Croissant Specification v0.2](../BIO_CROISSANT_SPECIFICATION_v0.2.md)
- [JSON Schema v0.2](../schema/biocroissant-v0.2-schema.json)
- [JSON-LD Context v0.2](../context/biocroissant-v0.2-context.jsonld)
- [v0.2 Revision Summary](../REVISION_SUMMARY_v0.2.md)

### External Resources
- [Croissant Format Documentation](https://docs.mlcommons.org/croissant/)
- [OMOP CDM Documentation](https://ohdsi.github.io/CommonDataModel/)
- [OME Data Model](https://www.openmicroscopy.org/)
- [ISO/IEC 11179 Framework](https://www.iso.org/standard/78914.html)
