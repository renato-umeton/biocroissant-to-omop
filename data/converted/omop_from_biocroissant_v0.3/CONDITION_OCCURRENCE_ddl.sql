CREATE TABLE CONDITION_OCCURRENCE (
  condition_occurrence_id INTEGER NOT NULL,
  person_id INTEGER,
  condition_concept_id INTEGER,
  PRIMARY KEY (condition_occurrence_id)
);