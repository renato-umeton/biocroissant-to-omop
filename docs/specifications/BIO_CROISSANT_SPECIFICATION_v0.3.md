# Bio-Croissant Metadata Format Specification v0.3

**Version:** 0.3
**Status:** Candidate Recommendation
**Date:** 2025-12-04
**Previous Version:** [v0.2](./BIO_CROISSANT_SPECIFICATION_v0.2.md)

## Abstract

Bio-Croissant v0.3 extends the MLCommons Croissant metadata format for biomedical and healthcare machine learning datasets with **ISO/IEC 11179 metadata registry** capabilities. This version adds data governance, value domain management, and semantic clarity following international metadata standards.

## Table of Contents

1. [Introduction](#1-introduction)
2. [ISO 11179 Metadata Registry Framework](#2-iso-11179-metadata-registry-framework)
3. [Namespaces and Conformance](#3-namespaces-and-conformance)
4. [Administrative Metadata](#4-administrative-metadata)
5. [Value Domains and Conceptual Domains](#5-value-domains-and-conceptual-domains)
6. [Data Element Concepts](#6-data-element-concepts)
7. [Classification Schemes](#7-classification-schemes)
8. [Core Bio-Croissant Extensions](#8-core-bio-croissant-extensions)
9. [OMOP CDM Support](#9-omop-cdm-support)
10. [Bioimaging Extension](#10-bioimaging-extension)
11. [Whole Slide Imaging Extension](#11-whole-slide-imaging-extension)
12. [Implementation Guidance](#12-implementation-guidance)
13. [Appendices](#13-appendices)

---

## 1. Introduction

### 1.1 Motivation

Bio-Croissant v0.3 addresses the need for **standardized metadata governance** in biomedical ML datasets by adopting [ISO/IEC 11179](https://www.iso.org/standard/78914.html) metadata registry principles. This enables:

- **Semantic clarity** through data element concepts separated from representation
- **Value domain management** with controlled vocabularies
- **Data governance** with stewardship and registration metadata
- **Interoperability** through standardized naming and definitions
- **Quality assurance** via administrative metadata and lifecycle management

### 1.2 Relationship to Standards

Bio-Croissant v0.3 builds upon:

- **MLCommons Croissant 1.0** - Base ML dataset metadata format
- **ISO/IEC 11179** ([Parts 1](https://www.iso.org/standard/78914.html), [3](https://www.iso.org/standard/78925.html), [5](https://www.iso.org/standard/60341.html), [6](https://www.iso.org/standard/78916.html)) - Metadata registry framework
- **Schema.org** - General-purpose vocabulary
- **OMOP CDM v5.4** - Clinical data standardization
- **OME** - Bioimaging data model
- **DICOM** - Medical imaging standards
- **FHIR R5** - Healthcare interoperability

### 1.3 Changes from v0.2

Major additions in v0.3:

1. **ISO 11179 metadata registry** support with administrative metadata
2. **Value domains** with permissible values and datatypes
3. **Conceptual domains** for semantic value meanings
4. **Data element concepts** separating semantics from representation
5. **Classification schemes** for organizing biomedical metadata
6. **Registration authority** and governance metadata
7. **Stewardship metadata** for data provenance and responsibility
8. **Enhanced definitions** following ISO 11179-4 principles

---

## 2. ISO 11179 Metadata Registry Framework

### 2.1 Overview

ISO/IEC 11179 defines a [metadata registry metamodel](https://help.aristotlecloud.io/subject-matter-and-theory/iso-iec-11179-data-element-representation) where:

- **Data Element** = Data Element Concept + Value Domain
- **Data Element Concept** = Object Class + Property (semantic meaning)
- **Value Domain** = Datatype + Permissible Values (representation)
- **Conceptual Domain** = Set of value meanings (independent of representation)

### 2.2 Bio-Croissant ISO 11179 Namespace

```
Prefix: iso11179
URI: http://mlcommons.org/croissant/bio/iso11179/0.3/
```

### 2.3 Core ISO 11179 Concepts in Bio-Croissant

Bio-Croissant fields can optionally include ISO 11179 metadata:

```json
{
  "@type": "cr:Field",
  "@id": "person/gender",
  "name": "Person Gender",
  "description": "The biological sex of a person at birth",
  "dataType": "sc:Text",

  "iso11179:dataElementConcept": {
    "@id": "dec:Person.GenderAtBirth",
    "iso11179:objectClass": "Person",
    "iso11179:property": "Gender at Birth",
    "iso11179:definition": "The biological sex classification of a person determined at birth"
  },

  "iso11179:valueDomain": {
    "@id": "vd:GenderCode",
    "iso11179:datatype": "Character 1",
    "iso11179:permissibleValues": [
      {"value": "M", "meaning": "Male"},
      {"value": "F", "meaning": "Female"},
      {"value": "U", "meaning": "Unknown"}
    ]
  }
}
```

---

## 3. Namespaces and Conformance

### 3.1 Required Namespaces

```json
{
  "@context": {
    "sc": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/",
    "dct": "http://purl.org/dc/terms/",
    "bio": "http://mlcommons.org/croissant/bio/0.3/",
    "iso11179": "http://mlcommons.org/croissant/bio/iso11179/0.3/"
  }
}
```

### 3.2 Conformance Declaration

Datasets MUST declare conformance to Bio-Croissant v0.3:

```json
{
  "dct:conformsTo": [
    "http://mlcommons.org/croissant/1.0",
    "http://mlcommons.org/croissant/bio/0.3"
  ]
}
```

### 3.3 Conformance Levels

**Level 1: Basic Bio-Croissant**
- Required: Core Bio-Croissant properties
- Optional: ISO 11179 metadata

**Level 2: ISO 11179 Enhanced**
- Required: Administrative metadata (steward, submitter)
- Required: Value domains for coded fields
- Recommended: Data element concepts

**Level 3: Full Metadata Registry**
- Required: Complete ISO 11179 metadata
- Required: Classification scheme membership
- Required: Registration authority metadata
- Required: All value domains and conceptual domains

---

## 4. Administrative Metadata

### 4.1 Dataset-Level Administrative Properties

Following ISO/IEC 11179-6 registration requirements:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `iso11179:registrationAuthority` | Organization | Level 2+ | Authority responsible for registration |
| `iso11179:registrationStatus` | Enum | Level 2+ | Lifecycle status (draft, candidate, standard, retired) |
| `iso11179:steward` | Person/Org | Level 2+ | Responsible for semantic accuracy |
| `iso11179:submitter` | Person/Org | Level 2+ | Who submitted the metadata |
| `iso11179:registeredDate` | DateTime | Level 2+ | Date of registration |
| `iso11179:lastReviewedDate` | DateTime | No | Date of last review |
| `iso11179:changeDescription` | Text | No | Summary of changes from previous version |

### 4.2 Example

```json
{
  "@type": "sc:Dataset",
  "name": "OMOP CDM Synthetic Dataset",

  "iso11179:registrationAuthority": {
    "@type": "sc:Organization",
    "name": "MLCommons Bio-Croissant Working Group",
    "url": "https://mlcommons.org/bio-croissant"
  },

  "iso11179:registrationStatus": "standard",

  "iso11179:steward": {
    "@type": "sc:Person",
    "name": "Dr. Jane Smith",
    "email": "j.smith@example.org",
    "affiliation": {
      "@type": "sc:Organization",
      "name": "Medical AI Research Center"
    }
  },

  "iso11179:submitter": {
    "@type": "sc:Person",
    "name": "Dr. John Doe",
    "email": "j.doe@example.org"
  },

  "iso11179:registeredDate": "2025-12-04T00:00:00Z",
  "iso11179:lastReviewedDate": "2025-12-04T00:00:00Z",
  "iso11179:changeDescription": "Initial v0.3 registration with ISO 11179 metadata"
}
```

---

## 5. Value Domains and Conceptual Domains

### 5.1 Value Domain Definition

A **Value Domain** specifies the representation of data values:

```typescript
interface ValueDomain {
  "@id": string;                    // Unique identifier
  "iso11179:datatype": string;      // Datatype (e.g., "Integer", "VARCHAR(50)")
  "iso11179:unitOfMeasure"?: string;
  "iso11179:format"?: string;       // Format specification
  "iso11179:maximumLength"?: number;
  "iso11179:permissibleValues"?: PermissibleValue[];
  "iso11179:conceptualDomain"?: {"@id": string};
}

interface PermissibleValue {
  "value": any;                     // Actual value
  "meaning": string;                // Semantic meaning
  "iso11179:valueMeaningId"?: string; // Link to conceptual domain
  "beginDate"?: string;             // Temporal validity
  "endDate"?: string;
}
```

### 5.2 Conceptual Domain Definition

A **Conceptual Domain** is a set of valid value meanings independent of representation:

```json
{
  "@type": "iso11179:ConceptualDomain",
  "@id": "cd:BiologicalSex",
  "name": "Biological Sex",
  "iso11179:definition": "The biological classification of organisms based on reproductive function",
  "iso11179:valueMeanings": [
    {
      "@id": "vm:Male",
      "name": "Male",
      "definition": "An organism that produces small, mobile gametes (sperm)"
    },
    {
      "@id": "vm:Female",
      "name": "Female",
      "definition": "An organism that produces large, immobile gametes (eggs)"
    },
    {
      "@id": "vm:Unknown",
      "name": "Unknown",
      "definition": "Biological sex is not known or not recorded"
    }
  ]
}
```

### 5.3 Standard Value Domains

Bio-Croissant v0.3 defines standard value domains:

#### 5.3.1 Clinical Data Categories

```json
{
  "@id": "vd:DataCategory",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "clinical", "meaning": "Patient clinical care data"},
    {"value": "imaging", "meaning": "Medical or biological imaging data"},
    {"value": "omics", "meaning": "Genomics, proteomics, metabolomics data"},
    {"value": "pathology", "meaning": "Anatomic pathology data"},
    {"value": "cellular", "meaning": "Cell-level biological data"},
    {"value": "molecular", "meaning": "Molecular structure and interaction data"},
    {"value": "animal", "meaning": "Animal model or veterinary data"},
    {"value": "synthetic", "meaning": "Computationally generated data"},
    {"value": "human", "meaning": "Human subject derived data"},
    {"value": "patient", "meaning": "Individual patient health data"}
  ]
}
```

#### 5.3.2 Registration Status

```json
{
  "@id": "vd:RegistrationStatus",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "draft", "meaning": "Under development, not yet reviewed"},
    {"value": "candidate", "meaning": "Submitted for review"},
    {"value": "standard", "meaning": "Approved and in active use"},
    {"value": "preferred", "meaning": "Recommended for new use cases"},
    {"value": "deprecated", "meaning": "Superseded but still valid"},
    {"value": "retired", "meaning": "No longer valid for use"}
  ]
}
```

#### 5.3.3 OMOP Concept Datatype

```json
{
  "@id": "vd:OMOPConceptID",
  "iso11179:datatype": "Integer",
  "iso11179:definition": "A unique identifier referencing a standardized concept in OMOP vocabulary",
  "iso11179:minimumValue": 0,
  "iso11179:maximumValue": 2147483647,
  "iso11179:conceptualDomain": {"@id": "cd:StandardizedConcept"}
}
```

---

## 6. Data Element Concepts

### 6.1 Definition

A **Data Element Concept** (DEC) represents the union of an Object Class and a Property, independent of representation.

Following ISO 11179 [naming principles](https://www.iso.org/standard/60341.html):

**Data Element Concept Name** = Object Class + Property

Examples:
- Person + Birth Date = "Person Birth Date"
- Patient + Body Weight = "Patient Body Weight"
- Cell + Nuclear Area = "Cell Nuclear Area"

### 6.2 Structure

```typescript
interface DataElementConcept {
  "@id": string;
  "iso11179:objectClass": string;
  "iso11179:property": string;
  "iso11179:definition": string;
  "iso11179:conceptualDomain": {"@id": string};
  "iso11179:classificationScheme"?: string[];
}
```

### 6.3 Examples

#### 6.3.1 Clinical Data Element Concept

```json
{
  "@id": "dec:Person.BirthDate",
  "iso11179:objectClass": "Person",
  "iso11179:property": "Birth Date",
  "iso11179:definition": "The calendar date on which a person was born",
  "iso11179:conceptualDomain": {"@id": "cd:CalendarDate"},
  "iso11179:classificationScheme": [
    "Demographics",
    "Temporal Information"
  ]
}
```

#### 6.3.2 Imaging Data Element Concept

```json
{
  "@id": "dec:MicroscopyImage.PhysicalSizeX",
  "iso11179:objectClass": "Microscopy Image",
  "iso11179:property": "Physical Size in X Dimension",
  "iso11179:definition": "The physical distance in micrometers represented by one pixel in the X dimension of a microscopy image",
  "iso11179:conceptualDomain": {"@id": "cd:PhysicalLength"},
  "iso11179:classificationScheme": [
    "Imaging Metadata",
    "Spatial Calibration"
  ]
}
```

### 6.4 Field-Level Data Element Concept Usage

```json
{
  "@type": "cr:Field",
  "@id": "person/birth_date",
  "name": "Birth Date",
  "description": "Date of birth for the person",
  "dataType": "sc:Date",

  "iso11179:dataElementConcept": {
    "@id": "dec:Person.BirthDate"
  },

  "iso11179:valueDomain": {
    "@id": "vd:ISO8601Date",
    "iso11179:datatype": "Date",
    "iso11179:format": "YYYY-MM-DD"
  },

  "source": {
    "fileObject": {"@id": "person_csv"},
    "extract": {"column": "birth_date"}
  }
}
```

---

## 7. Classification Schemes

### 7.1 Overview

Classification schemes organize metadata items into categories following ISO 11179-3.

### 7.2 Bio-Croissant Standard Classification Schemes

#### 7.2.1 Clinical Domain Classification

```json
{
  "@type": "iso11179:ClassificationScheme",
  "@id": "cs:ClinicalDomain",
  "name": "Clinical Data Domain Classification",
  "iso11179:classificationItems": [
    {
      "@id": "ci:Demographics",
      "name": "Demographics",
      "definition": "Patient demographic and identifying information"
    },
    {
      "@id": "ci:Diagnoses",
      "name": "Diagnoses and Conditions",
      "definition": "Disease diagnoses and health conditions"
    },
    {
      "@id": "ci:Procedures",
      "name": "Procedures and Interventions",
      "definition": "Medical procedures and therapeutic interventions"
    },
    {
      "@id": "ci:Medications",
      "name": "Medications and Exposures",
      "definition": "Drug exposures and pharmacological treatments"
    },
    {
      "@id": "ci:Observations",
      "name": "Observations and Measurements",
      "definition": "Clinical observations and measured values"
    }
  ]
}
```

#### 7.2.2 Imaging Modality Classification

```json
{
  "@type": "iso11179:ClassificationScheme",
  "@id": "cs:ImagingModality",
  "name": "Biomedical Imaging Modality Classification",
  "iso11179:classificationItems": [
    {
      "@id": "ci:LightMicroscopy",
      "name": "Light Microscopy",
      "definition": "Imaging using visible light wavelengths",
      "narrower": ["ci:Brightfield", "ci:Fluorescence", "ci:Confocal"]
    },
    {
      "@id": "ci:ElectronMicroscopy",
      "name": "Electron Microscopy",
      "definition": "Imaging using electron beams",
      "narrower": ["ci:TEM", "ci:SEM"]
    },
    {
      "@id": "ci:MedicalImaging",
      "name": "Medical Imaging",
      "definition": "Clinical diagnostic imaging",
      "narrower": ["ci:CT", "ci:MRI", "ci:PET", "ci:Ultrasound"]
    },
    {
      "@id": "ci:DigitalPathology",
      "name": "Digital Pathology",
      "definition": "Whole slide imaging of tissue specimens"
    }
  ]
}
```

### 7.3 Assigning Classification

```json
{
  "@type": "cr:RecordSet",
  "@id": "person",
  "name": "PERSON",
  "omop:cdmTable": "PERSON",

  "iso11179:classifiedBy": [
    {"@id": "ci:Demographics"},
    {"@id": "ci:ClinicalData"}
  ]
}
```

---

## 8. Core Bio-Croissant Extensions

### 8.1 Dataset-Level Properties

All properties from v0.2 are retained. Key properties enhanced with ISO 11179 metadata:

#### 8.1.1 bio:dataCategory

```json
{
  "bio:dataCategory": ["clinical", "imaging"],

  "iso11179:dataElementConcept": {
    "@id": "dec:Dataset.DataCategory",
    "iso11179:objectClass": "Dataset",
    "iso11179:property": "Data Category",
    "iso11179:definition": "The primary classification of data types contained in the dataset"
  },

  "iso11179:valueDomain": {"@id": "vd:DataCategory"}
}
```

#### 8.1.2 bio:deidentificationMethod

```json
{
  "bio:deidentificationMethod": "HIPAA Safe Harbor",

  "iso11179:dataElementConcept": {
    "@id": "dec:Dataset.DeidentificationMethod",
    "iso11179:objectClass": "Dataset",
    "iso11179:property": "Deidentification Method",
    "iso11179:definition": "The technique or standard used to remove personally identifiable information from the dataset"
  },

  "iso11179:valueDomain": {
    "@id": "vd:DeidentificationMethod",
    "iso11179:datatype": "Text",
    "iso11179:permissibleValues": [
      {"value": "HIPAA Safe Harbor", "meaning": "HIPAA Privacy Rule Safe Harbor method"},
      {"value": "HIPAA Expert Determination", "meaning": "HIPAA Privacy Rule Expert Determination"},
      {"value": "Anonymization", "meaning": "Irreversible removal of all identifiers"},
      {"value": "Pseudonymization", "meaning": "Replacement of identifiers with pseudonyms"},
      {"value": "Synthetic", "meaning": "Computationally generated non-real data"}
    ]
  }
}
```

### 8.2 Quality Metrics with Value Domains

```json
{
  "bio:qualityMetrics": {
    "bio:completeness": {
      "overall": 0.95,

      "iso11179:valueDomain": {
        "@id": "vd:CompletenessRatio",
        "iso11179:datatype": "Decimal",
        "iso11179:minimumValue": 0.0,
        "iso11179:maximumValue": 1.0,
        "iso11179:definition": "Proportion of required data elements that are populated"
      }
    }
  }
}
```

---

## 9. OMOP CDM Support

### 9.1 OMOP Value Domains

#### 9.1.1 OMOP Table Domain

```json
{
  "@id": "vd:OMOPTableDomain",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "Clinical", "meaning": "Patient-level clinical events and facts"},
    {"value": "Vocabulary", "meaning": "Standardized vocabulary and concept tables"},
    {"value": "Health Economics", "meaning": "Cost and payer information"},
    {"value": "Derived", "meaning": "Tables derived from clinical data"},
    {"value": "System", "meaning": "Metadata and system configuration"},
    {"value": "Analysis", "meaning": "Cohort and analysis results"}
  ]
}
```

#### 9.1.2 OMOP Database Dialect

```json
{
  "@id": "vd:OMOPDatabaseDialect",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "postgresql", "meaning": "PostgreSQL database"},
    {"value": "sql_server", "meaning": "Microsoft SQL Server"},
    {"value": "oracle", "meaning": "Oracle Database"},
    {"value": "redshift", "meaning": "Amazon Redshift"},
    {"value": "bigquery", "meaning": "Google BigQuery"},
    {"value": "snowflake", "meaning": "Snowflake Data Warehouse"}
  ]
}
```

### 9.2 OMOP Field with ISO 11179 Metadata

```json
{
  "@type": "cr:Field",
  "@id": "person/gender_concept_id",
  "name": "Gender Concept ID",
  "description": "Standard concept for biological sex at birth",
  "dataType": "sc:Integer",

  "omop:cdmField": "gender_concept_id",
  "omop:isRequired": true,
  "omop:foreignKeyTable": "CONCEPT",
  "omop:conceptDomain": "Gender",

  "iso11179:dataElementConcept": {
    "@id": "dec:Person.Gender",
    "iso11179:objectClass": "Person",
    "iso11179:property": "Gender",
    "iso11179:definition": "The biological sex of a person as determined at birth"
  },

  "iso11179:valueDomain": {
    "@id": "vd:OMOPConceptID",
    "iso11179:datatype": "Integer",
    "iso11179:conceptualDomain": {"@id": "cd:OMOPGenderConcept"},
    "iso11179:permissibleValues": [
      {"value": 8507, "meaning": "Male"},
      {"value": 8532, "meaning": "Female"},
      {"value": 0, "meaning": "No matching concept"}
    ]
  }
}
```

---

## 10. Bioimaging Extension

### 10.1 Imaging Value Domains

#### 10.1.1 Dimensionality

```json
{
  "@id": "vd:ImageDimensionality",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "2D", "meaning": "Two-dimensional (X, Y)"},
    {"value": "3D", "meaning": "Three-dimensional (X, Y, Z)"},
    {"value": "4D", "meaning": "3D plus time (X, Y, Z, T)"},
    {"value": "5D", "meaning": "3D plus time and channels (X, Y, Z, T, C)"}
  ]
}
```

#### 10.1.2 Pixel Format

```json
{
  "@id": "vd:PixelFormat",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "uint8", "meaning": "8-bit unsigned integer (0-255)"},
    {"value": "uint16", "meaning": "16-bit unsigned integer (0-65535)"},
    {"value": "uint32", "meaning": "32-bit unsigned integer"},
    {"value": "int8", "meaning": "8-bit signed integer (-128 to 127)"},
    {"value": "int16", "meaning": "16-bit signed integer"},
    {"value": "int32", "meaning": "32-bit signed integer"},
    {"value": "float32", "meaning": "32-bit floating point"},
    {"value": "float64", "meaning": "64-bit floating point"}
  ]
}
```

### 10.2 Physical Size with Unit of Measure

```json
{
  "@type": "cr:Field",
  "@id": "image/physical_size_x",
  "name": "Physical Size X",
  "dataType": "sc:Float",

  "iso11179:dataElementConcept": {
    "@id": "dec:MicroscopyImage.PhysicalSizeX",
    "iso11179:objectClass": "Microscopy Image",
    "iso11179:property": "Physical Size in X Dimension"
  },

  "iso11179:valueDomain": {
    "@id": "vd:PhysicalSizeMicrometers",
    "iso11179:datatype": "Decimal",
    "iso11179:unitOfMeasure": "micrometer",
    "iso11179:minimumValue": 0.001,
    "iso11179:maximumValue": 1000.0
  }
}
```

---

## 11. Whole Slide Imaging Extension

### 11.1 WSI-Specific Value Domains

#### 11.1.1 Stain Type

```json
{
  "@id": "vd:HistologicalStainType",
  "iso11179:datatype": "String",
  "iso11179:permissibleValues": [
    {"value": "H&E", "meaning": "Hematoxylin and Eosin"},
    {"value": "IHC", "meaning": "Immunohistochemistry"},
    {"value": "PAS", "meaning": "Periodic Acid-Schiff"},
    {"value": "Trichrome", "meaning": "Masson's Trichrome"},
    {"value": "Gram", "meaning": "Gram Stain"},
    {"value": "Giemsa", "meaning": "Giemsa Stain"}
  ]
}
```

#### 11.1.2 Magnification

```json
{
  "@id": "vd:OpticalMagnification",
  "iso11179:datatype": "Integer",
  "iso11179:unitOfMeasure": "times",
  "iso11179:permissibleValues": [
    {"value": 2, "meaning": "2x magnification"},
    {"value": 4, "meaning": "4x magnification"},
    {"value": 10, "meaning": "10x magnification"},
    {"value": 20, "meaning": "20x magnification"},
    {"value": 40, "meaning": "40x magnification"},
    {"value": 60, "meaning": "60x magnification"},
    {"value": 100, "meaning": "100x magnification"}
  ]
}
```

---

## 12. Implementation Guidance

### 12.1 Minimal ISO 11179 Adoption (Level 1)

For basic Bio-Croissant datasets, ISO 11179 metadata is optional. Use only core Bio-Croissant properties.

### 12.2 Recommended Adoption (Level 2)

Include:
1. Administrative metadata (steward, submitter, registration status)
2. Value domains for all coded/categorical fields
3. Classification scheme membership

```python
def create_level2_dataset():
    return {
        "@context": {
            "bio": "http://mlcommons.org/croissant/bio/0.3/",
            "iso11179": "http://mlcommons.org/croissant/bio/iso11179/0.3/"
        },

        "iso11179:steward": {
            "@type": "sc:Person",
            "name": "Data Steward Name",
            "email": "steward@example.org"
        },

        "iso11179:registrationStatus": "standard",

        "bio:dataCategory": ["clinical"],
        "iso11179:valueDomain": {"@id": "vd:DataCategory"}
    }
```

### 12.3 Full Metadata Registry (Level 3)

Include complete ISO 11179 metadata for all fields:

```python
def create_level3_field():
    return {
        "@type": "cr:Field",
        "@id": "field_id",
        "name": "Field Name",
        "description": "Clear description following ISO 11179-4",
        "dataType": "sc:Integer",

        # Data Element Concept
        "iso11179:dataElementConcept": {
            "@id": "dec:ObjectClass.Property",
            "iso11179:objectClass": "Object Class",
            "iso11179:property": "Property",
            "iso11179:definition": "Precise, unambiguous definition"
        },

        # Value Domain
        "iso11179:valueDomain": {
            "@id": "vd:ValueDomainName",
            "iso11179:datatype": "Integer",
            "iso11179:permissibleValues": [
                {"value": 1, "meaning": "Meaning 1"},
                {"value": 2, "meaning": "Meaning 2"}
            ]
        },

        # Classification
        "iso11179:classifiedBy": [{"@id": "ci:ClassificationItem"}]
    }
```

### 12.4 Validation

Validate ISO 11179 metadata:

```python
def validate_iso11179_metadata(field):
    """Validate field has complete ISO 11179 metadata."""

    # Check data element concept
    assert "iso11179:dataElementConcept" in field
    dec = field["iso11179:dataElementConcept"]
    assert "iso11179:objectClass" in dec
    assert "iso11179:property" in dec
    assert "iso11179:definition" in dec

    # Check value domain
    assert "iso11179:valueDomain" in field
    vd = field["iso11179:valueDomain"]
    assert "iso11179:datatype" in vd

    # If coded, must have permissible values
    if is_coded_field(field):
        assert "iso11179:permissibleValues" in vd
        for pv in vd["iso11179:permissibleValues"]:
            assert "value" in pv
            assert "meaning" in pv

    return True
```

---

## 13. Appendices

### 13.1 Complete Example: OMOP Dataset with ISO 11179

See `examples/omop_cdm_iso11179.json`

### 13.2 Standard Value Domain Registry

See `value-domains/standard-value-domains.json`

### 13.3 ISO 11179 References

- [ISO/IEC 11179-1:2023 Framework](https://www.iso.org/standard/78914.html)
- [ISO/IEC 11179-3 Metamodel](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-5 Naming Principles](https://www.iso.org/standard/60341.html)
- [ISO/IEC 11179-6 Registration](https://www.iso.org/standard/78916.html)
- [Aristotle Metadata Registry Guide](https://help.aristotlecloud.io/subject-matter-and-theory/iso-iec-11179-data-element-representation)

### 13.4 Migration from v0.2 to v0.3

**Backward Compatibility:** All v0.2 metadata is valid in v0.3. ISO 11179 additions are optional unless targeting Level 2 or 3 conformance.

**Migration Steps:**
1. Add `iso11179` namespace to `@context`
2. Add administrative metadata (steward, registration status)
3. Define value domains for coded fields
4. Optionally add data element concepts for semantic clarity
5. Update `dct:conformsTo` to v0.3

### 13.5 Glossary

- **Conceptual Domain:** Set of valid value meanings, independent of representation
- **Data Element:** Unit of data defined by data element concept + value domain
- **Data Element Concept:** Concept formed by object class + property
- **Object Class:** Set of entities with common characteristics
- **Property:** Characteristic of an object class
- **Value Domain:** Set of permissible values with datatype specification
- **Value Meaning:** Semantic definition of a value in the conceptual domain
- **Permissible Value:** Allowed value in a value domain
- **Registration Authority:** Organization responsible for metadata registration

---

**Sources:**
- [ISO/IEC 11179 - Wikipedia](https://en.wikipedia.org/wiki/ISO/IEC_11179)
- [ISO/IEC 11179-1:2023 Framework](https://www.iso.org/standard/78914.html)
- [ISO/IEC 11179-31:2023 Metamodel](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-5:2015 Naming Principles](https://www.iso.org/standard/60341.html)
- [ISO/IEC 11179-6:2023 Registration](https://www.iso.org/standard/78916.html)
- [Aristotle Metadata - ISO 11179 Guide](https://help.aristotlecloud.io/subject-matter-and-theory/iso-iec-11179-data-element-representation)

**Document Status:** Candidate Recommendation
**Next Review Date:** 2026-06-04
**Contact:** bio-croissant@mlcommons.org
