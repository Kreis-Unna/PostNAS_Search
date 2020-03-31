CREATE TABLE public.postnas_search
(
  gml_id character(16),
  typ text,
  vector tsvector
)
WITH (
  OIDS=FALSE
);

CREATE INDEX idx_postnas_search
  ON public.postnas_search
  USING gin (vector);