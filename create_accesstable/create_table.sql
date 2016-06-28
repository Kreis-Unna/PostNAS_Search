CREATE TABLE postnas_search_access_control
(
  username text NOT NULL,
  name text,
  access integer,
  CONSTRAINT pkey_postnas_search_access_control PRIMARY KEY (username)
)
WITH (
  OIDS=FALSE
);


CREATE TABLE postnas_search_accessmode
(
  id integer NOT NULL,
  bezeichnung text,
  CONSTRAINT pkey_postnas_search_access PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);


INSERT INTO postnas_search_accessmode (id,bezeichnung) VALUES (0,'Admin');
INSERT INTO postnas_search_accessmode (id,bezeichnung) VALUES (1,'Eigentümersuche');
INSERT INTO postnas_search_accessmode (id,bezeichnung) VALUES (2,'keine Eigentümersuche');