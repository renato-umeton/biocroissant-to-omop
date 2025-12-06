# Bio-Croissant Format Specification

**Version:** 0.2.0 (Updated Working Draft)
**Published:** December 2025
**Status:** Updated Working Draft
**Canonical URI:** `http://mlcommons.org/croissant/bio/0.2`
**Previous Version:** `http://mlcommons.org/croissant/bio/0.1`

## Authors

Bio-Croissant Working Group:
- Sebastian Lobentanzer (OMOP Workstream Lead)
- Josh Moore (Bioimage Workstream Lead)
- Agata Krason (Whole Slide Image Workstream Lead)
- Steffen Vogler (Bayer, Initiative Lead)
- Bio-Croissant Community Contributors

## Abstract

Bio-Croissant is a metadata format extending MLCommons Croissant 1.0 for biomedical, biological, and healthcare machine learning datasets. It provides standardized vocabulary for clinical data (OMOP CDM), biomedical imaging (microscopy, whole slide imaging), and related domains while maintaining backward compatibility with Croissant. This specification defines required and optional metadata properties, data types, validation rules, and integration patterns with existing biomedical standards.

## Status of This Document

This is an Updated Working Draft. It has undergone internal review and is ready for community feedback. Implementations are encouraged to provide feedback before final release.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Conformance](#2-conformance)
3. [Namespaces and Vocabularies](#3-namespaces-and-vocabularies)
4. [Core Metadata Model](#4-core-metadata-model)
5. [Data Types](#5-data-types)
6. [OMOP CDM Extension](#6-omop-cdm-extension)
7. [Bioimaging Extension](#7-bioimaging-extension)
8. [Whole Slide Imaging Extension](#8-whole-slide-imaging-extension)
9. [Cross-Domain Features](#9-cross-domain-features)
10. [Validation and Quality](#10-validation-and-quality)
11. [Implementation Guidance](#11-implementation-guidance)
12. [Examples](#12-examples)
13. [Appendices](#13-appendices)

---

## 1. Introduction

### 1.1 Motivation

While the MLCommons Croissant format provides excellent support for general machine learning datasets, biomedical data presents unique requirements:

**Clinical Data Challenges:**
- Standardized healthcare data models (OMOP CDM, FHIR)
- Mandatory de-identification for human subjects
- Complex vocabulary systems and concept mappings
- Regulatory compliance (HIPAA, GDPR)

**Imaging Modality Challenges:**
- Multi-dimensional arrays (T, C, Z, Y, X)
- Physical metadata (micrometers, timepoints)
- Multi-resolution pyramids (whole slide imaging)
- Integration with OME standards

**Domain-Specific Metadata:**
- Biological specimens and assays
- Experimental protocols
- Taxonomic information
- Measurement techniques

Bio-Croissant addresses these challenges while maintaining full backward compatibility with Croissant 1.0.

### 1.2 Design Principles

1. **Backward Compatibility**: All Bio-Croissant datasets are valid Croissant 1.0 datasets
2. **Minimal Extension**: Only add necessary properties; leverage existing standards
3. **Conditional Requirements**: Requirements vary based on data category and content
4. **Interoperability**: Align with OMOP, OME, FHIR, BioSchemas, and OBO ontologies
5. **Privacy-First**: De-identification and access control as core features
6. **Modular Design**: Domain extensions are independent and optional
7. **Machine Validation**: All requirements are machine-verifiable

### 1.3 Scope

**In Scope:**
- Metadata extensions for clinical, imaging, and biological datasets
- Integration with OMOP CDM v5.4+
- Bioimaging metadata (microscopy, OME-Zarr, OME-TIFF)
- Whole slide imaging (digital pathology)
- Privacy and security metadata
- Genomics, proteomics, metabolomics basics
- FHIR resource references

**Out of Scope:**
- Data transmission protocols
- Clinical workflow orchestration
- Real-time decision support systems
- Modifications to base Croissant specification

### 1.4 Use Cases

1. **Clinical Research**: OMOP CDM observational health data for ML training
2. **Drug Discovery**: High-content screening microscopy with compound treatments
3. **Digital Pathology**: WSI datasets for cancer detection and classification
4. **Multi-Omics**: Integrated genomics, proteomics, and metabolomics
5. **Federated Learning**: Privacy-preserving distributed training on healthcare data
6. **Regulatory Submissions**: ML model training data documentation

---

## 2. Conformance

### 2.1 Conformance Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

### 2.2 Base Requirements

All Bio-Croissant datasets MUST:

1. Conform to Croissant 1.0 specification
2. Include valid JSON-LD `@context` with Bio-Croissant namespaces
3. Declare conformance via `dct:conformsTo`:
   ```json
   "dct:conformsTo": [
     "http://mlcommons.org/croissant/1.0",
     "http://mlcommons.org/croissant/bio/0.2"
   ]
   ```
4. Use valid JSON-LD syntax (validated against JSON-LD 1.1)
5. Include all required Croissant dataset properties (name, description, license, etc.)

### 2.3 Conformance Levels

Bio-Croissant defines three conformance levels:

#### Level 1: Basic Bio-Croissant

**Requirements:**
- Declares Bio-Croissant conformance
- Uses at least one Bio-Croissant data type (from Section 5)
- Includes `bio:dataCategory` property
- For human subjects data: includes `bio:deidentificationMethod`

**Use Case:** Simple biomedical datasets with minimal domain-specific metadata

#### Level 2: Domain-Specific

**Requirements:**
- All Level 1 requirements
- Implements at least one complete domain extension (OMOP, Bioimaging, or WSI)
- Uses domain-specific RecordSet patterns
- Provides domain-specific metadata properties
- If human data: includes Data Use Ontology (DUO) terms

**Use Case:** Production datasets for specific biomedical domains

#### Level 3: Full Compliance

**Requirements:**
- All Level 2 requirements
- Implements 2+ domain extensions with cross-references
- Includes BioSchemas dual typing (`["sc:Dataset", "bioschemas:Dataset"]`)
- Provides complete provenance metadata (Section 9.3)
- Includes quality metrics (Section 9.4)
- All FileObjects include SHA256 checksums
- Complete vocabulary version documentation

**Use Case:** High-quality datasets for publication, regulatory submission, or long-term archival

### 2.4 Conformance Declaration

Datasets SHOULD explicitly declare their conformance level:

```json
{
  "@context": { ... },
  "@type": ["sc:Dataset", "bioschemas:Dataset"],
  "dct:conformsTo": [
    "http://mlcommons.org/croissant/1.0",
    "http://mlcommons.org/croissant/bio/0.2"
  ],
  "bio:conformanceLevel": "Level 2",
  "bio:extensions": ["omop", "bioimaging"]
}
```

### 2.5 Conditional Requirements

Many Bio-Croissant requirements are conditional based on data characteristics:

| Condition | Required Properties |
|-----------|-------------------|
| Contains human subjects data | `bio:deidentificationMethod` |
| Requires authentication | `bio:authenticatedAccess`, `bio:accessControlMechanism` |
| Uses OMOP CDM | `omop:cdmVersion`, `omop:vocabularyVersion` |
| Contains imaging data | `bioimg:dimensionality` or `wsi:scannerManufacturer` |
| Level 3 conformance | All RECOMMENDED properties for used extensions |

**Determining Human Subjects Data:**

A dataset contains human subjects data if:
- `bio:dataCategory` includes "clinical", "patient", or "human"
- `bioschemas:taxonomicRange` is `http://purl.obolibrary.org/obo/NCBITaxon_9606` (Homo sapiens)
- Any RecordSet represents individual human records

---

## 3. Namespaces and Vocabularies

### 3.1 Namespace Definitions

Bio-Croissant introduces versioned namespaces:

| Prefix | Namespace IRI | Description |
|--------|---------------|-------------|
| `bio` | `http://mlcommons.org/croissant/bio/0.2/` | Core Bio-Croissant vocabulary |
| `omop` | `http://mlcommons.org/croissant/bio/omop/0.2/` | OMOP CDM extensions |
| `bioimg` | `http://mlcommons.org/croissant/bio/imaging/0.2/` | Bioimaging extensions |
| `wsi` | `http://mlcommons.org/croissant/bio/wsi/0.2/` | Whole slide imaging |
| `obo` | `http://purl.obolibrary.org/obo/` | Open Biological Ontologies |
| `bioschemas` | `https://bioschemas.org/` | BioSchemas vocabulary |
| `fhir` | `http://hl7.org/fhir/` | FHIR resources |
| `prov` | `http://www.w3.org/ns/prov#` | W3C Provenance |
| `duo` | `http://purl.obolibrary.org/obo/DUO_` | Data Use Ontology |

### 3.2 Complete JSON-LD Context

All Bio-Croissant metadata files MUST include this context (or a superset):

```json
{
  "@context": {
    "@version": 1.1,
    "@language": "en",
    "@vocab": "https://schema.org/",
    "sc": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/",
    "rai": "http://mlcommons.org/croissant/RAI/",
    "dct": "http://purl.org/dc/terms/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",

    "bio": "http://mlcommons.org/croissant/bio/0.2/",
    "omop": "http://mlcommons.org/croissant/bio/omop/0.2/",
    "bioimg": "http://mlcommons.org/croissant/bio/imaging/0.2/",
    "wsi": "http://mlcommons.org/croissant/bio/wsi/0.2/",
    "obo": "http://purl.obolibrary.org/obo/",
    "bioschemas": "https://bioschemas.org/",
    "fhir": "http://hl7.org/fhir/",
    "prov": "http://www.w3.org/ns/prov#",
    "duo": "http://purl.obolibrary.org/obo/DUO_",

    "conformanceLevel": "bio:conformanceLevel",
    "extensions": "bio:extensions",
    "dataCategory": "bio:dataCategory",
    "deidentificationMethod": "bio:deidentificationMethod",
    "deidentificationNote": "bio:deidentificationNote",
    "cohortDescription": "bio:cohortDescription",
    "clinicalStudyType": "bio:clinicalStudyType",
    "specimenType": "bio:specimenType",
    "assayType": "bio:assayType",
    "authenticatedAccess": {
      "@id": "bio:authenticatedAccess",
      "@type": "xsd:boolean"
    },
    "accessControlMechanism": "bio:accessControlMechanism",
    "accessControlEndpoint": {
      "@id": "bio:accessControlEndpoint",
      "@type": "@id"
    },
    "dataAccessCommittee": "bio:dataAccessCommittee",
    "dataUseOntology": {
      "@id": "bio:dataUseOntology",
      "@type": "@id"
    },
    "vocabulary": "bio:vocabulary",
    "vocabularyVersion": "bio:vocabularyVersion",
    "qualityMetrics": "bio:qualityMetrics"
  }
}
```

**Note:** A complete context with all properties is provided in Appendix A.

### 3.3 Namespace Versioning Policy

- Minor version increments (0.1 -> 0.2): backward compatible additions
- Major version increments (0.x -> 1.0): may include breaking changes
- Implementations SHOULD accept any minor version >= declared version
- Implementations MUST reject major version mismatches

---

## 4. Core Metadata Model

### 4.1 Dataset-Level Properties

All Bio-Croissant datasets inherit schema.org/Dataset properties from Croissant 1.0 and add the following:

#### 4.1.1 Core Bio-Croissant Properties

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bio:dataCategory` | Text | MANY | Always | Categories: "clinical", "imaging", "omics", "pathology", "cellular", "molecular", "animal", "synthetic" |
| `bio:conformanceLevel` | Text | ONE | Recommended | "Level 1", "Level 2", or "Level 3" |
| `bio:extensions` | Text | MANY | If Level 2+ | Array of extension names: ["omop", "bioimaging", "wsi"] |

#### 4.1.2 Human Subjects Properties

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bio:deidentificationMethod` | Text or URL | ONE | Human subjects data | Method: "HIPAA Safe Harbor", "Expert Determination", "k-anonymity", "Synthetic", etc. |
| `bio:cohortDescription` | Text | ONE | Recommended for clinical | Description of patient cohort or study population |
| `bio:clinicalStudyType` | Text or URL | ONE | Clinical studies | "observational", "interventional", "registry", "case-control" |

#### 4.1.3 Access Control Properties

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bio:authenticatedAccess` | Boolean | ONE | If auth required | Whether dataset requires authentication |
| `bio:accessControlMechanism` | Text or URL | ONE | If authenticated | "OAuth2", "SAML", "institutional", "DAC approval" |
| `bio:accessControlEndpoint` | URL | ONE | If OAuth/SAML | Authentication endpoint URL |
| `bio:dataAccessCommittee` | Organization | ONE | If DAC required | Contact info for data access committee |

#### 4.1.4 Data Use and Licensing

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bio:dataUseOntology` | URL | MANY | Recommended for human data | DUO term URIs (e.g., duo:0000042 for general research use) |
| `bio:dataUseDescription` | Text | ONE | If DUO provided | Human-readable data use restrictions |
| `bio:ethicsApprovalNumber` | Text | ONE | If applicable | IRB or ethics committee approval number |

#### 4.1.5 Biological Context Properties

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bio:specimenType` | Text or URL | MANY | Biological specimens | "blood", "tissue", "cell line", "FFPE", "saliva" |
| `bio:assayType` | Text or URL | MANY | Experimental data | "RNA-seq", "immunohistochemistry", "mass spectrometry" |

### 4.2 RecordSet-Level Properties

RecordSets inherit from Croissant `cr:RecordSet` and may include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `bio:recordType` | Text | ONE | Semantic type: "patient", "visit", "observation", "image", "cell", "molecule" |
| `bio:temporalCoverage` | Text | ONE | Time period covered (ISO 8601 interval) |

### 4.3 Field-Level Properties

Fields inherit from Croissant `cr:Field` and may include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `bio:vocabulary` | Text | ONE | Vocabulary name (e.g., "SNOMED CT", "LOINC") |
| `bio:vocabularyVersion` | Text | ONE | Version identifier |
| `bio:deidentificationNote` | Text | ONE | Explanation of de-identification applied to field |
| `bio:unit` | Text or URL | ONE | Measurement unit (prefer UCUM codes) |

---

## 5. Data Types

### 5.1 Data Type Semantics

Bio-Croissant data types are **semantic annotations**, not type hierarchies. They indicate meaning and expected usage patterns while the underlying JSON-LD `dataType` remains a schema.org type.

**Pattern:**
```json
{
  "@type": "cr:Field",
  "dataType": "sc:Integer",
  "bio:semanticType": "bio:ConceptID",
  "bio:vocabulary": "SNOMED CT"
}
```

For brevity, documentation may show:
```json
{
  "dataType": "bio:ConceptID"
}
```

But implementations SHOULD interpret this as the pattern above.

### 5.2 Healthcare Data Types

| Semantic Type | Base Type | Description | Usage |
|---------------|-----------|-------------|-------|
| `bio:ConceptID` | `sc:Integer` | Standardized vocabulary concept identifier | OMOP concept fields, SNOMED codes |
| `bio:DateShifted` | `sc:Date` | Date shifted by random offset for de-identification | De-identified date fields |
| `bio:AgeCategory` | `sc:Text` | Age as range rather than exact value | "18-25", "65+", etc. |
| `bio:DeidentifiedText` | `sc:Text` | Text with PHI removed/masked | Clinical notes, reports |
| `bio:ClinicalCode` | `sc:Text` | Medical coding string | ICD-10, CPT, LOINC codes |
| `bio:EncounterID` | `sc:Integer` | Healthcare encounter identifier | Visit IDs, admission numbers |

### 5.3 Imaging Data Types

| Semantic Type | Base Type | Description | Usage |
|---------------|-----------|-------------|-------|
| `bioimg:MicroscopyImage` | `sc:ImageObject` | Microscopy image with dimensional metadata | Fluorescence, brightfield imaging |
| `bioimg:MultiDimensionalArray` | - (complex) | N-dimensional array (T, C, Z, Y, X) | Time-series, z-stacks, multi-channel |
| `bioimg:ROI` | `sc:GeoShape` | Region of interest annotation | Cell boundaries, tissue regions |
| `bioimg:Mask` | - (complex) | Label or binary mask | Segmentation outputs |
| `wsi:WholeSlideImage` | `sc:ImageObject` | Digital pathology whole slide image | Histopathology slides |
| `wsi:ImagePyramid` | - (complex) | Multi-resolution pyramid levels | WSI with multiple zoom levels |
| `wsi:TileLocator` | - (complex) | Tile coordinate specification | Patch extraction coordinates |

### 5.4 Omics Data Types

| Semantic Type | Base Type | Description | Usage |
|---------------|-----------|-------------|-------|
| `bio:SequenceData` | - (complex) | Genomic sequence data | FASTQ, BAM, VCF formats |
| `bio:VariantCall` | - (complex) | Genetic variant | SNPs, indels |
| `bio:GeneExpression` | `sc:Float` | Gene expression value | RNA-seq TPM, microarray |
| `bio:MassSpectrum` | - (complex) | Mass spectrometry spectrum | Proteomics, metabolomics |

### 5.5 Data Type Extensions

Implementations MAY define additional semantic types by:

1. Using a domain-specific namespace
2. Providing clear base type mapping
3. Documenting expected properties
4. Registering with Bio-Croissant registry (when available)

Example custom type:
```json
{
  "@context": {
    "mylab": "https://example.org/mylab/types/"
  },
  "dataType": "sc:Float",
  "mylab:semanticType": "mylab:CalciumSignal",
  "mylab:signalUnit": "nM",
  "mylab:acquisitionRate": 100
}
```

---

## 6. OMOP CDM Extension

### 6.1 Overview

The OMOP extension enables representation of OMOP Common Data Model v5.4+ datasets. It provides metadata for clinical tables, vocabulary mappings, and concept relationships.

### 6.2 OMOP Dataset Properties

When using OMOP extension, datasets MUST include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:cdmVersion` | Text | ONE | OMOP CDM version (e.g., "5.4", "5.4.1") |
| `omop:vocabularyVersion` | Text or Object | ONE | Vocabulary version (see 6.2.1) |
| `omop:cdmSourceName` | Text | ONE | Source database name |

Datasets SHOULD include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:databaseDialect` | Text | ONE | "postgresql", "sql_server", "oracle", "redshift" |
| `omop:cdmReleaseDate` | Date | ONE | Date CDM was implemented for this source |

#### 6.2.1 Vocabulary Versioning

For single vocabulary version:
```json
{
  "omop:vocabularyVersion": "v5.0 20-Oct-2024"
}
```

For multiple vocabularies:
```json
{
  "omop:vocabularyVersions": [
    {
      "vocabulary": "SNOMED",
      "version": "2024-01-31",
      "versionFormat": "date"
    },
    {
      "vocabulary": "RxNorm",
      "version": "2024-10-07",
      "versionFormat": "date"
    }
  ]
}
```

### 6.3 OMOP RecordSet Properties

RecordSets representing OMOP tables MUST include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:cdmTable` | Text | ONE | OMOP table name (e.g., "PERSON", "DRUG_EXPOSURE") |
| `omop:tableDomain` | Text | ONE | "Clinical", "Vocabulary", "Health Economics", "Derived", "System" |

RecordSets SHOULD include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:distributionKey` | Text | ONE | "person_id", "RANDOM", or other distribution column |
| `omop:recordCount` | Integer | ONE | Approximate number of records |

### 6.4 OMOP Field Properties

Fields representing OMOP columns MUST include:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:cdmField` | Text | ONE | OMOP field name exactly as in specification |

Fields SHOULD include when applicable:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `omop:isRequired` | Boolean | ONE | Per OMOP CDM specification |
| `omop:isPrimaryKey` | Boolean | ONE | Is primary key |
| `omop:isForeignKey` | Boolean | ONE | Is foreign key |
| `omop:foreignKeyTable` | Text | ONE | Referenced table name |
| `omop:foreignKeyField` | Text | ONE | Referenced field name |
| `omop:conceptDomain` | Text | ONE | For concept_id fields: "Drug", "Condition", "Gender", etc. |

### 6.5 OMOP Extraction Mechanisms

Bio-Croissant defines OMOP-specific extraction operators:

#### 6.5.1 SQL Query Extraction

```json
{
  "source": {
    "omop:sqlQuery": "SELECT * FROM @cdmDatabaseSchema.PERSON WHERE person_id < 1000",
    "omop:databaseSchema": "cdm_synpuf"
  }
}
```

#### 6.5.2 Concept Lookup

```json
{
  "source": {
    "fileObject": { "@id": "condition_table" },
    "extract": { "column": "condition_concept_id" },
    "omop:conceptLookup": {
      "vocabularyTable": { "@id": "concept_table" },
      "joinOn": "concept_id",
      "returnField": "concept_name"
    }
  }
}
```

### 6.6 OMOP RecordSet Patterns

#### 6.6.1 Person Table Pattern

```json
{
  "@type": "cr:RecordSet",
  "@id": "person",
  "name": "PERSON",
  "description": "OMOP CDM PERSON table with patient demographics",
  "omop:cdmTable": "PERSON",
  "omop:tableDomain": "Clinical",
  "omop:distributionKey": "person_id",
  "omop:recordCount": 10000,
  "bio:recordType": "patient",
  "key": [{ "@id": "person/person_id" }],
  "field": [
    {
      "@type": "cr:Field",
      "@id": "person/person_id",
      "name": "person_id",
      "description": "Unique identifier for each person",
      "dataType": "sc:Integer",
      "omop:cdmField": "person_id",
      "omop:isRequired": true,
      "omop:isPrimaryKey": true,
      "source": {
        "fileObject": { "@id": "person_csv" },
        "extract": { "column": "person_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "person/gender_concept_id",
      "name": "gender_concept_id",
      "description": "Standard concept for biological sex at birth",
      "dataType": "sc:Integer",
      "bio:semanticType": "bio:ConceptID",
      "omop:cdmField": "gender_concept_id",
      "omop:isRequired": true,
      "omop:isForeignKey": true,
      "omop:foreignKeyTable": "CONCEPT",
      "omop:foreignKeyField": "concept_id",
      "omop:conceptDomain": "Gender",
      "bio:vocabulary": "OMOP Gender",
      "bio:vocabularyVersion": "v5.0",
      "references": { "@id": "concept/concept_id" },
      "source": {
        "fileObject": { "@id": "person_csv" },
        "extract": { "column": "gender_concept_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "person/year_of_birth",
      "name": "year_of_birth",
      "description": "Year of birth",
      "dataType": "sc:Integer",
      "omop:cdmField": "year_of_birth",
      "omop:isRequired": true,
      "bio:deidentificationNote": "Exact year preserved; may be generalized in some datasets",
      "source": {
        "fileObject": { "@id": "person_csv" },
        "extract": { "column": "year_of_birth" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "person/birth_datetime",
      "name": "birth_datetime",
      "description": "Date and time of birth (de-identified)",
      "dataType": "sc:DateTime",
      "bio:semanticType": "bio:DateShifted",
      "omop:cdmField": "birth_datetime",
      "bio:deidentificationNote": "All datetimes shifted by same random offset per person",
      "source": {
        "fileObject": { "@id": "person_csv" },
        "extract": { "column": "birth_datetime" }
      }
    }
  ]
}
```

#### 6.6.2 Clinical Event Table Pattern

```json
{
  "@type": "cr:RecordSet",
  "@id": "drug_exposure",
  "name": "DRUG_EXPOSURE",
  "description": "OMOP CDM DRUG_EXPOSURE table with medication records",
  "omop:cdmTable": "DRUG_EXPOSURE",
  "omop:tableDomain": "Clinical",
  "omop:distributionKey": "person_id",
  "bio:recordType": "medication_administration",
  "key": [{ "@id": "drug_exposure/drug_exposure_id" }],
  "field": [
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/drug_exposure_id",
      "name": "drug_exposure_id",
      "dataType": "sc:Integer",
      "omop:cdmField": "drug_exposure_id",
      "omop:isPrimaryKey": true,
      "source": {
        "fileObject": { "@id": "drug_exposure_csv" },
        "extract": { "column": "drug_exposure_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/person_id",
      "name": "person_id",
      "dataType": "sc:Integer",
      "omop:cdmField": "person_id",
      "omop:isRequired": true,
      "omop:isForeignKey": true,
      "omop:foreignKeyTable": "PERSON",
      "omop:foreignKeyField": "person_id",
      "references": { "@id": "person/person_id" },
      "source": {
        "fileObject": { "@id": "drug_exposure_csv" },
        "extract": { "column": "person_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/drug_concept_id",
      "name": "drug_concept_id",
      "dataType": "sc:Integer",
      "bio:semanticType": "bio:ConceptID",
      "omop:cdmField": "drug_concept_id",
      "omop:isRequired": true,
      "omop:isForeignKey": true,
      "omop:foreignKeyTable": "CONCEPT",
      "omop:conceptDomain": "Drug",
      "bio:vocabulary": "RxNorm",
      "references": { "@id": "concept/concept_id" },
      "source": {
        "fileObject": { "@id": "drug_exposure_csv" },
        "extract": { "column": "drug_concept_id" }
      }
    }
  ]
}
```

### 6.7 Cross-RecordSet Queries

Bio-Croissant implementations that support querying SHOULD support:

1. **Foreign Key Traversal**: Follow `references` to join RecordSets
2. **Concept Resolution**: Lookup concept names from IDs
3. **Temporal Filtering**: Filter by date ranges on datetime fields

Example conceptual query pattern:
```python
# Get condition names for patient 123
person = dataset.recordSet['person'].filter(person_id=123)
conditions = dataset.recordSet['condition_occurrence'].filter(
    person_id=person.person_id
)
condition_names = conditions.join(
    dataset.recordSet['concept'],
    left_on='condition_concept_id',
    right_on='concept_id'
).select('concept_name')
```

---

## 7. Bioimaging Extension

### 7.1 Overview

The Bioimaging extension supports microscopy images, multi-dimensional arrays, and integration with OME (Open Microscopy Environment) standards.

### 7.2 Bioimaging Dataset Properties

| Property | Type | Cardinality | Required When | Description |
|----------|------|-------------|---------------|-------------|
| `bioimg:imagingModality` | Text or URL | MANY | Imaging datasets | "fluorescence", "brightfield", "confocal", "electron microscopy", "TIRF" |
| `bioimg:dimensionality` | Text | ONE | Imaging datasets | "2D", "3D", "4D" (3D+T), "5D" (3D+T+C) |
| `bioimg:pixelFormat` | Text | ONE | Recommended | "uint8", "uint16", "float32", "float64" |

### 7.3 Bioimaging Field Properties

For fields with `dataType` of `bioimg:MultiDimensionalArray`:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `bioimg:dimensions` | Object | ONE | Dimension sizes: `{"T": 10, "C": 4, "Z": 50, "Y": 1024, "X": 1024}` |
| `bioimg:dimensionOrder` | Text | ONE | Order specification: "TCZYX", "XYCZT", etc. |
| `bioimg:physicalSizeX` | Number | RECOMMENDED | Physical size per pixel in X (micrometers) |
| `bioimg:physicalSizeY` | Number | RECOMMENDED | Physical size per pixel in Y (micrometers) |
| `bioimg:physicalSizeZ` | Number | If Z present | Physical size per pixel in Z (micrometers) |
| `bioimg:physicalSizeUnit` | Text | ONE | "micrometer", "nanometer", "millimeter" |
| `bioimg:timeIncrement` | Number | If T present | Time between frames (seconds) |
| `bioimg:timeUnit` | Text | If T present | "second", "millisecond", "minute" |

#### 7.3.1 Channel Metadata

For multi-channel images:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `bioimg:channelNames` | Text | MANY | Channel names: ["DAPI", "GFP", "RFP", "Cy5"] |
| `bioimg:channelColors` | Text | MANY | Display colors (hex): ["#0000FF", "#00FF00", "#FF0000"] |
| `bioimg:channelExcitationWavelength` | Number | MANY | Excitation wavelengths (nm): [405, 488, 561] |
| `bioimg:channelEmissionWavelength` | Number | MANY | Emission wavelengths (nm): [461, 525, 595] |
| `bioimg:channelIlluminationType` | Text | MANY | "transmitted", "epifluorescence", "oblique" |

#### 7.3.2 Acquisition Metadata

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `bioimg:objectiveLens` | Object | ONE | `{"magnification": 40, "na": 1.3, "immersion": "oil"}` |
| `bioimg:microscopeManufacturer` | Text | ONE | Microscope manufacturer |
| `bioimg:microscopeModel` | Text | ONE | Microscope model |
| `bioimg:acquisitionSoftware` | Text | ONE | Acquisition software and version |
| `bioimg:acquisitionDate` | DateTime | ONE | When images were acquired |

### 7.4 OME Metadata Integration

#### 7.4.1 OME-Zarr FileObjects

```json
{
  "@type": "cr:FileObject",
  "@id": "ome_zarr_store",
  "name": "OME-Zarr Image Collection",
  "contentUrl": "https://example.org/data/images.zarr",
  "encodingFormat": "application/zarr",
  "bioimg:omeFormat": "OME-Zarr",
  "bioimg:omeZarrVersion": "0.4",
  "bioimg:pyramidLevels": 5,
  "bioimg:chunkSize": [1, 1, 1, 256, 256],
  "bioimg:compressionCodec": "blosc",
  "description": "OME-Zarr format microscopy images with multi-resolution pyramid"
}
```

#### 7.4.2 OME-XML Reference

Bio-Croissant datasets MAY reference external OME-XML metadata:

```json
{
  "bioimg:omeXmlReference": {
    "@type": "cr:FileObject",
    "@id": "ome_xml_metadata",
    "contentUrl": "https://example.org/data/metadata.ome.xml",
    "encodingFormat": "application/ome+xml",
    "bioimg:omeXmlVersion": "2016-06"
  },
  "bioimg:omeXmlIntegration": "reference-only"
}
```

Integration modes:
- `"reference-only"`: OME-XML exists separately, not duplicated in Bio-Croissant
- `"embedded"`: OME-XML content embedded in Bio-Croissant metadata
- `"synchronized"`: Both maintained with automated synchronization

### 7.5 Extraction Mechanisms

#### 7.5.1 Zarr Array Path

```json
{
  "source": {
    "fileObject": { "@id": "zarr_store" },
    "extract": {
      "bioimg:zarrPath": "/image/0",
      "bioimg:zarrResolution": 0
    }
  }
}
```

#### 7.5.2 HDF5 Dataset Path

```json
{
  "source": {
    "fileObject": { "@id": "hdf5_file" },
    "extract": {
      "bioimg:hdf5Path": "/experiment1/images/channel_0"
    }
  }
}
```

#### 7.5.3 Multi-File TIFF Series

```json
{
  "source": {
    "fileSet": { "@id": "tiff_series" },
    "extract": {
      "bioimg:tiffPattern": "image_{t:03d}_z{z:03d}.tif",
      "bioimg:dimensionMapping": {
        "T": "t",
        "Z": "z"
      }
    }
  }
}
```

### 7.6 Region of Interest (ROI)

```json
{
  "@type": "cr:Field",
  "@id": "annotations/cell_roi",
  "name": "Cell Segmentation ROI",
  "dataType": "bioimg:ROI",
  "description": "Cell boundary polygons from automated segmentation",
  "repeated": true,
  "bioimg:roiType": "polygon",
  "bioimg:roiFormat": "XY-coordinates",
  "bioimg:coordinateSystem": "pixel",
  "bioimg:referenceFrame": {
    "@id": "images/microscopy_image"
  },
  "source": {
    "fileObject": { "@id": "roi_annotations_json" },
    "extract": {
      "jsonPath": "$.cells[*].boundary"
    }
  }
}
```

### 7.7 Segmentation Masks

```json
{
  "@type": "cr:Field",
  "@id": "segmentation/nuclear_mask",
  "name": "Nuclear Segmentation",
  "dataType": "bioimg:Mask",
  "description": "Nuclear segmentation label image",
  "bioimg:dimensions": {
    "T": 10,
    "Z": 50,
    "Y": 1024,
    "X": 1024
  },
  "bioimg:dimensionOrder": "TZYX",
  "bioimg:pixelFormat": "uint32",
  "bioimg:maskType": "label",
  "bioimg:backgroundLabel": 0,
  "bioimg:labelSemantics": "instance",
  "source": {
    "fileObject": { "@id": "segmentation_zarr" },
    "extract": {
      "bioimg:zarrPath": "/labels/nuclei"
    }
  }
}
```

Mask types:
- `"label"`: Instance segmentation (each object has unique integer ID)
- `"binary"`: Binary mask (0=background, 1=foreground)
- `"probability"`: Probability map (0.0-1.0 float values)
- `"multi-class"`: Semantic segmentation (integer class IDs)

---

## 8. Whole Slide Imaging Extension

### 8.1 Overview

The WSI extension supports digital pathology whole slide images with multi-resolution pyramids, tile-based access, and pathologist annotations.

### 8.2 WSI Dataset Properties

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `wsi:scannerManufacturer` | Text | ONE | "Aperio", "Hamamatsu", "3DHistech", "Leica" |
| `wsi:scannerModel` | Text | ONE | Scanner model name |
| `wsi:magnification` | Number | ONE | Objective lens magnification (e.g., 20, 40) |
| `wsi:tissueType` | Text or URL | MANY | Tissue types in dataset |
| `wsi:stainType` | Text or URL | MANY | "H&E", "IHC", "IF", "PAS", etc. |
| `wsi:preparationType` | Text | ONE | "FFPE", "frozen", "cytology" |

### 8.3 WSI Field Properties

For fields with `dataType` of `wsi:WholeSlideImage`:

| Property | Type | Cardinality | Description |
|----------|------|-------------|-------------|
| `wsi:pyramidLevels` | Integer | ONE | Number of resolution levels (typically 6-10) |
| `wsi:baseMagnification` | Number | ONE | Magnification at level 0 (highest resolution) |
| `wsi:tileWidth` | Integer | ONE | Tile width in pixels (typically 256 or 512) |
| `wsi:tileHeight` | Integer | ONE | Tile height in pixels |
| `wsi:slideWidth` | Integer | ONE | Full slide width at base resolution (pixels) |
| `wsi:slideHeight` | Integer | ONE | Full slide height at base resolution (pixels) |
| `wsi:mppX` | Number | ONE | Microns per pixel in X at base resolution |
| `wsi:mppY` | Number | ONE | Microns per pixel in Y at base resolution |
| `wsi:compressionFormat` | Text | ONE | "JPEG", "JPEG2000", "LZW", "uncompressed" |
| `wsi:colorSpace` | Text | ONE | "RGB", "grayscale", "CYMK" |
| `wsi:bitsPerSample` | Integer | ONE | Bits per channel (typically 8) |

### 8.4 Tile Access Patterns

#### 8.4.1 TileLocator Data Type

```json
{
  "@type": "cr:Field",
  "@id": "tiles/location",
  "name": "Tile Coordinates",
  "dataType": "wsi:TileLocator",
  "description": "Tile extraction coordinates for patch-based training",
  "repeated": true,
  "wsi:tileSize": 512,
  "wsi:pyramidLevel": 0,
  "wsi:overlapPixels": 0,
  "subField": [
    {
      "@type": "cr:Field",
      "@id": "tiles/location/x",
      "name": "x",
      "dataType": "sc:Integer",
      "description": "X coordinate (top-left corner)",
      "source": {
        "fileObject": { "@id": "tile_manifest" },
        "extract": { "column": "x_coord" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "tiles/location/y",
      "name": "y",
      "dataType": "sc:Integer",
      "description": "Y coordinate (top-left corner)",
      "source": {
        "fileObject": { "@id": "tile_manifest" },
        "extract": { "column": "y_coord" }
      }
    }
  ]
}
```

#### 8.4.2 Tile Extraction

```json
{
  "source": {
    "fileObject": { "@id": "whole_slide_image_svs" },
    "extract": {
      "wsi:extractTile": {
        "level": 0,
        "x": { "@id": "tiles/location/x" },
        "y": { "@id": "tiles/location/y" },
        "width": 512,
        "height": 512
      }
    }
  }
}
```

### 8.5 Pathologist Annotations

```json
{
  "@type": "cr:Field",
  "@id": "annotations/tumor_regions",
  "name": "Tumor Region Annotations",
  "dataType": "wsi:Annotation",
  "description": "Invasive tumor areas annotated by pathologists",
  "repeated": true,
  "wsi:annotationType": "polygon",
  "wsi:annotationClass": "invasive_tumor",
  "wsi:annotator": {
    "@type": "sc:Person",
    "name": "Board-Certified Pathologist",
    "bio:deidentificationNote": "Specific pathologist ID removed"
  },
  "wsi:annotationDate": "2025-03",
  "wsi:coordinateSystem": "base-level-pixels",
  "source": {
    "fileObject": { "@id": "annotations_geojson" },
    "extract": {
      "jsonPath": "$.features[?(@.properties.class=='invasive_tumor')].geometry.coordinates"
    }
  }
}
```

Annotation types:
- `"polygon"`: Closed polygon vertices
- `"point"`: Point markers
- `"line"`: Line segments
- `"rectangle"`: Bounding boxes
- `"freehand"`: Freehand drawings

### 8.6 WSI Format Support

Supported formats (via `encodingFormat`):

| Format | MIME Type | Description |
|--------|-----------|-------------|
| Aperio SVS | `image/svs` | Aperio ScanScope Virtual Slide |
| Hamamatsu NDPI | `image/ndpi` | Hamamatsu NanoZoomer Digital Pathology |
| 3DHistech MRXS | `image/mrxs` | 3DHistech Pannoramic Scanner |
| Generic TIFF | `image/tiff` | Tiled pyramidal TIFF |
| DICOM WSI | `application/dicom` | DICOM Whole Slide Imaging |
| Zarr | `application/zarr` | Zarr-based WSI (emerging) |

---

## 9. Cross-Domain Features

### 9.1 FHIR Integration

Bio-Croissant datasets MAY reference FHIR resources for clinical context:

```json
{
  "bio:fhirServer": "https://fhir.example.org/r4",
  "bio:fhirVersion": "4.0.1",
  "fhir:relatedResources": [
    {
      "@type": "fhir:Patient",
      "fhir:resourceReference": "Patient/example-123",
      "bio:linkageMethod": "deterministic",
      "bio:deidentificationNote": "FHIR Patient.id is de-identified hash"
    },
    {
      "@type": "fhir:Observation",
      "fhir:resourceReference": "Observation?patient=example-123",
      "bio:included": false,
      "bio:availableOnRequest": true
    }
  ]
}
```

RecordSets MAY link to FHIR profiles:

```json
{
  "@type": "cr:RecordSet",
  "@id": "patients",
  "fhir:conformsToProfile": "http://hl7.org/fhir/StructureDefinition/Patient",
  "field": [
    {
      "@id": "patients/identifier",
      "fhir:mapsToElement": "Patient.identifier"
    }
  ]
}
```

### 9.2 BioSchemas Integration

Level 3 conformant datasets SHOULD use BioSchemas dual typing:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "bioschemas": "https://bioschemas.org/"
  },
  "@type": ["sc:Dataset", "bioschemas:Dataset"],
  "bioschemas:taxonomicRange": [
    {
      "@type": "bioschemas:Taxon",
      "@id": "http://purl.obolibrary.org/obo/NCBITaxon_9606",
      "name": "Homo sapiens"
    }
  ],
  "bioschemas:measurementTechnique": [
    {
      "@type": "bioschemas:MeasurementTechnique",
      "@id": "http://purl.obolibrary.org/obo/OBI_0000070",
      "name": "genotyping assay"
    }
  ],
  "bioschemas:variableMeasured": [
    {
      "@type": "sc:PropertyValue",
      "name": "tumor grade",
      "propertyID": "http://purl.obolibrary.org/obo/NCIT_C28076"
    }
  ]
}
```

### 9.3 Provenance and Lineage

Bio-Croissant integrates W3C PROV for data provenance:

```json
{
  "prov:wasGeneratedBy": {
    "@type": "prov:Activity",
    "@id": "data-generation-activity",
    "prov:startedAtTime": "2024-01-01T00:00:00Z",
    "prov:endedAtTime": "2024-12-31T23:59:59Z",
    "prov:used": [
      {
        "@type": "prov:Entity",
        "@id": "source-ehr-system",
        "name": "Hospital EHR System v3.2"
      }
    ],
    "prov:wasAssociatedWith": {
      "@type": "prov:Agent",
      "@id": "data-engineering-team",
      "name": "Clinical Data Engineering Team"
    }
  },
  "prov:wasDerivedFrom": {
    "@type": "prov:Entity",
    "@id": "https://example.org/source-dataset",
    "name": "Source Clinical Database"
  },
  "bio:transformationsPipeline": [
    {
      "@type": "prov:Activity",
      "name": "De-identification",
      "bio:method": "HIPAA Safe Harbor",
      "bio:software": "deidentification-tool v2.1",
      "prov:startedAtTime": "2024-11-01T00:00:00Z"
    },
    {
      "@type": "prov:Activity",
      "name": "OMOP CDM Transformation",
      "bio:software": "omop-etl v5.4.2",
      "prov:startedAtTime": "2024-11-15T00:00:00Z"
    }
  ]
}
```

### 9.4 Quality Metrics

Bio-Croissant supports dataset quality metadata:

```json
{
  "bio:qualityMetrics": {
    "bio:completeness": {
      "overall": 0.95,
      "byTable": {
        "PERSON": 1.0,
        "DRUG_EXPOSURE": 0.92,
        "MEASUREMENT": 0.88
      }
    },
    "bio:consistency": {
      "foreignKeyIntegrity": 0.998,
      "dateConsistency": 0.995
    },
    "bio:validity": {
      "conceptMapping": 0.96,
      "dataTypeConformance": 0.99
    },
    "bio:knownLimitations": [
      "Lab measurements missing for 12% of patients pre-2020",
      "Prescription data incomplete for outpatient settings"
    ],
    "bio:qualityAssessmentDate": "2025-11-30",
    "bio:qualityAssessmentMethod": "Automated DQA tool v2.0 + manual review"
  }
}
```

Quality dimensions (following ISO 25012):
- **Completeness**: Proportion of required data present
- **Consistency**: Logical consistency and constraint satisfaction
- **Validity**: Conformance to defined formats and vocabularies
- **Accuracy**: (if ground truth available) Agreement with truth
- **Timeliness**: How current the data is

---

## 10. Validation and Quality

### 10.1 JSON-LD Validation

All Bio-Croissant metadata MUST:

1. Be valid JSON
2. Be valid JSON-LD 1.1
3. Successfully expand using standard JSON-LD processor
4. Resolve all `@context` references

### 10.2 Schema Validation

Bio-Croissant provides JSON Schema for structural validation. Validators SHOULD check:

#### 10.2.1 Required Properties

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["@context", "@type", "dct:conformsTo", "name", "description", "license"],
  "properties": {
    "dct:conformsTo": {
      "type": "array",
      "contains": {
        "const": "http://mlcommons.org/croissant/bio/0.2"
      }
    },
    "bio:dataCategory": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["clinical", "imaging", "omics", "pathology", "cellular", "molecular", "animal", "synthetic"]
      },
      "minItems": 1
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "bio:dataCategory": {
            "contains": {
              "enum": ["clinical", "patient", "human"]
            }
          }
        }
      },
      "then": {
        "required": ["bio:deidentificationMethod"]
      }
    }
  ]
}
```

#### 10.2.2 OMOP Extension Validation

If `"omop"` in `bio:extensions`:

```json
{
  "required": ["omop:cdmVersion", "omop:vocabularyVersion", "omop:cdmSourceName"],
  "properties": {
    "recordSet": {
      "type": "array",
      "items": {
        "if": {
          "properties": {
            "omop:cdmTable": { "type": "string" }
          },
          "required": ["omop:cdmTable"]
        },
        "then": {
          "required": ["omop:tableDomain"]
        }
      }
    }
  }
}
```

Complete JSON Schema in Appendix B.

### 10.3 Semantic Validation

Validators SHOULD verify:

1. **Foreign Key Integrity**: All `references` point to existing RecordSet fields
2. **Vocabulary Consistency**: Concept domains match vocabulary types
3. **Data Type Compatibility**: Base types support declared semantic types
4. **Unit Compatibility**: Physical units are valid UCUM codes

### 10.4 Validation Checklist

Before publishing Bio-Croissant metadata:

**Basic Validation:**
- [ ] Valid JSON syntax
- [ ] Valid JSON-LD 1.1
- [ ] Passes JSON Schema validation
- [ ] All `@context` URIs resolve
- [ ] Conforms to declared Bio-Croissant version

**Content Validation:**
- [ ] All required properties present
- [ ] Conditional requirements satisfied
- [ ] Data categories are valid
- [ ] If human data: de-identification method specified
- [ ] If authenticated: access control mechanism specified

**Domain Validation:**
- [ ] If OMOP: vocabulary versions specified
- [ ] If imaging: physical dimensions provided
- [ ] If WSI: scanner information complete
- [ ] All foreign keys reference existing fields

**Quality Validation:**
- [ ] File checksums (SHA256) provided for all FileObjects
- [ ] License is valid SPDX identifier or URL
- [ ] Creator information complete
- [ ] Citation information provided

**Best Practices:**
- [ ] Examples provided for complex RecordSets
- [ ] Known limitations documented
- [ ] Quality metrics included
- [ ] Provenance information provided

---

## 11. Implementation Guidance

### 11.1 Creating Bio-Croissant Metadata

#### 11.1.1 Recommended Tools

**Editors:**
- **Croissant Editor**: Web-based visual editor (extend for Bio-Croissant)
- **JSON-LD Playground**: Validate JSON-LD syntax
- **VS Code with JSON Schema**: Use provided schema for auto-completion

**Libraries:**
- **Python**: `mlcroissant` library (plan Bio-Croissant extension)
- **JavaScript**: JSON-LD libraries + custom validation
- **R**: `jsonlite` + custom Bio-Croissant functions

#### 11.1.2 Creation Workflow

1. **Start from Template**:
   - Choose appropriate example from Section 12
   - Copy and modify for your dataset

2. **Dataset-Level Metadata**:
   - Set name, description, license, creators
   - Declare data categories
   - Add de-identification if applicable

3. **Define Distribution**:
   - Create FileObject entries for each data file
   - Add checksums (SHA256)
   - Specify encoding formats

4. **Model RecordSets**:
   - One RecordSet per logical table/collection
   - Define primary keys
   - Map to domain tables (if OMOP/FHIR)

5. **Define Fields**:
   - Map fields to data sources
   - Add semantic types
   - Document vocabularies
   - Create foreign key references

6. **Validate**:
   - JSON syntax validation
   - JSON-LD expansion
   - Schema validation
   - Manual review of examples

7. **Document**:
   - Add examples to RecordSets
   - Document known limitations
   - Provide quality metrics

### 11.2 Loading Bio-Croissant Datasets

#### 11.2.1 Python Example

```python
import mlcroissant as cr
import biocroissant  # hypothetical extension

# Load metadata
dataset = cr.Dataset.from_file("dataset.json")

# Access OMOP extension
if dataset.has_extension("omop"):
    omop = biocroissant.OMOPExtension(dataset)

    # Get person table as pandas DataFrame
    persons = omop.load_recordset("person")

    # Follow foreign keys
    conditions = omop.load_recordset("condition_occurrence")
    conditions_with_names = omop.join_concepts(
        conditions,
        concept_field="condition_concept_id"
    )

# Access imaging extension
if dataset.has_extension("bioimaging"):
    imaging = biocroissant.ImagingExtension(dataset)

    # Load 5D array
    images = imaging.load_recordset("images")
    image_array = images.get_field("image_array").load()
    # Returns numpy array or dask array for large data
```

#### 11.2.2 Lazy Loading

Implementations SHOULD support lazy loading:

```python
# Don't load entire dataset into memory
dataset = cr.Dataset.from_file("large_wsi_dataset.json")
wsi_ext = biocroissant.WSIExtension(dataset)

# Load only specific tiles
for tile_coord in wsi_ext.get_tile_manifest("slides"):
    tile_image = wsi_ext.load_tile(
        slide_id=tile_coord["slide_id"],
        x=tile_coord["x"],
        y=tile_coord["y"],
        level=0,
        size=512
    )
    # Process tile...
```

### 11.3 Framework Integration

#### 11.3.1 PyTorch Dataset

```python
from torch.utils.data import Dataset

class BioCroissantDataset(Dataset):
    def __init__(self, croissant_file, recordset_name):
        self.dataset = cr.Dataset.from_file(croissant_file)
        self.recordset = self.dataset.recordset[recordset_name]

    def __len__(self):
        return len(self.recordset)

    def __getitem__(self, idx):
        record = self.recordset.get_record(idx)
        # Convert to tensors based on data types
        return {
            "features": record.to_tensor(),
            "label": record["label"]
        }
```

#### 11.3.2 TensorFlow Dataset

```python
import tensorflow as tf

def biocroissant_generator(croissant_file, recordset_name):
    dataset = cr.Dataset.from_file(croissant_file)
    recordset = dataset.recordset[recordset_name]

    for record in recordset:
        yield record.to_dict()

# Create TF dataset
tf_dataset = tf.data.Dataset.from_generator(
    lambda: biocroissant_generator("dataset.json", "images"),
    output_signature={
        "image": tf.TensorSpec(shape=(1024, 1024, 3), dtype=tf.uint8),
        "label": tf.TensorSpec(shape=(), dtype=tf.int32)
    }
)
```

### 11.4 Error Handling

Implementations SHOULD provide clear error messages:

```python
# Good error handling
try:
    dataset = cr.Dataset.from_file("dataset.json")
except cr.ValidationError as e:
    if "bio:deidentificationMethod" in str(e):
        print("Error: Human subjects data requires de-identification method.")
        print(f"Data categories: {dataset.get('bio:dataCategory')}")
        print("Add 'bio:deidentificationMethod' to dataset metadata.")
    else:
        print(f"Validation error: {e}")
```

### 11.5 Versioning and Compatibility

#### 11.5.1 Reading Newer Minor Versions

Implementations SHOULD accept minor version increments:

```python
# Can read 0.2.x when implementation supports 0.2.0
declared_version = dataset.get("dct:conformsTo")
if "bio/0.2" in declared_version or "bio/0.3" in declared_version:
    # Compatible - proceed
    pass
```

#### 11.5.2 Migration from v0.1 to v0.2

Key changes:
1. Namespaces now versioned (`bio/0.2/` vs `bio/`)
2. `bio:deidentificationMethod` now conditional
3. New provenance properties optional
4. Complete JSON-LD context required

Migration script should:
1. Update namespace URIs
2. Add complete `@context`
3. Remove `bio:deidentificationMethod` if not human data
4. Validate against v0.2 schema

---

## 12. Examples

Complete, validated examples are provided in the `examples/` directory:

### 12.1 OMOP CDM Synthetic Dataset
**File:** `examples/omop_cdm_synthetic_v0.2.json`

Demonstrates:
- OMOP CDM v5.4 metadata
- Multiple clinical tables with foreign keys
- Vocabulary references with versions
- De-identification documentation
- Provenance information

### 12.2 High-Content Screening Microscopy
**File:** `examples/microscopy_hcs_v0.2.json`

Demonstrates:
- 5D imaging data (TCZYX)
- OME-Zarr integration
- Channel metadata
- Segmentation masks
- Single-cell measurements

### 12.3 Digital Pathology WSI
**File:** `examples/pathology_wsi_v0.2.json`

Demonstrates:
- Whole slide images with pyramids
- Pathologist annotations
- Tile extraction manifests
- Clinical metadata integration
- Access control declarations

### 12.4 Multi-Omics Dataset
**File:** `examples/multi_omics_v0.2.json`

Demonstrates:
- Genomics (VCF) + proteomics integration
- FHIR resource references
- BioSchemas typing
- Cross-modal linking

---

## 13. Appendices

### Appendix A: Complete JSON-LD Context

See separate file: `context/biocroissant-v0.2-context.jsonld`

### Appendix B: JSON Schema

See separate file: `schema/biocroissant-v0.2-schema.json`

### Appendix C: OMOP CDM v5.4 Complete Table Mapping

| OMOP Table | Bio-Croissant RecordSet Pattern | Distribution | Domain |
|------------|--------------------------------|--------------|--------|
| PERSON | `person` | person_id | Clinical |
| OBSERVATION_PERIOD | `observation_period` | person_id | Clinical |
| VISIT_OCCURRENCE | `visit_occurrence` | person_id | Clinical |
| VISIT_DETAIL | `visit_detail` | person_id | Clinical |
| CONDITION_OCCURRENCE | `condition_occurrence` | person_id | Clinical |
| DRUG_EXPOSURE | `drug_exposure` | person_id | Clinical |
| PROCEDURE_OCCURRENCE | `procedure_occurrence` | person_id | Clinical |
| DEVICE_EXPOSURE | `device_exposure` | person_id | Clinical |
| MEASUREMENT | `measurement` | person_id | Clinical |
| OBSERVATION | `observation` | person_id | Clinical |
| DEATH | `death` | person_id | Clinical |
| NOTE | `note` | person_id | Clinical |
| NOTE_NLP | `note_nlp` | RANDOM | Clinical |
| SPECIMEN | `specimen` | person_id | Clinical |
| FACT_RELATIONSHIP | `fact_relationship` | RANDOM | Clinical |
| LOCATION | `location` | RANDOM | System |
| CARE_SITE | `care_site` | RANDOM | System |
| PROVIDER | `provider` | RANDOM | System |
| PAYER_PLAN_PERIOD | `payer_plan_period` | person_id | Economics |
| COST | `cost` | RANDOM | Economics |
| DRUG_ERA | `drug_era` | person_id | Derived |
| DOSE_ERA | `dose_era` | person_id | Derived |
| CONDITION_ERA | `condition_era` | person_id | Derived |
| EPISODE | `episode` | person_id | Derived |
| EPISODE_EVENT | `episode_event` | RANDOM | Derived |
| METADATA | `metadata` | RANDOM | Vocabulary |
| CDM_SOURCE | `cdm_source` | RANDOM | Vocabulary |
| CONCEPT | `concept` | RANDOM | Vocabulary |
| VOCABULARY | `vocabulary` | RANDOM | Vocabulary |
| DOMAIN | `domain` | RANDOM | Vocabulary |
| CONCEPT_CLASS | `concept_class` | RANDOM | Vocabulary |
| CONCEPT_RELATIONSHIP | `concept_relationship` | RANDOM | Vocabulary |
| RELATIONSHIP | `relationship` | RANDOM | Vocabulary |
| CONCEPT_SYNONYM | `concept_synonym` | RANDOM | Vocabulary |
| CONCEPT_ANCESTOR | `concept_ancestor` | RANDOM | Vocabulary |
| SOURCE_TO_CONCEPT_MAP | `source_to_concept_map` | RANDOM | Vocabulary |
| DRUG_STRENGTH | `drug_strength` | RANDOM | Vocabulary |
| COHORT | `cohort` | RANDOM | Analysis |
| COHORT_DEFINITION | `cohort_definition` | RANDOM | Analysis |

### Appendix D: Imaging Format Support Matrix

| Format | Extension | MIME Type | Bio-Croissant Support | Notes |
|--------|-----------|-----------|---------------------|-------|
| OME-TIFF | .ome.tif | image/tiff | Full | Preferred for microscopy |
| OME-Zarr | .zarr | application/zarr | Full | Preferred for large/cloud |
| HDF5 | .h5, .hdf5 | application/x-hdf5 | Full | Common in research |
| TIFF Series | .tif | image/tiff | Full | Multi-file support |
| Aperio SVS | .svs | image/svs | Full (WSI) | Digital pathology |
| Hamamatsu NDPI | .ndpi | image/ndpi | Full (WSI) | Digital pathology |
| 3DHistech MRXS | .mrxs | image/mrxs | Full (WSI) | Digital pathology |
| Leica SCN | .scn | image/scn | Full (WSI) | Digital pathology |
| DICOM | .dcm | application/dicom | Partial | Via WSI extension |
| BigDataViewer | .xml | application/xml | Planned | Future support |

### Appendix E: Data Use Ontology (DUO) Common Terms

| DUO Term | ID | Description |
|----------|-----|-------------|
| General Research Use | DUO_0000042 | Data available for general research use |
| Health/Medical/Biomedical Research | DUO_0000006 | Data limited to health/medical/biomedical research |
| Disease-Specific Research | DUO_0000007 | Data limited to research on specific disease |
| Population Origins/Ancestry Research Only | DUO_0000011 | Data limited to population research |
| Not-for-profit Use Only | DUO_0000046 | Data limited to non-commercial use |
| User-Specific Restriction | DUO_0000026 | Data requires specific approval |
| Publication Required | DUO_0000019 | Requestor must provide publication |
| Collaboration Required | DUO_0000020 | Requires collaboration with data provider |
| Ethics Approval Required | DUO_0000021 | Requires local ethics approval |
| Geographical Restriction | DUO_0000022 | Limited to specific geography |
| Publication Moratorium | DUO_0000024 | Publication embargo for period |
| Return to Database/Archive | DUO_0000029 | Derived data must be returned |

### Appendix F: Change Log

**Version 0.2.0 (December 2025)**
- Made `bio:deidentificationMethod` conditional on human subjects data
- Added complete JSON-LD context with all property mappings
- Defined explicit conformance level requirements
- Clarified data types as semantic annotations
- Added OMOP extraction mechanisms section
- Added OME metadata integration details
- Added FHIR integration section
- Added provenance and quality metrics sections
- Added validation rules and JSON Schema
- Added implementation guidance
- Versioned all namespaces
- Added error handling guidance

**Version 0.1.0 (December 2025)**
- Initial draft specification
- OMOP CDM v5.4 support
- Bioimaging extensions
- Whole slide imaging extensions
- BioSchemas alignment
- Security and privacy framework

### Appendix G: Future Roadmap

**Planned for v0.3 (Q2 2026):**
- Genomics extension (VCF, BAM, FASTQ)
- Proteomics extension (mzML, MGF)
- Electronic phenotyping algorithms
- Federated learning metadata
- Differential privacy parameters

**Planned for v1.0 (Q4 2026):**
- Clinical trials integration (ClinicalTrials.gov)
- Real-world evidence (RWE) specific metadata
- Model cards integration
- Audit trail requirements
- Certified conformance testing

**Under Consideration:**
- Synthetic data generation parameters
- Active learning metadata
- Multi-modal fusion specifications
- Temporal event sequences
- Causal inference metadata

---

## References

1. MLCommons Croissant Format Specification v1.0: https://docs.mlcommons.org/croissant/
2. OMOP Common Data Model v5.4: https://ohdsi.github.io/CommonDataModel/
3. BioSchemas: https://bioschemas.org/
4. OME Data Model: https://www.openmicroscopy.org/
5. OME-Zarr Specification: https://ngff.openmicroscopy.org/
6. Data Use Ontology (DUO): http://www.obofoundry.org/ontology/duo.html
7. HIPAA De-identification: https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/
8. FHIR R4: http://hl7.org/fhir/R4/
9. W3C PROV-O: https://www.w3.org/TR/prov-o/
10. JSON-LD 1.1: https://www.w3.org/TR/json-ld11/
11. ISO 25012 Data Quality: https://iso25000.com/index.php/en/iso-25000-standards/iso-25012

---

## Acknowledgments

This specification builds on the excellent work of the MLCommons Croissant team and incorporates input from the OHDSI, OME, BioSchemas, and GA4GH communities.

## Contact

Bio-Croissant Working Group: biocroissant@mlcommons.org

---

**Document Status**: Updated Working Draft
**Last Updated**: December 4, 2025
**Next Review**: March 2026

---

**Copyright © 2025 MLCommons Bio-Croissant Working Group**

This document is licensed under the MIT License.
