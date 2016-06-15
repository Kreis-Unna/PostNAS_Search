CREATE TABLE postnas_search
(
  gml_id character(16),
  vector tsvector
)
WITH (
  OIDS=FALSE
);