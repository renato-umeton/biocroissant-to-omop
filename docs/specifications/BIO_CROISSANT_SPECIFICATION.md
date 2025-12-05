# Bio-Croissant Format Specification

**Version:** 0.1.0 (Draft)
**Published:** December 2025
**Status:** Working Draft
**Canonical URI:** `http://mlcommons.org/croissant/bio/0.1`

## Authors

Bio-Croissant Working Group:
- Sebastian Lobentanzer (OMOP Workstream Lead)
- Josh Moore (Bioimage Workstream Lead)
- Agata Krason (Whole Slide Image Workstream Lead)
- Steffen Vogler (Bayer, Initiative Lead)
- Bio-Croissant Community Contributors

## Table of Contents

1. [Introduction](#introduction)
2. [Scope and Objectives](#scope-and-objectives)
3. [Conformance](#conformance)
4. [Namespaces and Vocabularies](#namespaces-and-vocabularies)
5. [Bio-Croissant Core Extensions](#bio-croissant-core-extensions)
6. [OMOP CDM Support](#omop-cdm-support)
7. [Bioimaging Support](#bioimaging-support)
8. [Whole Slide Imaging Support](#whole-slide-imaging-support)
9. [BioSchemas Alignment](#bioschemas-alignment)
10. [Security and Privacy](#security-and-privacy)
11. [Examples](#examples)
12. [Appendices](#appendices)

---

## 1. Introduction

### 1.1 Background

Bio-Croissant is an extension of the MLCommons Croissant metadata format designed specifically for biomedical, biological, and healthcare datasets. While the base Croissant format provides excellent support for general machine learning datasets, biomedical data presents unique challenges:

- **Standardized Clinical Data Models**: Healthcare data often conforms to established standards like OMOP CDM (Observational Medical Outcomes Partnership Common Data Model)
- **Complex Imaging Modalities**: Biomedical imaging includes microscopy, whole slide pathology images, and multi-dimensional array data
- **Privacy and Security**: Healthcare data requires robust authentication, authorization, and de-identification mechanisms
- **Domain-Specific Metadata**: Biological data includes specialized metadata for specimens, assays, protocols, and experimental conditions
- **Regulatory Compliance**: Must support HIPAA, GDPR, and other healthcare data regulations

### 1.2 Design Principles

Bio-Croissant adheres to the following principles:

1. **Backward Compatibility**: All Bio-Croissant datasets are valid Croissant datasets
2. **Minimal Extension**: Only add what is absolutely necessary for biomedical use cases
3. **Interoperability**: Align with existing biomedical standards (OMOP, OME, BioSchemas)
4. **Privacy-First**: Built-in support for de-identification and access control
5. **Modular Design**: Extensions are optional and can be used independently

### 1.3 Use Cases

Bio-Croissant supports the following primary use cases:

- **Clinical Data Exchange**: OMOP CDM datasets for observational health research
- **Microscopy Data Sharing**: Biological imaging with OME-Zarr and other array formats
- **Digital Pathology**: Whole slide images with annotations and metadata
- **Multi-Omics Integration**: Genomics, proteomics, metabolomics datasets
- **Federated Learning**: Privacy-preserving distributed ML on healthcare data
- **AI Model Training**: ML-ready biomedical datasets across modalities

---

## 2. Scope and Objectives

### 2.1 In Scope

- Extensions to Croissant for OMOP CDM v5.4+ datasets
- Bioimaging metadata for microscopy and array-based data
- Whole slide image (WSI) metadata and tile access patterns
- Healthcare-specific data types and semantic types
- Privacy and de-identification metadata
- Clinical vocabulary and concept mappings
- Biomedical-specific RecordSet patterns

### 2.2 Out of Scope

- Modifications to core Croissant specification
- Data storage or transmission protocols
- Clinical workflow management
- Electronic Health Record (EHR) system integration
- Real-time clinical decision support

---

## 3. Conformance

### 3.1 Base Croissant Conformance

Bio-Croissant datasets MUST:
- Conform to Croissant 1.0 specification
- Include `dct:conformsTo` pointing to both Croissant and Bio-Croissant specifications
- Use valid JSON-LD syntax
- Include all required Croissant dataset-level properties

### 3.2 Bio-Croissant Conformance Levels

**Level 1 - Basic Bio-Croissant**: Uses Bio-Croissant namespaces and data types without domain-specific extensions

**Level 2 - Domain-Specific**: Implements at least one domain extension (OMOP, Bioimaging, or WSI)

**Level 3 - Full Compliance**: Implements multiple extensions with complete metadata and BioSchemas alignment

### 3.3 Conformance Declaration

```json
{
  "@context": { ... },
  "@type": "sc:Dataset",
  "dct:conformsTo": [
    "http://mlcommons.org/croissant/1.0",
    "http://mlcommons.org/croissant/bio/0.1"
  ],
  "bio:conformanceLevel": "Level 2",
  "bio:extensions": ["omop", "bioimaging"]
}
```

---

## 4. Namespaces and Vocabularies

### 4.1 Namespace Definitions

Bio-Croissant introduces the following namespaces:

| Prefix | Namespace IRI | Description |
|--------|---------------|-------------|
| `bio` | `http://mlcommons.org/croissant/bio/` | Core Bio-Croissant vocabulary |
| `omop` | `http://mlcommons.org/croissant/bio/omop/` | OMOP CDM extensions |
| `bioimg` | `http://mlcommons.org/croissant/bio/imaging/` | Bioimaging extensions |
| `wsi` | `http://mlcommons.org/croissant/bio/wsi/` | Whole slide imaging extensions |
| `obo` | `http://purl.obolibrary.org/obo/` | Open Biological and Biomedical Ontologies |
| `bioschemas` | `https://bioschemas.org/` | BioSchemas vocabulary |

### 4.2 Recommended Context

```json
{
  "@context": {
    "@language": "en",
    "@vocab": "https://schema.org/",
    "sc": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/",
    "rai": "http://mlcommons.org/croissant/RAI/",
    "dct": "http://purl.org/dc/terms/",
    "bio": "http://mlcommons.org/croissant/bio/",
    "omop": "http://mlcommons.org/croissant/bio/omop/",
    "bioimg": "http://mlcommons.org/croissant/bio/imaging/",
    "wsi": "http://mlcommons.org/croissant/bio/wsi/",
    "obo": "http://purl.obolibrary.org/obo/",
    "bioschemas": "https://bioschemas.org/"
  }
}
```

---

## 5. Bio-Croissant Core Extensions

### 5.1 Dataset-Level Properties

Bio-Croissant adds the following properties to `sc:Dataset`:

#### Required Properties

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `bio:dataCategory` | Text | MANY | Category of biomedical data (e.g., "clinical", "imaging", "omics", "pathology") |
| `bio:deidentificationMethod` | Text or URL | ONE | Method used for de-identification (e.g., "HIPAA Safe Harbor", "Expert Determination") |

#### Recommended Properties

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `bio:clinicalStudyType` | Text or URL | ONE | Type of clinical study (e.g., "observational", "interventional", "registry") |
| `bio:cohortDescription` | Text | ONE | Description of the patient cohort or study population |
| `bio:dataUseOntology` | URL | MANY | Data Use Ontology (DUO) terms for permitted uses |
| `bio:specimenType` | Text or URL | MANY | Types of biological specimens (e.g., "blood", "tissue", "cell line") |
| `bio:assayType` | Text or URL | MANY | Experimental assay types (e.g., "RNA-seq", "immunohistochemistry") |
| `bio:authenticatedAccess` | Boolean | ONE | Whether dataset requires authentication for access |
| `bio:accessControlMechanism` | Text or URL | ONE | Access control mechanism (e.g., "OAuth2", "SAML", "institutional access") |

### 5.2 Bio-Croissant Data Types

#### Healthcare-Specific Data Types

| Data Type | URI | Description |
|-----------|-----|-------------|
| ConceptID | `bio:ConceptID` | Standardized vocabulary concept identifier |
| DateShifted | `bio:DateShifted` | Date that has been shifted for de-identification |
| AgeCategory | `bio:AgeCategory` | Age as category rather than exact value |
| DeidentifiedText | `bio:DeidentifiedText` | Text with PHI removed/masked |
| ClinicalCode | `bio:ClinicalCode` | Medical code (ICD, SNOMED, LOINC, etc.) |

#### Imaging Data Types

| Data Type | URI | Description |
|-----------|-----|-------------|
| MicroscopyImage | `bioimg:MicroscopyImage` | Microscopy image with dimensional metadata |
| MultiDimensionalArray | `bioimg:MultiDimensionalArray` | N-dimensional array (e.g., time, z-stack, channels) |
| ROI | `bioimg:ROI` | Region of interest in an image |
| WholeSlideImage | `wsi:WholeSlideImage` | Digital pathology whole slide image |
| ImagePyramid | `wsi:ImagePyramid` | Multi-resolution image pyramid |

### 5.3 Common Field Patterns

#### De-identified Date Field

```json
{
  "@type": "cr:Field",
  "@id": "recordset/date_shifted",
  "name": "Shifted Date",
  "dataType": "bio:DateShifted",
  "description": "Date shifted by random offset for de-identification",
  "bio:deidentificationNote": "All dates shifted by same random offset per patient",
  "source": { ... }
}
```

#### Concept ID with Vocabulary

```json
{
  "@type": "cr:Field",
  "@id": "recordset/condition_concept_id",
  "name": "Condition Concept ID",
  "dataType": "bio:ConceptID",
  "bio:vocabulary": "SNOMED CT",
  "bio:vocabularyVersion": "2024-01",
  "description": "Standard SNOMED concept for condition",
  "source": { ... }
}
```

---

## 6. OMOP CDM Support

### 6.1 Overview

The OMOP extension enables Bio-Croissant to fully represent OMOP Common Data Model v5.4 datasets, including clinical tables, vocabulary mappings, and analytical cohorts.

### 6.2 OMOP-Specific Properties

#### Dataset-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `omop:cdmVersion` | Text | ONE | OMOP CDM version (e.g., "5.4") |
| `omop:cdmSourceName` | Text | ONE | Name of the source database |
| `omop:vocabularyVersion` | Text | ONE | Version of OMOP vocabularies used |
| `omop:databaseDialect` | Text | ONE | SQL dialect (e.g., "postgresql", "sql_server") |

#### RecordSet-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `omop:cdmTable` | Text | ONE | Name of OMOP CDM table (e.g., "PERSON", "DRUG_EXPOSURE") |
| `omop:tableDomain` | Text | ONE | OMOP domain (e.g., "Clinical", "Vocabulary", "Health Economics") |
| `omop:distributionKey` | Text | ONE | Distribution key for table (e.g., "person_id", "RANDOM") |

#### Field-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `omop:cdmField` | Text | ONE | OMOP CDM field name |
| `omop:isRequired` | Boolean | ONE | Whether field is required in OMOP CDM |
| `omop:isPrimaryKey` | Boolean | ONE | Whether field is primary key |
| `omop:foreignKeyTable` | Text | ONE | Referenced table for foreign keys |
| `omop:foreignKeyField` | Text | ONE | Referenced field for foreign keys |
| `omop:conceptDomain` | Text | ONE | Domain for concept fields (e.g., "Gender", "Drug") |

### 6.3 OMOP RecordSet Patterns

#### Person Table

```json
{
  "@type": "cr:RecordSet",
  "@id": "person",
  "name": "PERSON",
  "description": "OMOP CDM PERSON table containing demographic information",
  "omop:cdmTable": "PERSON",
  "omop:tableDomain": "Clinical",
  "omop:distributionKey": "person_id",
  "key": [{ "@id": "person/person_id" }],
  "field": [
    {
      "@type": "cr:Field",
      "@id": "person/person_id",
      "name": "person_id",
      "dataType": "sc:Integer",
      "omop:cdmField": "person_id",
      "omop:isRequired": true,
      "omop:isPrimaryKey": true,
      "description": "Unique identifier for each person",
      "source": {
        "fileObject": { "@id": "person_table" },
        "extract": { "column": "person_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "person/gender_concept_id",
      "name": "gender_concept_id",
      "dataType": "bio:ConceptID",
      "omop:cdmField": "gender_concept_id",
      "omop:isRequired": true,
      "omop:foreignKeyTable": "CONCEPT",
      "omop:foreignKeyField": "concept_id",
      "omop:conceptDomain": "Gender",
      "bio:vocabulary": "OMOP Gender",
      "description": "Standard concept for biological sex",
      "references": { "@id": "concept/concept_id" },
      "source": {
        "fileObject": { "@id": "person_table" },
        "extract": { "column": "gender_concept_id" }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "person/year_of_birth",
      "name": "year_of_birth",
      "dataType": "sc:Integer",
      "omop:cdmField": "year_of_birth",
      "omop:isRequired": true,
      "description": "Year of birth",
      "bio:deidentificationNote": "May be generalized or shifted",
      "source": {
        "fileObject": { "@id": "person_table" },
        "extract": { "column": "year_of_birth" }
      }
    }
  ]
}
```

#### Drug Exposure Table with Event Reference

```json
{
  "@type": "cr:RecordSet",
  "@id": "drug_exposure",
  "name": "DRUG_EXPOSURE",
  "description": "OMOP CDM DRUG_EXPOSURE table",
  "omop:cdmTable": "DRUG_EXPOSURE",
  "omop:tableDomain": "Clinical",
  "omop:distributionKey": "person_id",
  "key": [{ "@id": "drug_exposure/drug_exposure_id" }],
  "field": [
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/drug_exposure_id",
      "name": "drug_exposure_id",
      "dataType": "sc:Integer",
      "omop:cdmField": "drug_exposure_id",
      "omop:isPrimaryKey": true,
      "source": { ... }
    },
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/person_id",
      "name": "person_id",
      "dataType": "sc:Integer",
      "omop:cdmField": "person_id",
      "omop:isRequired": true,
      "omop:foreignKeyTable": "PERSON",
      "omop:foreignKeyField": "person_id",
      "references": { "@id": "person/person_id" },
      "source": { ... }
    },
    {
      "@type": "cr:Field",
      "@id": "drug_exposure/drug_concept_id",
      "name": "drug_concept_id",
      "dataType": "bio:ConceptID",
      "omop:cdmField": "drug_concept_id",
      "omop:isRequired": true,
      "omop:foreignKeyTable": "CONCEPT",
      "omop:conceptDomain": "Drug",
      "bio:vocabulary": "RxNorm",
      "references": { "@id": "concept/concept_id" },
      "source": { ... }
    }
  ]
}
```

### 6.4 Vocabulary Tables

OMOP vocabulary tables (CONCEPT, VOCABULARY, DOMAIN, etc.) should be represented as standard RecordSets with appropriate concept mappings.

---

## 7. Bioimaging Support

### 7.1 Overview

The Bioimaging extension supports microscopy images, multi-dimensional arrays, and integration with formats like OME-Zarr, OME-TIFF, and HDF5.

### 7.2 Bioimaging Properties

#### Dataset-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `bioimg:imagingModality` | Text or URL | MANY | Imaging modality (e.g., "fluorescence", "brightfield", "electron microscopy") |
| `bioimg:dimensionality` | Text | ONE | Image dimensionality (e.g., "2D", "3D", "4D", "5D") |
| `bioimg:pixelFormat` | Text | ONE | Pixel data format (e.g., "uint8", "uint16", "float32") |

#### Field-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `bioimg:dimensions` | Object | ONE | Dimension specification (X, Y, Z, T, C) |
| `bioimg:physicalSizeX` | Number | ONE | Physical size per pixel in X (micrometers) |
| `bioimg:physicalSizeY` | Number | ONE | Physical size per pixel in Y (micrometers) |
| `bioimg:physicalSizeZ` | Number | ONE | Physical size per pixel in Z (micrometers) |
| `bioimg:timeIncrement` | Number | ONE | Time between frames (seconds) |
| `bioimg:channelNames` | Text | MANY | Names of image channels |
| `bioimg:channelColors` | Text | MANY | Display colors for channels (hex format) |

### 7.3 Multi-Dimensional Array Pattern

```json
{
  "@type": "cr:Field",
  "@id": "images/array_data",
  "name": "Image Array",
  "dataType": "bioimg:MultiDimensionalArray",
  "description": "5D microscopy image (TCZYX)",
  "bioimg:dimensions": {
    "T": 10,
    "C": 4,
    "Z": 50,
    "Y": 1024,
    "X": 1024
  },
  "bioimg:dimensionOrder": "TCZYX",
  "bioimg:pixelFormat": "uint16",
  "bioimg:physicalSizeX": 0.065,
  "bioimg:physicalSizeY": 0.065,
  "bioimg:physicalSizeZ": 0.3,
  "bioimg:physicalSizeUnit": "micrometer",
  "bioimg:timeIncrement": 5.0,
  "bioimg:timeUnit": "second",
  "bioimg:channelNames": ["DAPI", "GFP", "RFP", "CY5"],
  "bioimg:channelColors": ["#0000FF", "#00FF00", "#FF0000", "#FF00FF"],
  "source": {
    "fileObject": { "@id": "zarr_array" },
    "extract": { "path": "/image/0" }
  }
}
```

### 7.4 OME-Zarr Integration

```json
{
  "@type": "cr:FileObject",
  "@id": "ome_zarr_store",
  "name": "OME-Zarr Image Store",
  "contentUrl": "https://example.org/data/image.zarr",
  "encodingFormat": "application/zarr",
  "bioimg:omeZarrVersion": "0.4",
  "bioimg:pyramidLevels": 5,
  "bioimg:chunkSize": [1, 1, 1, 256, 256],
  "description": "OME-Zarr format microscopy image with multi-resolution pyramid"
}
```

### 7.5 Region of Interest (ROI)

```json
{
  "@type": "cr:Field",
  "@id": "annotations/roi",
  "name": "Cell ROI",
  "dataType": "bioimg:ROI",
  "description": "Cell segmentation regions of interest",
  "bioimg:roiType": "polygon",
  "source": {
    "fileObject": { "@id": "roi_annotations" },
    "extract": { "column": "roi_coordinates" },
    "format": "X Y"
  }
}
```

---

## 8. Whole Slide Imaging Support

### 8.1 Overview

The WSI extension supports digital pathology whole slide images with tiled access patterns, multi-resolution pyramids, and associated annotations.

### 8.2 WSI Properties

#### Dataset-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `wsi:scannerManufacturer` | Text | ONE | WSI scanner manufacturer |
| `wsi:scannerModel` | Text | ONE | WSI scanner model |
| `wsi:magnification` | Number | ONE | Objective lens magnification |
| `wsi:tissueType` | Text or URL | MANY | Tissue types in slides |
| `wsi:stainType` | Text or URL | MANY | Staining methods used (e.g., "H&E", "IHC") |

#### Field-Level

| Property | ExpectedType | Cardinality | Description |
|----------|--------------|-------------|-------------|
| `wsi:pyramidLevels` | Integer | ONE | Number of resolution levels in pyramid |
| `wsi:baseMagnification` | Number | ONE | Magnification at highest resolution level |
| `wsi:tileWidth` | Integer | ONE | Tile width in pixels |
| `wsi:tileHeight` | Integer | ONE | Tile height in pixels |
| `wsi:slideWidth` | Integer | ONE | Full slide width at base resolution |
| `wsi:slideHeight` | Integer | ONE | Full slide height at base resolution |
| `wsi:mppX` | Number | ONE | Microns per pixel in X dimension |
| `wsi:mppY` | Number | ONE | Microns per pixel in Y dimension |
| `wsi:compressionFormat` | Text | ONE | Tile compression (e.g., "JPEG", "JPEG2000", "LZW") |

### 8.3 Whole Slide Image Pattern

```json
{
  "@type": "cr:RecordSet",
  "@id": "whole_slide_images",
  "name": "Whole Slide Images",
  "description": "H&E stained whole slide images",
  "wsi:stainType": "H&E",
  "field": [
    {
      "@type": "cr:Field",
      "@id": "wsi/slide_image",
      "name": "Slide Image",
      "dataType": "wsi:WholeSlideImage",
      "description": "Multi-resolution whole slide image",
      "wsi:pyramidLevels": 8,
      "wsi:baseMagnification": 40,
      "wsi:tileWidth": 256,
      "wsi:tileHeight": 256,
      "wsi:slideWidth": 100000,
      "wsi:slideHeight": 80000,
      "wsi:mppX": 0.25,
      "wsi:mppY": 0.25,
      "wsi:compressionFormat": "JPEG",
      "wsi:colorSpace": "RGB",
      "source": {
        "fileObject": { "@id": "slide_svs_file" },
        "encodingFormat": "image/svs"
      }
    },
    {
      "@type": "cr:Field",
      "@id": "wsi/thumbnail",
      "name": "Slide Thumbnail",
      "dataType": "sc:ImageObject",
      "description": "Low-resolution thumbnail image",
      "source": {
        "fileObject": { "@id": "slide_svs_file" },
        "extract": { "wsi:pyramidLevel": 7 }
      }
    },
    {
      "@type": "cr:Field",
      "@id": "wsi/annotations",
      "name": "Pathologist Annotations",
      "dataType": "bioimg:ROI",
      "repeated": true,
      "description": "Tumor region annotations",
      "bioimg:roiType": "polygon",
      "source": {
        "fileObject": { "@id": "annotation_geojson" },
        "extract": { "jsonPath": "$.features[*].geometry.coordinates" }
      }
    }
  ]
}
```

### 8.4 Tile Access Locator

```json
{
  "@type": "cr:Field",
  "@id": "wsi/tile_locator",
  "name": "Tile Locations",
  "dataType": "wsi:TileLocator",
  "description": "List of tile coordinates for patch extraction",
  "repeated": true,
  "wsi:tileLocatorFormat": {
    "level": "sc:Integer",
    "x": "sc:Integer",
    "y": "sc:Integer",
    "width": "sc:Integer",
    "height": "sc:Integer"
  },
  "source": {
    "fileObject": { "@id": "tile_locations_csv" },
    "extract": { "column": "tile_coords" }
  }
}
```

---

## 9. BioSchemas Alignment

### 9.1 Overview

Bio-Croissant aligns with BioSchemas profiles to ensure interoperability with the life sciences semantic web ecosystem.

### 9.2 Dataset Profile Alignment

Bio-Croissant datasets SHOULD include BioSchemas Dataset profile properties:

```json
{
  "@context": [ ... ],
  "@type": ["sc:Dataset", "bioschemas:Dataset"],
  "bioschemas:taxonomicRange": "http://purl.obolibrary.org/obo/NCBITaxon_9606",
  "bioschemas:measurementTechnique": "http://purl.obolibrary.org/obo/OBI_0000070",
  "bioschemas:variableMeasured": ["gene expression", "protein abundance"],
  "bioschemas:isBasedOn": "https://example.org/parent-study"
}
```

### 9.3 Recommended BioSchemas Properties

| Property | Description |
|----------|-------------|
| `bioschemas:taxonomicRange` | Species or taxa covered (NCBI Taxonomy) |
| `bioschemas:measurementTechnique` | Measurement techniques used (OBI ontology) |
| `bioschemas:variableMeasured` | Variables or features measured |
| `bioschemas:isBasedOn` | Source dataset or study |
| `bioschemas:funding` | Funding sources |

---

## 10. Security and Privacy

### 10.1 De-identification Requirements

All Bio-Croissant datasets containing human subjects data MUST:

1. Declare de-identification method via `bio:deidentificationMethod`
2. Mark de-identified fields with appropriate data types
3. Document any retained identifiers and justification

### 10.2 Access Control

Datasets requiring authentication MUST specify:

```json
{
  "bio:authenticatedAccess": true,
  "bio:accessControlMechanism": "OAuth2",
  "bio:accessControlEndpoint": "https://example.org/auth",
  "bio:dataAccessCommittee": {
    "@type": "sc:Organization",
    "name": "Example Data Access Committee",
    "email": "dac@example.org"
  }
}
```

### 10.3 Data Use Ontology (DUO)

Datasets SHOULD specify permitted uses using DUO terms:

```json
{
  "bio:dataUseOntology": [
    "http://purl.obolibrary.org/obo/DUO_0000042",
    "http://purl.obolibrary.org/obo/DUO_0000006"
  ],
  "bio:dataUseDescription": "General research use, with publication moratorium until 2026-01-01"
}
```

---

## 11. Examples

### 11.1 Complete OMOP CDM Dataset Example

See [examples/omop_cdm_synthetic.json](examples/omop_cdm_synthetic.json)

### 11.2 Microscopy Dataset with OME-Zarr

See [examples/microscopy_ome_zarr.json](examples/microscopy_ome_zarr.json)

### 11.3 Digital Pathology WSI Dataset

See [examples/digital_pathology_wsi.json](examples/digital_pathology_wsi.json)

### 11.4 Multi-Omics Dataset

See [examples/multi_omics.json](examples/multi_omics.json)

---

## 12. Appendices

### Appendix A: Complete JSON-LD Context

```json
{
  "@context": {
    "@language": "en",
    "@vocab": "https://schema.org/",
    "sc": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/",
    "rai": "http://mlcommons.org/croissant/RAI/",
    "dct": "http://purl.org/dc/terms/",
    "bio": {
      "@id": "http://mlcommons.org/croissant/bio/",
      "@prefix": true
    },
    "omop": {
      "@id": "http://mlcommons.org/croissant/bio/omop/",
      "@prefix": true
    },
    "bioimg": {
      "@id": "http://mlcommons.org/croissant/bio/imaging/",
      "@prefix": true
    },
    "wsi": {
      "@id": "http://mlcommons.org/croissant/bio/wsi/",
      "@prefix": true
    },
    "obo": "http://purl.obolibrary.org/obo/",
    "bioschemas": "https://bioschemas.org/"
  }
}
```

### Appendix B: Data Type Reference

#### Bio-Croissant Core Data Types

| Data Type | URI | Base Type | Description |
|-----------|-----|-----------|-------------|
| ConceptID | `bio:ConceptID` | `sc:Integer` | Vocabulary concept identifier |
| DateShifted | `bio:DateShifted` | `sc:Date` | De-identified date |
| AgeCategory | `bio:AgeCategory` | `sc:Text` | Age range category |
| DeidentifiedText | `bio:DeidentifiedText` | `sc:Text` | PHI-removed text |
| ClinicalCode | `bio:ClinicalCode` | `sc:Text` | Medical coding |

#### Bioimaging Data Types

| Data Type | URI | Base Type | Description |
|-----------|-----|-----------|-------------|
| MicroscopyImage | `bioimg:MicroscopyImage` | `sc:ImageObject` | Microscopy image |
| MultiDimensionalArray | `bioimg:MultiDimensionalArray` | - | N-dimensional array |
| ROI | `bioimg:ROI` | `sc:GeoShape` | Region of interest |

#### WSI Data Types

| Data Type | URI | Base Type | Description |
|-----------|-----|-----------|-------------|
| WholeSlideImage | `wsi:WholeSlideImage` | `sc:ImageObject` | WSI with pyramid |
| ImagePyramid | `wsi:ImagePyramid` | - | Multi-resolution pyramid |
| TileLocator | `wsi:TileLocator` | - | Tile coordinate list |

### Appendix C: OMOP CDM Table Mapping

Complete mapping of OMOP CDM v5.4 tables to Bio-Croissant RecordSets:

| OMOP Table | RecordSet ID Pattern | Distribution Key | Domain |
|------------|---------------------|------------------|--------|
| PERSON | `person` | person_id | Clinical |
| OBSERVATION_PERIOD | `observation_period` | person_id | Clinical |
| VISIT_OCCURRENCE | `visit_occurrence` | person_id | Clinical |
| CONDITION_OCCURRENCE | `condition_occurrence` | person_id | Clinical |
| DRUG_EXPOSURE | `drug_exposure` | person_id | Clinical |
| PROCEDURE_OCCURRENCE | `procedure_occurrence` | person_id | Clinical |
| MEASUREMENT | `measurement` | person_id | Clinical |
| OBSERVATION | `observation` | person_id | Clinical |
| CONCEPT | `concept` | RANDOM | Vocabulary |
| VOCABULARY | `vocabulary` | RANDOM | Vocabulary |

### Appendix D: Validation Checklist

- [ ] Valid JSON-LD syntax
- [ ] Conforms to Croissant 1.0
- [ ] Includes Bio-Croissant conformance declaration
- [ ] De-identification method declared (if applicable)
- [ ] Access control mechanism specified (if authenticated)
- [ ] All concept fields reference vocabularies
- [ ] Foreign key relationships properly defined
- [ ] File checksums provided (recommended)
- [ ] License specified
- [ ] Citation information provided

### Appendix E: Change Log

**Version 0.1.0 (December 2025)**
- Initial draft specification
- OMOP CDM v5.4 support
- Bioimaging extensions
- Whole slide imaging extensions
- BioSchemas alignment
- Security and privacy framework

### Appendix F: Future Extensions

Planned for future versions:

- **Genomics Extension**: Support for VCF, BAM, FASTQ formats
- **Proteomics Extension**: Mass spectrometry data
- **Electronic Health Records**: FHIR integration
- **Clinical Trials**: Integration with ClinicalTrials.gov metadata
- **Federated Learning**: Privacy-preserving ML specifications
- **Synthetic Data**: Metadata for synthetic clinical data generation

---

## References

1. MLCommons Croissant Format Specification v1.0: https://docs.mlcommons.org/croissant/
2. OMOP Common Data Model v5.4: https://ohdsi.github.io/CommonDataModel/
3. BioSchemas: https://bioschemas.org/
4. OME Data Model: https://www.openmicroscopy.org/
5. Data Use Ontology (DUO): http://www.obofoundry.org/ontology/duo.html
6. HIPAA De-identification Methods: https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/

---

**Document Status**: Working Draft
**Last Updated**: December 4, 2025
**Feedback**: Please submit issues and suggestions to the Bio-Croissant working group
