CREATE TABLE postnas_search_logging
(
  datum timestamp without time zone NOT NULL,
  username text NOT NULL,
  requestType text,
  search text,
  result text[]
)
WITH (
  OIDS=FALSE
);
