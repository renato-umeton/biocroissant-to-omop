# Bio-Croissant v0.3 Revision Summary

**Date:** 2025-12-04
**Previous Version:** v0.2
**Current Version:** v0.3

## Executive Summary

Bio-Croissant v0.3 introduces **ISO/IEC 11179 metadata registry** capabilities, enabling standardized data governance, semantic clarity, and value domain management for biomedical ML datasets. This is a major enhancement that aligns Bio-Croissant with international metadata standards.

## Motivation for v0.3

### Problems Addressed

1. **Semantic Ambiguity:** Fields lacked clear separation between meaning and representation
2. **Ungoverned Vocabularies:** No standard way to define permissible values
3. **Missing Stewardship:** No metadata about data governance and responsibility
4. **Inconsistent Definitions:** Field descriptions varied in clarity and completeness
5. **Limited Interoperability:** Difficult to map to other metadata registries

### ISO 11179 Benefits

Adopting [ISO/IEC 11179](https://www.iso.org/standard/78914.html) provides:

- **Data Element Concepts** separating semantics from representation
- **Value Domains** with controlled vocabularies and datatypes
- **Conceptual Domains** for vendor-neutral value meanings
- **Administrative Metadata** for governance and stewardship
- **Classification Schemes** for organizing biomedical metadata
- **Registration Management** with lifecycle tracking

## Major Changes

### 1. ISO 11179 Namespace (NEW)

**Added:** `iso11179:` namespace for metadata registry properties

```json
{
  "@context": {
    "iso11179": "http://mlcommons.org/croissant/bio/iso11179/0.3/"
  }
}
```

### 2. Administrative Metadata (NEW)

**Added:** Dataset-level governance properties per [ISO 11179-6](https://www.iso.org/standard/78916.html):

| Property | Type | Purpose |
|----------|------|---------|
| `iso11179:registrationAuthority` | Organization | Who manages the registry |
| `iso11179:registrationStatus` | Enum | Lifecycle status (draft/standard/retired) |
| `iso11179:steward` | Person/Org | Responsible for semantic accuracy |
| `iso11179:submitter` | Person/Org | Who submitted the metadata |
| `iso11179:registeredDate` | DateTime | Registration timestamp |
| `iso11179:lastReviewedDate` | DateTime | Last review timestamp |
| `iso11179:changeDescription` | Text | Summary of changes |

**Example:**

```json
{
  "iso11179:steward": {
    "@type": "sc:Person",
    "name": "Dr. Jane Smith",
    "email": "steward@example.org"
  },
  "iso11179:registrationStatus": "standard",
  "iso11179:registeredDate": "2025-12-04T00:00:00Z"
}
```

### 3. Data Element Concepts (NEW)

**Added:** Semantic definitions following [ISO 11179-3 metamodel](https://www.iso.org/standard/78925.html):

**Data Element Concept** = Object Class + Property

```json
{
  "iso11179:dataElementConcept": {
    "@id": "dec:Person.BirthDate",
    "iso11179:objectClass": "Person",
    "iso11179:property": "Birth Date",
    "iso11179:definition": "The calendar date on which a person was born"
  }
}
```

This separates **what the data means** (concept) from **how it's stored** (representation).

### 4. Value Domains (NEW)

**Added:** Permissible value specifications:

```json
{
  "iso11179:valueDomain": {
    "@id": "vd:DataCategory",
    "iso11179:datatype": "String",
    "iso11179:permissibleValues": [
      {"value": "clinical", "meaning": "Patient clinical care data"},
      {"value": "imaging", "meaning": "Medical or biological imaging data"},
      {"value": "omics", "meaning": "Genomics, proteomics, metabolomics data"}
    ]
  }
}
```

Standard value domains defined for:
- `bio:dataCategory`
- `iso11179:registrationStatus`
- `omop:tableDomain`
- `omop:databaseDialect`
- `bioimg:dimensionality`
- `bioimg:pixelFormat`
- `wsi:stainType`
- And more...

### 5. Conceptual Domains (NEW)

**Added:** Semantic value meanings independent of representation:

```json
{
  "@type": "iso11179:ConceptualDomain",
  "@id": "cd:BiologicalSex",
  "name": "Biological Sex",
  "iso11179:valueMeanings": [
    {"@id": "vm:Male", "definition": "..."},
    {"@id": "vm:Female", "definition": "..."}
  ]
}
```

### 6. Classification Schemes (NEW)

**Added:** Hierarchical categorization of metadata items:

```json
{
  "@type": "iso11179:ClassificationScheme",
  "@id": "cs:ClinicalDomain",
  "iso11179:classificationItems": [
    {"@id": "ci:Demographics", "name": "Demographics"},
    {"@id": "ci:Diagnoses", "name": "Diagnoses and Conditions"},
    {"@id": "ci:Procedures", "name": "Procedures and Interventions"}
  ]
}
```

### 7. Conformance Levels (ENHANCED)

**Modified:** Three conformance levels:

**Level 1:** Basic Bio-Croissant (ISO 11179 optional)
**Level 2:** ISO 11179 Enhanced
- Required: Administrative metadata
- Required: Value domains for coded fields
- Recommended: Data element concepts

**Level 3:** Full Metadata Registry
- Required: Complete ISO 11179 metadata
- Required: Classification schemes
- Required: All value domains

### 8. Namespace Versioning (UPDATED)

**Changed:** All namespaces updated to v0.3:

```
bio:       0.2 → 0.3
omop:      0.2 → 0.3
bioimg:    0.2 → 0.3
wsi:       0.2 → 0.3
iso11179:  NEW in 0.3
```

## Detailed Property Additions

### Dataset-Level

| Property (NEW) | Type | Description |
|---------------|------|-------------|
| `iso11179:registrationAuthority` | Organization | Registration authority |
| `iso11179:registrationStatus` | Enum | Lifecycle status |
| `iso11179:steward` | Person/Org | Data steward |
| `iso11179:submitter` | Person/Org | Submitter |
| `iso11179:registeredDate` | DateTime | Registration date |
| `iso11179:lastReviewedDate` | DateTime | Last review date |
| `iso11179:changeDescription` | Text | Change summary |

### Field-Level

| Property (NEW) | Type | Description |
|---------------|------|-------------|
| `iso11179:dataElementConcept` | Object | Semantic concept definition |
| `iso11179:valueDomain` | Object | Representation specification |
| `iso11179:classifiedBy` | Array | Classification scheme membership |

### Data Element Concept Properties

| Property (NEW) | Type | Description |
|---------------|------|-------------|
| `iso11179:objectClass` | String | Object being described |
| `iso11179:property` | String | Characteristic of object |
| `iso11179:definition` | String | Precise semantic definition |
| `iso11179:conceptualDomain` | Reference | Associated conceptual domain |
| `iso11179:classificationScheme` | Array | Classification memberships |

### Value Domain Properties

| Property (NEW) | Type | Description |
|---------------|------|-------------|
| `iso11179:datatype` | String | Datatype specification |
| `iso11179:unitOfMeasure` | String | Unit of measurement |
| `iso11179:format` | String | Format specification |
| `iso11179:maximumLength` | Integer | Maximum length constraint |
| `iso11179:minimumValue` | Number | Minimum value constraint |
| `iso11179:maximumValue` | Number | Maximum value constraint |
| `iso11179:permissibleValues` | Array | List of allowed values |
| `iso11179:conceptualDomain` | Reference | Associated conceptual domain |

## Files Updated

### New Files

1. **BIO_CROISSANT_SPECIFICATION_v0.3.md** - Complete v0.3 specification
2. **context/biocroissant-v0.3-context.jsonld** - JSON-LD context with ISO 11179 properties
3. **REVISION_SUMMARY_v0.3.md** - This document

### Files to Update

1. **schema/biocroissant-v0.3-schema.json** - JSON Schema with value domain validation
2. **examples/omop_cdm_iso11179.json** - Example demonstrating ISO 11179 features
3. **value-domains/standard-value-domains.json** - Standard value domain registry

## Backward Compatibility

**Status:** FULLY BACKWARD COMPATIBLE

- All v0.2 properties remain valid in v0.3
- ISO 11179 properties are optional for Level 1 conformance
- Existing v0.2 datasets can be used without modification
- Migration to v0.3 only requires namespace version updates

## Migration Guide

### Minimal Migration (v0.2 → v0.3)

1. Update namespace versions in `@context`:
   ```json
   {
     "bio": "http://mlcommons.org/croissant/bio/0.3/",
     "omop": "http://mlcommons.org/croissant/bio/omop/0.3/"
   }
   ```

2. Update conformance declaration:
   ```json
   {
     "dct:conformsTo": [
       "http://mlcommons.org/croissant/1.0",
       "http://mlcommons.org/croissant/bio/0.3"
     ]
   }
   ```

### Enhanced Migration (Level 2 Conformance)

3. Add administrative metadata:
   ```json
   {
     "iso11179:steward": {
       "@type": "sc:Person",
       "name": "Steward Name",
       "email": "steward@example.org"
     },
     "iso11179:registrationStatus": "standard"
   }
   ```

4. Add value domains for coded fields:
   ```json
   {
     "bio:dataCategory": ["clinical"],
     "iso11179:valueDomain": {"@id": "vd:DataCategory"}
   }
   ```

### Full Migration (Level 3 Conformance)

5. Add data element concepts to all fields:
   ```json
   {
     "@type": "cr:Field",
     "iso11179:dataElementConcept": {
       "@id": "dec:ObjectClass.Property",
       "iso11179:objectClass": "Object Class",
       "iso11179:property": "Property",
       "iso11179:definition": "Precise definition"
     }
   }
   ```

6. Add classification scheme memberships:
   ```json
   {
     "iso11179:classifiedBy": [
       {"@id": "ci:Demographics"}
     ]
   }
   ```

## Benefits of v0.3

### For Dataset Publishers

- **Standardized governance** with clear stewardship
- **Controlled vocabularies** reduce data quality issues
- **Semantic clarity** through data element concepts
- **Registration tracking** for versioning and lifecycle management

### For Dataset Consumers

- **Unambiguous meanings** via conceptual domains
- **Validated values** through value domain specifications
- **Better discoverability** via classification schemes
- **Trustworthy metadata** with steward attribution

### For Tool Developers

- **Standard interfaces** following ISO 11179
- **Validation rules** from value domains
- **Mapping support** via conceptual domains
- **Registry integration** with ISO 11179-compliant systems

## ISO 11179 Compliance

Bio-Croissant v0.3 implements:

- **[ISO/IEC 11179-1:2023](https://www.iso.org/standard/78914.html)** - Framework ✓
- **[ISO/IEC 11179-3](https://www.iso.org/standard/78925.html)** - Registry metamodel (partial)
- **[ISO/IEC 11179-5:2015](https://www.iso.org/standard/60341.html)** - Naming principles ✓
- **[ISO/IEC 11179-6:2023](https://www.iso.org/standard/78916.html)** - Registration metadata ✓

## Next Steps

### Implementation Tasks

1. ✓ Create v0.3 specification document
2. ✓ Create v0.3 JSON-LD context
3. ⏳ Create v0.3 JSON Schema
4. ⏳ Create standard value domain registry
5. ⏳ Create example with ISO 11179 metadata
6. ⏳ Update validation tools

### Future Enhancements (v0.4+)

- Full ISO 11179-31 data specification registration
- Integration with external metadata registries
- Automated value domain discovery
- Enhanced FHIR mapping via ISO 11179 concepts

## References

- [ISO/IEC 11179-1:2023 Framework](https://www.iso.org/standard/78914.html)
- [ISO/IEC 11179-31:2023 Metamodel](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-5:2015 Naming Principles](https://www.iso.org/standard/60341.html)
- [ISO/IEC 11179-6:2023 Registration](https://www.iso.org/standard/78916.html)
- [Aristotle Metadata - ISO 11179 Guide](https://help.aristotlemetadata.com/subject-matter-and-theory/iso-iec-11179-data-element-representation)
- [ISO/IEC 11179 - Wikipedia](https://en.wikipedia.org/wiki/ISO/IEC_11179)

## Contact

For questions about Bio-Croissant v0.3:

- **GitHub:** https://github.com/renato-umeton/biocroissant-to-omop
- **Issues:** https://github.com/renato-umeton/biocroissant-to-omop/issues
- **Specification:** BIO_CROISSANT_SPECIFICATION_v0.3.md

---

**Document Version:** 1.0
**Last Updated:** 2025-12-04
**Status:** Final
