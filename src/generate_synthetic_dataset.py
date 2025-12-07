#!/usr/bin/env python3
"""
Generate synthetic biomedical dataset with Bio-Croissant v0.2 and v0.3 metadata.

This script demonstrates:
- Synthetic OMOP CDM clinical data generation
- Bio-Croissant v0.2 metadata creation
- Bio-Croissant v0.3 metadata with ISO 11179
- Data quality metrics calculation
- SHA-256 hash generation
"""

import json
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Output directories (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "generated"
OUTPUT_DIR = PROJECT_ROOT / "data" / "metadata"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


class OMOPSyntheticDataGenerator:
    """Generate synthetic OMOP CDM data."""

    # OMOP Concept IDs for reference
    GENDER_CONCEPTS = {
        "Male": 8507,
        "Female": 8532,
        "Unknown": 8551
    }

    RACE_CONCEPTS = {
        "White": 8527,
        "Black or African American": 8516,
        "Asian": 8515,
        "Other": 8522
    }

    ETHNICITY_CONCEPTS = {
        "Hispanic or Latino": 38003563,
        "Not Hispanic or Latino": 38003564
    }

    # Common condition concept IDs (SNOMED CT)
    CONDITION_CONCEPTS = {
        "Essential hypertension": 320128,
        "Type 2 diabetes mellitus": 201826,
        "Hyperlipidemia": 432867,
        "Coronary arteriosclerosis": 313217,
        "Atrial fibrillation": 313217,
        "Asthma": 317009,
        "Depression": 440383,
        "Osteoarthritis": 80180,
        "Chronic kidney disease": 46271022,
        "GERD": 318800
    }

    def __init__(self, n_patients: int = 1000):
        """Initialize generator.

        Args:
            n_patients: Number of synthetic patients to generate
        """
        self.n_patients = n_patients
        self.person_data = None
        self.condition_data = None
        self.quality_metrics = {}

    def generate_person_table(self) -> pd.DataFrame:
        """Generate synthetic PERSON table."""
        print(f"Generating {self.n_patients} synthetic patients...")

        persons = []
        for person_id in range(1, self.n_patients + 1):
            gender = random.choice(list(self.GENDER_CONCEPTS.keys()))
            race = random.choice(list(self.RACE_CONCEPTS.keys()))
            ethnicity = random.choice(list(self.ETHNICITY_CONCEPTS.keys()))

            # Generate birth year (18-90 years old)
            birth_year = random.randint(1934, 2006)

            person = {
                "person_id": person_id,
                "gender_concept_id": self.GENDER_CONCEPTS[gender],
                "year_of_birth": birth_year,
                "month_of_birth": random.randint(1, 12),
                "day_of_birth": random.randint(1, 28),
                "race_concept_id": self.RACE_CONCEPTS[race],
                "ethnicity_concept_id": self.ETHNICITY_CONCEPTS[ethnicity]
            }
            persons.append(person)

        self.person_data = pd.DataFrame(persons)
        return self.person_data

    def generate_condition_occurrence_table(self) -> pd.DataFrame:
        """Generate synthetic CONDITION_OCCURRENCE table."""
        print(f"Generating condition occurrences...")

        conditions = []
        condition_id = 1

        for person_id in range(1, self.n_patients + 1):
            # Each person gets 1-5 conditions
            n_conditions = random.randint(1, 5)

            birth_year = self.person_data[
                self.person_data['person_id'] == person_id
            ]['year_of_birth'].values[0]

            for _ in range(n_conditions):
                condition_name = random.choice(list(self.CONDITION_CONCEPTS.keys()))
                concept_id = self.CONDITION_CONCEPTS[condition_name]

                # Condition start date between age 18 and current age
                age_at_condition = random.randint(18, min(90, 2024 - birth_year))
                condition_year = birth_year + age_at_condition

                start_date = fake.date_between(
                    start_date=datetime(condition_year, 1, 1),
                    end_date=datetime(min(condition_year + 1, 2024), 12, 31)
                )

                condition = {
                    "condition_occurrence_id": condition_id,
                    "person_id": person_id,
                    "condition_concept_id": concept_id,
                    "condition_start_date": start_date.strftime("%Y-%m-%d"),
                    "condition_type_concept_id": 32020  # EHR encounter diagnosis
                }
                conditions.append(condition)
                condition_id += 1

        self.condition_data = pd.DataFrame(conditions)
        return self.condition_data

    def calculate_quality_metrics(self) -> Dict[str, Any]:
        """Calculate data quality metrics."""
        print("Calculating quality metrics...")

        person_completeness = (
            self.person_data.notna().sum() / len(self.person_data)
        ).mean()

        condition_completeness = (
            self.condition_data.notna().sum() / len(self.condition_data)
        ).mean()

        self.quality_metrics = {
            "overall_completeness": (
                (person_completeness + condition_completeness) / 2
            ),
            "person_completeness": person_completeness,
            "condition_completeness": condition_completeness,
            "total_patients": len(self.person_data),
            "total_conditions": len(self.condition_data),
            "avg_conditions_per_patient": len(self.condition_data) / len(self.person_data)
        }

        return self.quality_metrics

    def save_data(self) -> Dict[str, Path]:
        """Save generated data to CSV files and calculate hashes."""
        print("Saving data files...")

        person_path = DATA_DIR / "person.csv"
        condition_path = DATA_DIR / "condition_occurrence.csv"

        self.person_data.to_csv(person_path, index=False)
        self.condition_data.to_csv(condition_path, index=False)

        # Calculate SHA-256 hashes
        person_hash = self._calculate_sha256(person_path)
        condition_hash = self._calculate_sha256(condition_path)

        print(f"✓ Saved {person_path} ({person_path.stat().st_size} bytes)")
        print(f"  SHA-256: {person_hash}")
        print(f"✓ Saved {condition_path} ({condition_path.stat().st_size} bytes)")
        print(f"  SHA-256: {condition_hash}")

        return {
            "person": {"path": person_path, "hash": person_hash},
            "condition": {"path": condition_path, "hash": condition_hash}
        }

    @staticmethod
    def _calculate_sha256(file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()


class BioCroissantMetadataGenerator:
    """Generate Bio-Croissant metadata."""

    def __init__(self, data_info: Dict, quality_metrics: Dict):
        """Initialize metadata generator.

        Args:
            data_info: Information about generated data files
            quality_metrics: Quality metrics for the dataset
        """
        self.data_info = data_info
        self.quality_metrics = quality_metrics
        self.timestamp = datetime.now().isoformat()

    def generate_v02_metadata(self) -> Dict[str, Any]:
        """Generate Bio-Croissant v0.2 metadata."""
        print("\nGenerating Bio-Croissant v0.2 metadata...")

        metadata = {
            "@context": {
                "@language": "en",
                "@vocab": "https://schema.org/",
                "sc": "https://schema.org/",
                "cr": "http://mlcommons.org/croissant/",
                "dct": "http://purl.org/dc/terms/",
                "bio": "http://mlcommons.org/croissant/bio/0.2/",
                "omop": "http://mlcommons.org/croissant/bio/omop/0.2/"
            },
            "@type": ["sc:Dataset", "bioschemas:Dataset"],
            "dct:conformsTo": [
                "http://mlcommons.org/croissant/1.0",
                "http://mlcommons.org/croissant/bio/0.2"
            ],

            "name": "Synthetically Generated OMOP CDM Dataset - v0.2",
            "description": f"Automatically generated synthetic OMOP CDM v5.4 dataset with {self.quality_metrics['total_patients']} patients and {self.quality_metrics['total_conditions']} condition occurrences. Generated using Faker library on {datetime.now().strftime('%Y-%m-%d')}.",
            "url": "file:///" + str(DATA_DIR.absolute()),
            "version": "1.0.0",
            "datePublished": datetime.now().strftime("%Y-%m-%d"),
            "dateCreated": datetime.now().strftime("%Y-%m-%d"),
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "license": "https://creativecommons.org/publicdomain/zero/1.0/",

            "creator": [{
                "@type": "Person",
                "name": "Bio-Croissant Synthetic Data Generator",
                "email": "generated@example.org"
            }],

            "keywords": [
                "synthetic data",
                "OMOP CDM",
                "clinical data",
                "machine learning",
                "automated generation"
            ],

            "bio:conformanceLevel": "Level 1",
            "bio:extensions": ["omop"],
            "bio:dataCategory": ["clinical", "synthetic"],
            "bio:deidentificationMethod": "Synthetic",
            "bio:cohortDescription": f"Synthetically generated cohort of {self.quality_metrics['total_patients']} patients with ages ranging from 18 to 90 years. Each patient has between 1-5 condition diagnoses.",
            "bio:clinicalStudyType": "observational",
            "bio:authenticatedAccess": False,

            "omop:cdmVersion": "5.4",
            "omop:cdmSourceName": "Synthetic_Auto_Generated",
            "omop:vocabularyVersion": "2024-10-01",
            "omop:databaseDialect": "postgresql",

            "bio:qualityMetrics": {
                "bio:completeness": {
                    "overall": round(self.quality_metrics['overall_completeness'], 4),
                    "PERSON": round(self.quality_metrics['person_completeness'], 4),
                    "CONDITION_OCCURRENCE": round(self.quality_metrics['condition_completeness'], 4)
                }
            },

            "distribution": self._create_distribution_v02(),
            "recordSet": self._create_recordsets_v02()
        }

        return metadata

    def generate_v03_metadata(self) -> Dict[str, Any]:
        """Generate Bio-Croissant v0.3 metadata with ISO 11179."""
        print("\nGenerating Bio-Croissant v0.3 metadata with ISO 11179...")

        metadata = {
            # NOTE: Context URL is a PLACEHOLDER - does not exist yet
            "@context": "https://mlcommons.org/croissant/bio/0.3/context",
            "@type": ["sc:Dataset", "bioschemas:Dataset"],
            "dct:conformsTo": [
                "http://mlcommons.org/croissant/1.0",
                "http://mlcommons.org/croissant/bio/0.3"
            ],

            "name": "Synthetically Generated OMOP CDM Dataset - v0.3 ISO 11179",
            "description": f"Automatically generated synthetic OMOP CDM v5.4 dataset with complete ISO 11179 metadata registry. Contains {self.quality_metrics['total_patients']} patients and {self.quality_metrics['total_conditions']} condition occurrences. Demonstrates data element concepts, value domains, and administrative metadata.",
            "url": "file:///" + str(DATA_DIR.absolute()),
            "version": "2.0.0",
            "datePublished": datetime.now().strftime("%Y-%m-%d"),
            "dateCreated": datetime.now().strftime("%Y-%m-%d"),
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "license": "https://creativecommons.org/publicdomain/zero/1.0/",

            "creator": [{
                "@type": "Person",
                "name": "Bio-Croissant Synthetic Data Generator v0.3",
                "email": "generated@example.org"
            }],

            "keywords": [
                "synthetic data",
                "OMOP CDM",
                "ISO 11179",
                "metadata registry",
                "automated generation"
            ],

            "bio:conformanceLevel": "Level 3",
            "bio:extensions": ["omop"],
            "bio:dataCategory": ["clinical", "synthetic"],
            "bio:deidentificationMethod": "Synthetic",
            "bio:cohortDescription": f"Synthetically generated cohort of {self.quality_metrics['total_patients']} patients with ages ranging from 18 to 90 years.",
            "bio:clinicalStudyType": "observational",
            "bio:authenticatedAccess": False,

            "omop:cdmVersion": "5.4",
            "omop:cdmSourceName": "Synthetic_Auto_Generated_ISO11179",
            "omop:vocabularyVersion": "2024-10-01",
            "omop:databaseDialect": "postgresql",

            "bio:qualityMetrics": {
                "bio:completeness": {
                    "overall": round(self.quality_metrics['overall_completeness'], 4),
                    "PERSON": round(self.quality_metrics['person_completeness'], 4),
                    "CONDITION_OCCURRENCE": round(self.quality_metrics['condition_completeness'], 4)
                }
            },

            # ISO 11179 Administrative Metadata
            "iso11179:registrationAuthority": {
                "@type": "sc:Organization",
                "name": "Bio-Croissant Automated Registry",
                "url": "https://mlcommons.org/bio-croissant"  # PLACEHOLDER - URL does not exist yet
            },

            "iso11179:registrationStatus": "standard",

            "iso11179:steward": {
                "@type": "sc:Person",
                "name": "Automated Data Steward",
                "email": "steward@generated.example.org"
            },

            "iso11179:submitter": {
                "@type": "sc:Person",
                "name": "Synthetic Data Generator Bot",
                "email": "bot@generated.example.org"
            },

            "iso11179:registeredDate": self.timestamp,
            "iso11179:lastReviewedDate": self.timestamp,
            "iso11179:changeDescription": "Initial automated generation with complete ISO 11179 metadata",

            "distribution": self._create_distribution_v03(),
            "recordSet": self._create_recordsets_v03()
        }

        return metadata

    def _create_distribution_v02(self) -> List[Dict]:
        """Create distribution section for v0.2."""
        return [
            {
                "@type": "cr:FileObject",
                "@id": "person_csv",
                "name": "PERSON table",
                "contentUrl": str(self.data_info['person']['path']),
                "encodingFormat": "text/csv",
                "sha256": self.data_info['person']['hash'],
                "contentSize": f"{self.data_info['person']['path'].stat().st_size} bytes",
                "description": "OMOP PERSON table with synthetic demographic data"
            },
            {
                "@type": "cr:FileObject",
                "@id": "condition_csv",
                "name": "CONDITION_OCCURRENCE table",
                "contentUrl": str(self.data_info['condition']['path']),
                "encodingFormat": "text/csv",
                "sha256": self.data_info['condition']['hash'],
                "contentSize": f"{self.data_info['condition']['path'].stat().st_size} bytes",
                "description": "OMOP CONDITION_OCCURRENCE table with synthetic diagnosis records"
            }
        ]

    def _create_distribution_v03(self) -> List[Dict]:
        """Create distribution section for v0.3 (same as v0.2 for files)."""
        return self._create_distribution_v02()

    def _create_recordsets_v02(self) -> List[Dict]:
        """Create recordSet section for v0.2."""
        return [
            {
                "@type": "cr:RecordSet",
                "@id": "person",
                "name": "PERSON",
                "description": "Synthetic patient demographics per OMOP CDM PERSON table",
                "omop:cdmTable": "PERSON",
                "omop:tableDomain": "Clinical",
                "omop:distributionKey": "person_id",
                "key": [{"@id": "person/person_id"}],
                "field": [
                    {
                        "@type": "cr:Field",
                        "@id": "person/person_id",
                        "name": "person_id",
                        "description": "Unique identifier for each person",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "person_id",
                        "omop:isPrimaryKey": True,
                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "person_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "person/gender_concept_id",
                        "name": "gender_concept_id",
                        "description": "OMOP concept for gender",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "gender_concept_id",
                        "omop:conceptDomain": "Gender",
                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "gender_concept_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "person/year_of_birth",
                        "name": "year_of_birth",
                        "description": "Year of birth (synthetic)",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "year_of_birth",
                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "year_of_birth"}
                        }
                    }
                ]
            },
            {
                "@type": "cr:RecordSet",
                "@id": "condition_occurrence",
                "name": "CONDITION_OCCURRENCE",
                "description": "Synthetic condition diagnoses per OMOP CDM",
                "omop:cdmTable": "CONDITION_OCCURRENCE",
                "omop:tableDomain": "Clinical",
                "omop:distributionKey": "person_id",
                "key": [{"@id": "condition_occurrence/condition_occurrence_id"}],
                "field": [
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/condition_occurrence_id",
                        "name": "condition_occurrence_id",
                        "description": "Unique identifier for condition record",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "condition_occurrence_id",
                        "omop:isPrimaryKey": True,
                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "condition_occurrence_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/person_id",
                        "name": "person_id",
                        "description": "Foreign key to PERSON",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "person_id",
                        "omop:foreignKeyTable": "PERSON",
                        "references": {"@id": "person/person_id"},
                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "person_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/condition_concept_id",
                        "name": "condition_concept_id",
                        "description": "SNOMED concept for condition",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "condition_concept_id",
                        "omop:conceptDomain": "Condition",
                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "condition_concept_id"}
                        }
                    }
                ]
            }
        ]

    def _create_recordsets_v03(self) -> List[Dict]:
        """Create recordSet section for v0.3 with ISO 11179."""
        return [
            {
                "@type": "cr:RecordSet",
                "@id": "person",
                "name": "PERSON",
                "description": "Synthetic patient demographics with ISO 11179 metadata",
                "omop:cdmTable": "PERSON",
                "omop:tableDomain": "Clinical",
                "omop:distributionKey": "person_id",

                "iso11179:classifiedBy": [
                    {"@id": "ci:Demographics"}
                ],

                "key": [{"@id": "person/person_id"}],
                "field": [
                    {
                        "@type": "cr:Field",
                        "@id": "person/person_id",
                        "name": "person_id",
                        "description": "Unique identifier for each person",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "person_id",
                        "omop:isPrimaryKey": True,

                        "iso11179:dataElementConcept": {
                            "@id": "dec:Person.Identifier",
                            "iso11179:objectClass": "Person",
                            "iso11179:property": "Unique Identifier",
                            "iso11179:definition": "A unique integer assigned to identify each person in the database"
                        },

                        "iso11179:valueDomain": {
                            "@id": "vd:PositiveInteger",
                            "iso11179:datatype": "Integer",
                            "iso11179:minimumValue": 1
                        },

                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "person_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "person/gender_concept_id",
                        "name": "gender_concept_id",
                        "description": "OMOP concept for gender",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "gender_concept_id",
                        "omop:conceptDomain": "Gender",

                        "iso11179:dataElementConcept": {
                            "@id": "dec:Person.Gender",
                            "iso11179:objectClass": "Person",
                            "iso11179:property": "Gender",
                            "iso11179:definition": "The biological sex of a person"
                        },

                        "iso11179:valueDomain": {
                            "@id": "vd:OMOPGenderConceptID",
                            "iso11179:datatype": "Integer",
                            "iso11179:permissibleValues": [
                                {"value": 8507, "meaning": "Male"},
                                {"value": 8532, "meaning": "Female"},
                                {"value": 8551, "meaning": "Unknown"}
                            ]
                        },

                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "gender_concept_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "person/year_of_birth",
                        "name": "year_of_birth",
                        "description": "Year of birth (synthetic)",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "year_of_birth",

                        "iso11179:dataElementConcept": {
                            "@id": "dec:Person.BirthYear",
                            "iso11179:objectClass": "Person",
                            "iso11179:property": "Birth Year",
                            "iso11179:definition": "The calendar year in which a person was born"
                        },

                        "iso11179:valueDomain": {
                            "@id": "vd:Year",
                            "iso11179:datatype": "Integer",
                            "iso11179:minimumValue": 1900,
                            "iso11179:maximumValue": 2025
                        },

                        "source": {
                            "fileObject": {"@id": "person_csv"},
                            "extract": {"column": "year_of_birth"}
                        }
                    }
                ]
            },
            {
                "@type": "cr:RecordSet",
                "@id": "condition_occurrence",
                "name": "CONDITION_OCCURRENCE",
                "description": "Synthetic condition diagnoses with ISO 11179 metadata",
                "omop:cdmTable": "CONDITION_OCCURRENCE",
                "omop:tableDomain": "Clinical",
                "omop:distributionKey": "person_id",

                "iso11179:classifiedBy": [
                    {"@id": "ci:Diagnoses"}
                ],

                "key": [{"@id": "condition_occurrence/condition_occurrence_id"}],
                "field": [
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/condition_occurrence_id",
                        "name": "condition_occurrence_id",
                        "description": "Unique identifier for condition record",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "condition_occurrence_id",
                        "omop:isPrimaryKey": True,

                        "iso11179:dataElementConcept": {
                            "@id": "dec:ConditionOccurrence.Identifier",
                            "iso11179:objectClass": "Condition Occurrence",
                            "iso11179:property": "Unique Identifier",
                            "iso11179:definition": "A unique integer for each condition occurrence"
                        },

                        "iso11179:valueDomain": {
                            "@id": "vd:PositiveInteger",
                            "iso11179:datatype": "Integer",
                            "iso11179:minimumValue": 1
                        },

                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "condition_occurrence_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/person_id",
                        "name": "person_id",
                        "description": "Foreign key to PERSON",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "person_id",
                        "omop:foreignKeyTable": "PERSON",
                        "references": {"@id": "person/person_id"},

                        "iso11179:dataElementConcept": {
                            "@id": "dec:ConditionOccurrence.PersonReference",
                            "iso11179:objectClass": "Condition Occurrence",
                            "iso11179:property": "Person Reference",
                            "iso11179:definition": "The person who experienced this condition"
                        },

                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "person_id"}
                        }
                    },
                    {
                        "@type": "cr:Field",
                        "@id": "condition_occurrence/condition_concept_id",
                        "name": "condition_concept_id",
                        "description": "SNOMED concept for condition",
                        "dataType": "sc:Integer",
                        "omop:cdmField": "condition_concept_id",
                        "omop:conceptDomain": "Condition",

                        "iso11179:dataElementConcept": {
                            "@id": "dec:ConditionOccurrence.Condition",
                            "iso11179:objectClass": "Condition Occurrence",
                            "iso11179:property": "Medical Condition",
                            "iso11179:definition": "The standardized SNOMED concept representing the diagnosed condition"
                        },

                        "iso11179:valueDomain": {
                            "@id": "vd:OMOPConditionConceptID",
                            "iso11179:datatype": "Integer",
                            "iso11179:definition": "OMOP concept ID from Condition domain"
                        },

                        "source": {
                            "fileObject": {"@id": "condition_csv"},
                            "extract": {"column": "condition_concept_id"}
                        }
                    }
                ]
            }
        ]

    def save_metadata(self, version: str, metadata: Dict) -> Path:
        """Save metadata to JSON file."""
        filename = f"synthetic_dataset_{version}.json"
        output_path = OUTPUT_DIR / filename

        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"✓ Saved {output_path} ({output_path.stat().st_size} bytes)")
        return output_path


