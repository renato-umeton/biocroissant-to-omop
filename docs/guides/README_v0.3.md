# Bio-Croissant v0.3 - ISO 11179 Metadata Registry Edition

**Version:** 0.3
**Release Date:** 2025-12-04
**Status:** Ready for Community Input

## Overview

Bio-Croissant v0.3 is a **metadata format for biomedical ML datasets** that extends MLCommons Croissant with **ISO/IEC 11179 metadata registry** capabilities. This enables standardized data governance, semantic clarity, and controlled vocabularies for healthcare and life sciences datasets.

## What's New in v0.3

### ISO 11179 Metadata Registry Support

Bio-Croissant v0.3 implements [ISO/IEC 11179](https://www.iso.org/standard/78914.html) international standards for metadata registries:

- **Data Element Concepts** - Separate semantic meaning (object class + property) from representation
- **Value Domains** - Controlled vocabularies with permissible values and datatypes
- **Conceptual Domains** - Vendor-neutral value meanings for interoperability
- **Administrative Metadata** - Data stewardship, registration authority, lifecycle management
- **Classification Schemes** - Hierarchical organization of biomedical metadata
- **Three Conformance Levels** - Flexible adoption from basic to full registry

### Key Benefits

**For Dataset Publishers:**
- Formal data governance with steward attribution
- Controlled vocabularies reduce data quality issues
- Standards-based metadata interoperability
- Clear semantic definitions following ISO 11179-4

**For Dataset Consumers:**
- Unambiguous data meanings
- Validated permissible values
- Better discoverability through classification
- Trustworthy metadata with governance trail

**For Tool Developers:**
- Standard ISO 11179 interfaces
- Validation rules from value domains
- Registry system integration
- Semantic mapping support

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/renato-umeton/biocroissant-to-omop.git
cd biocroissant-to-omop

# Install dependencies
pipenv install

# Validate examples
pipenv run python3 validate_v0.3.py
```

### Example Usage

```json
{
  "@context": "https://mlcommons.org/croissant/bio/0.3/context",
  "@type": "sc:Dataset",
  "dct:conformsTo": [
    "http://mlcommons.org/croissant/1.0",
    "http://mlcommons.org/croissant/bio/0.3"
  ],
  "bio:conformanceLevel": "Level 2",

  "name": "My Biomedical Dataset",
  "description": "Dataset with ISO 11179 metadata",

  "iso11179:steward": {
    "@type": "sc:Person",
    "name": "Dr. Jane Doe",
    "email": "steward@example.org"
  },

  "iso11179:registrationStatus": "standard",

  "bio:dataCategory": ["clinical"],

  "recordSet": [{
    "@type": "cr:RecordSet",
    "@id": "patients",
    "field": [{
      "@type": "cr:Field",
      "@id": "patients/gender",
      "name": "Gender",
      "dataType": "sc:Text",

      "iso11179:dataElementConcept": {
        "@id": "dec:Person.GenderAtBirth",
        "iso11179:objectClass": "Person",
        "iso11179:property": "Gender at Birth",
        "iso11179:definition": "Biological sex determined at birth"
      },

      "iso11179:valueDomain": {
        "@id": "vd:GenderCode",
        "iso11179:datatype": "String",
        "iso11179:permissibleValues": [
          {"value": "M", "meaning": "Male"},
          {"value": "F", "meaning": "Female"}
        ]
      }
    }]
  }]
}
```

## Conformance Levels

### Level 1: Basic Bio-Croissant
- Core Bio-Croissant properties
- ISO 11179 metadata **optional**
- Suitable for simple use cases

### Level 2: ISO 11179 Enhanced
- **Required**: Data steward and registration status
- **Required**: Value domains for coded fields
- **Recommended**: Data element concepts
- Suitable for governed datasets

### Level 3: Full Metadata Registry
- **Required**: Complete ISO 11179 metadata
- **Required**: Data element concepts for all fields
- **Required**: Classification scheme membership
- Suitable for registry integration

## Documentation

### Specifications
- [Bio-Croissant Specification v0.3](./BIO_CROISSANT_SPECIFICATION_v0.3.md) - Complete specification
- [Revision Summary v0.3](./REVISION_SUMMARY_v0.3.md) - What changed from v0.2

### Technical Files
- [JSON Schema](./schema/biocroissant-v0.3-schema.json) - Validation schema
- [JSON-LD Context](./context/biocroissant-v0.3-context.jsonld) - RDF context
- [Value Domains Registry](./value-domains/standard-value-domains.json) - Standard vocabularies

### Examples
- [OMOP CDM with ISO 11179](./examples/omop_cdm_iso11179.json) - Level 3 example
- [Examples README](./examples/README.md) - All examples documentation

## Features

### Core Bio-Croissant (from v0.2)
- Clinical data categories and study types
- Deidentification methods and privacy controls
- Quality metrics and completeness tracking
- Data access controls and governance

### OMOP CDM Extension
- OMOP CDM v5.4 table and field mappings
- Concept domain vocabularies
- Foreign key relationships
- Database dialect support

### Bioimaging Extension
- Multi-dimensional array metadata
- OME-Zarr format integration
- Physical dimensions and calibration
- Channel and modality specifications

### Whole Slide Imaging Extension
- Multi-resolution pyramid metadata
- Scanner and staining information
- Annotation formats
- Tile extraction specifications

### ISO 11179 Extensions (NEW in v0.3)
- Data element concepts
- Value domains with permissible values
- Conceptual domains
- Administrative metadata
- Classification schemes
- Registration management

## Validation

Validate your Bio-Croissant metadata:

```bash
# Validate v0.3 example
pipenv run python3 validate_v0.3.py

# Validate custom file
pipenv run python3 -c "
from validate_v0.3 import validate_file
from pathlib import Path

schema = Path('schema/biocroissant-v0.3-schema.json')
example = Path('your-dataset.json')

validate_file(example, schema)
"
```

## Migration from v0.2

v0.3 is **100% backward compatible** with v0.2. Migration is optional and incremental:

### Minimal Migration (5 minutes)
1. Update namespace versions in `@context`
2. Update `dct:conformsTo` to v0.3

### Level 2 Migration (30 minutes)
3. Add `iso11179:steward` with contact information
4. Add `iso11179:registrationStatus`
5. Reference standard value domains

### Level 3 Migration (2-4 hours)
6. Add data element concepts to all fields
7. Define custom value domains
8. Add classification scheme memberships

See [Migration Guide](./REVISION_SUMMARY_v0.3.md#migration-guide) for details.

## Standard Value Domains

Bio-Croissant v0.3 includes 16 standard value domains:

- **Data Category** - Types of biomedical data
- **Registration Status** - Metadata lifecycle stages
- **Deidentification Method** - Privacy techniques
- **Clinical Study Type** - Research study designs
- **OMOP Table Domain** - OMOP CDM table types
- **OMOP Database Dialect** - Database systems
- **Image Dimensionality** - 2D/3D/4D/5D specifications
- **Pixel Format** - Data types for images
- **Histological Stain Type** - Tissue staining methods
- **Optical Magnification** - Microscope magnifications
- **And more...**

See [standard-value-domains.json](./value-domains/standard-value-domains.json) for complete list.

## Roadmap

### v0.4 (Planned)
- Full ISO 11179-31 data specification registration
- Genomics and proteomics extensions
- Enhanced FHIR mapping
- External registry integration

### Future
- Automated value domain discovery
- ML model card integration
- Data quality assessment tools
- Registry API specifications

## Contributing

We welcome contributions! Areas of interest:

- Additional value domain definitions
- Domain-specific extensions
- Example datasets
- Validation tools
- Documentation improvements

## References

### ISO 11179 Standards
- [ISO/IEC 11179-1:2023 Framework](https://www.iso.org/standard/78914.html)
- [ISO/IEC 11179-31:2023 Metamodel](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-5:2015 Naming Principles](https://www.iso.org/standard/60341.html)
- [ISO/IEC 11179-6:2023 Registration](https://www.iso.org/standard/78916.html)
- [Aristotle Metadata Guide](https://help.aristotlecloud.io/subject-matter-and-theory/iso-iec-11179-data-element-representation)

### Related Standards
- [MLCommons Croissant](https://docs.mlcommons.org/croissant/)
- [OMOP CDM](https://ohdsi.github.io/CommonDataModel/)
- [OME Data Model](https://www.openmicroscopy.org/)
- [FHIR R5](https://hl7.org/fhir/)

## License

MIT License

## Contact

- **GitHub:** https://github.com/renato-umeton/biocroissant-to-omop
- **Issues:** https://github.com/renato-umeton/biocroissant-to-omop/issues

## Acknowledgments

Bio-Croissant v0.3 implements ISO/IEC 11179 standards with guidance from:
- MLCommons Croissant Working Group
- OHDSI OMOP CDM Community
- ISO/IEC JTC 1/SC 32 Metadata Standards

---

**Bio-Croissant v0.3** - Bringing standardized metadata governance to biomedical ML datasets.