def main():
    """Main execution function."""
    print("="*70)
    print("Bio-Croissant Synthetic Dataset Generator")
    print("="*70)
    print()

    # Generate synthetic data
    generator = OMOPSyntheticDataGenerator(n_patients=1000)
    generator.generate_person_table()
    generator.generate_condition_occurrence_table()
    generator.calculate_quality_metrics()

    print("\nQuality Metrics:")
    for key, value in generator.quality_metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    data_info = generator.save_data()

    # Generate Bio-Croissant metadata
    metadata_gen = BioCroissantMetadataGenerator(data_info, generator.quality_metrics)

    # Generate v0.2 metadata
    v02_metadata = metadata_gen.generate_v02_metadata()
    v02_path = metadata_gen.save_metadata("v0.2", v02_metadata)

    # Generate v0.3 metadata
    v03_metadata = metadata_gen.generate_v03_metadata()
    v03_path = metadata_gen.save_metadata("v0.3", v03_metadata)

    print("\n" + "="*70)
    print("Generation Complete!")
    print("="*70)
    print(f"\nGenerated Files:")
    print(f"  Data:")
    print(f"    - {data_info['person']['path']}")
    print(f"    - {data_info['condition']['path']}")
    print(f"  Metadata:")
    print(f"    - {v02_path} (Bio-Croissant v0.2)")
    print(f"    - {v03_path} (Bio-Croissant v0.3 with ISO 11179)")

    print(f"\nNext steps:")
    print(f"  Validate v0.2: pipenv run python3 -c \"from validate_examples import validate_file; from pathlib import Path; validate_file(Path('{v02_path}'), Path('schema/biocroissant-v0.2-schema.json'))\"")
    print(f"  Validate v0.3: pipenv run python3 validate_v0.3.py")

    return v02_path, v03_path


if __name__ == "__main__":
    main()
